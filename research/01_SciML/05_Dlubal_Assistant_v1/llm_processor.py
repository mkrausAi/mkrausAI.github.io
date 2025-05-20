from openai import OpenAI
from models import *
import base64
import json
from typing import Dict, Optional, Union

DEFAULT_INSTRUCTION = "Extract RFEM entities from the provided text and structure them according to the RFEMTemplate. If specific elements - such as node coordinates, section types, members, support conditions, lines, or load directions—are not explicitly mentioned, infer reasonable default values. Assume the positive z-direction is downward unless stated otherwise. Loads with positive magnitudes act downward in the positive z-direction. By default, assign walls vertically and plates or slabs horizontally. Unless specified, consider geometry to extend positively in the negative z-direction."

class LLMProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def process_section_data(self, section_data: Dict) -> SectionDefinition:
        """Processes the section data and creates a SectionDefinition object."""
        no = section_data.get("no", 1)  # Default value if 'no' is missing
        section_type_str = section_data.get("section_type", "STANDARD")  # Default section type

        try:
            section_type = SectionType(section_type_str.upper())
        except ValueError:
            raise ValueError(f"Invalid section_type: {section_type_str}")

        material_no = section_data.get("material_no", 1)  # Default material number

        # Section-specific parameters
        name = section_data.get("name")
        width = section_data.get("width")
        height = section_data.get("height")
        diameter = section_data.get("diameter")
        comment = section_data.get("comment", "")

        # Create and return the SectionDefinition object
        return SectionDefinition.create_section(
            no=no,
            section_type=section_type,
            material_no=material_no,
            name=name,
            width=width,
            height=height,
            diameter=diameter,
            comment=comment
        )

    def process_load_data(self, load_data: Dict) -> LoadDefinition:
        """Processes the load data and creates a LoadDefinition object."""
        no = load_data.get("no", 1)
        load_case_no = load_data.get("load_case_no", 1)
        load_type_str = load_data.get("load_type")
        magnitude = load_data.get("magnitude")
        applied_to = load_data.get("applied_to")
        comment = load_data.get("comment", "")

        try:
            load_type = LoadType(load_type_str.upper())
        except ValueError:
            raise ValueError(f"Invalid load_type: {load_type_str}")

        try:
            if load_type == LoadType.NODAL:
                nodal_load_data = load_data.get("nodal_load")
                if not nodal_load_data:
                    raise ValueError("Nodal load data is missing")

                load_direction_str = nodal_load_data.get("load_direction")
                load_direction = NodalLoadDirection(load_direction_str)

                return LoadDefinition.create_nodal_load(
                    no=no,
                    load_case_no=load_case_no,
                    nodes_no=','.join(map(str, applied_to)),
                    load_direction=load_direction,
                    magnitude=magnitude,
                    comment=comment
                )
            elif load_type == LoadType.MEMBER:
                member_load_data = load_data.get("member_load")
                if not member_load_data:
                    raise ValueError("Member load data is missing")

                load_direction_str = member_load_data.get("load_direction")
                load_direction = MemberLoadDirection(load_direction_str)

                return LoadDefinition.create_member_load(
                    no=no,
                    load_case_no=load_case_no,
                    members_no=','.join(map(str, applied_to)),
                    load_direction=load_direction,
                    magnitude=magnitude,
                    comment=comment
                )
            elif load_type == LoadType.SURFACE:
                surface_load_data = load_data.get("surface_load")
                if not surface_load_data:
                    raise ValueError("Surface load data is missing")

                return LoadDefinition.create_surface_load(
                    no=no,
                    load_case_no=load_case_no,
                    surface_no=','.join(map(str, applied_to)),
                    magnitude=magnitude,
                    comment=comment
                )
            elif load_type == LoadType.LINE:
                line_load_data = load_data.get("line_load")
                if not line_load_data:
                    raise ValueError("Line load data is missing")

                load_direction_str = line_load_data.get("load_direction")
                load_direction = LineLoadDirection(load_direction_str)

                return LoadDefinition.create_line_load(
                    no=no,
                    load_case_no=load_case_no,
                    lines_no=','.join(map(str, applied_to)),
                    load_direction=load_direction,
                    magnitude=magnitude,
                    comment=comment
                )
            else:
                raise ValueError(f"Unsupported load type: {load_type}")

        except ValueError as e:
            raise ValueError(f"Error creating LoadDefinition: {e}")

    def _process_api_response(self, response) -> RFEMTemplate:
        """Process the API response and convert it to an RFEMTemplate object."""
        if not hasattr(response.choices[0].message, 'function_call'):
            raise ValueError("The response does not contain a valid function call.")
            
        function_call_args = response.choices[0].message.function_call.arguments
        data = json.loads(function_call_args)
        
        # Set empty lists for missing optional fields
        for field in ['sections', 'nodes', 'members', 'supports', 'lines']:
            if data.get(field) is None:
                data[field] = []
                
        # Process sections to create SectionDefinition objects
        if "sections" in data and data["sections"]:
            data["sections"] = [self.process_section_data(section_data) for section_data in data["sections"]]

        # Process loads to create LoadDefinition objects
        if "loads" in data and data["loads"]:
            data["loads"] = [self.process_load_data(load_data) for load_data in data["loads"]]

        # Use model_validate to create the RFEMTemplate object
        return RFEMTemplate.model_validate(data)

    def extract_entities_from_text(self, text: str) -> RFEMTemplate:
        """Extracts RFEM entities from text input."""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": DEFAULT_INSTRUCTION},
                {"role": "user", "content": text}
            ],
            functions=[{"name": "fill_rfem_template", "parameters": RFEMTemplate.model_json_schema()}],
            function_call={"name": "fill_rfem_template"}
        )
        print("Text Response:", response)  # Debugging
        return self._process_api_response(response)

    def extract_entities_from_image(self, image_path: str) -> RFEMTemplate:
        """Extracts RFEM entities from an image file."""
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {image_path}")
        except Exception as e:
            raise ValueError(f"Error reading image file: {str(e)}")

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": DEFAULT_INSTRUCTION},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract RFEM entities from this image:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            functions=[{"name": "fill_rfem_template", "parameters": RFEMTemplate.model_json_schema()}],
            function_call={"name": "fill_rfem_template"}
        )
        print("Image Response:", response)  # Debugging
        return self._process_api_response(response)

    def extract_entities_from_audio(self, audio_file_path: str) -> RFEMTemplate:
        """
        Extracts RFEM entities from an audio file by transcribing the audio to text
        and then extracting entities from the transcribed text.
        """
        try:
            text = self.transcribe_audio(audio_file_path)
            if not text:
                raise ValueError("Audio transcription yielded empty text")
            return self.extract_entities_from_text(text)
        except Exception as e:
            raise ValueError(f"Error extracting entities from audio: {str(e)}")
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file to text using OpenAI's Whisper model.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcription
        except FileNotFoundError:
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        except Exception as e:
            raise ValueError(f"Error transcribing audio: {str(e)}")