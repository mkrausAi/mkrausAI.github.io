import os
from llm_processor import LLMProcessor
from models import *
from rfem_script_generator import generate_rfem_script
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """Get API key from environment or from string."""
    # First check environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        # If not in environment, use the hardcoded key (not recommended for production)
        logger.warning("Provide an OpenAI API-Key by setting the OPENAI_API_KEY environment variable.")
    
    return api_key

def process_input(processor, input_data, input_type, file_prefix, max_attempts=5):
    """Process a single input with retry logic."""
    log_info = {
        "input_type": input_type, 
        "filename": file_prefix, 
        "input_data": input_data[:50] if isinstance(input_data, str) else input_data
    }
    
    for attempt in range(1, max_attempts + 1):
        start_time = time.time()
        try:
            # Select the appropriate processor method
            if input_type == "text":
                result = processor.extract_entities_from_text(input_data)
            elif input_type == "image":
                result = processor.extract_entities_from_image(input_data)
            elif input_type == "audio":
                result = processor.extract_entities_from_audio(input_data)
            else:
                raise ValueError(f"Unsupported input type: {input_type}")
                
            # Generate and save RFEM script
            rfem_script = generate_rfem_script(result)
            with open(file_prefix, "w") as f:
                f.write(rfem_script)
                
            # Log success
            processing_time = time.time() - start_time
            logger.info(f"{input_type.capitalize()} input processed successfully on attempt {attempt} in {processing_time:.2f}s.")
            logger.info(f"RFEM script saved to file: {file_prefix}")
            
            # Update result metadata
            result.filename = file_prefix
            result.input_type = input_type
            
            # Update log info
            log_info.update({
                "success": True,
                "attempts": attempt,
                "processing_time": processing_time
            })
            logger.info(f"Processing details: {log_info}")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Attempt {attempt} failed with error: {str(e)}")
            
            # Update log info
            log_info.update({
                "success": False,
                "attempts": attempt,
                "error": str(e),
                "processing_time": processing_time
            })
            logger.info(f"Processing details: {log_info}")
            
            # Retry logic
            if attempt < max_attempts:
                retry_delay = 2 * attempt  # Exponential backoff
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Max retries reached. Giving up on this input.")
                return None

def run_study(processor, inputs, input_type, starting_index=0, max_attempts=5):
    """Runs a study processing a list of inputs with a retry mechanism."""
    study_results = []
    
    for i, input_data in enumerate(inputs):
        index = starting_index + i + 1
        file_prefix = f"generated_rfem_{input_type}_{index}.py"
        logger.info(f"Starting processing for {input_type.capitalize()} Input {i+1}/{len(inputs)}")
        
        result = process_input(processor, input_data, input_type, file_prefix, max_attempts)
        study_results.append(result)
        
    return study_results

def evaluate_results(results):
    """Evaluate the processing results."""
    evaluation_metrics = []
    for result in results:
        metrics = {}
        if result:
            metrics['filename'] = getattr(result, 'filename', 'N/A')
            metrics['input_type'] = getattr(result, 'input_type', 'N/A')
            # Add more specific checks based on the RFEM model attributes
            metrics['correct_material'] = result and result.materials and any(m.name == "C30/37" for m in result.materials)
            metrics['load_present'] = result and bool(result.loads)
            metrics['node_count'] = len(result.nodes) if result and result.nodes else 0
            metrics['load_count'] = len(result.loads) if result and result.loads else 0
        else:
            metrics['filename'] = 'Failed to process'
            metrics['input_type'] = 'N/A'
            metrics['correct_material'] = False
            metrics['load_present'] = False
            metrics['node_count'] = 0
            metrics['load_count'] = 0

        evaluation_metrics.append(metrics)
    return evaluation_metrics

def print_evaluation(evaluation_metrics):
    """Print evaluation metrics in a formatted way."""
    print("\n--- Evaluation Metrics ---")
    success_count = sum(1 for metric in evaluation_metrics if metric['filename'] != 'Failed to process')
    print(f"Successfully processed: {success_count}/{len(evaluation_metrics)} inputs")
    
    for i, metric in enumerate(evaluation_metrics, 1):
        print(f"\n{i}. File: {metric['filename']}")
        print(f"   Input Type: {metric['input_type']}")
        for key, value in metric.items():
            if key not in ["filename", "input_type"]:
                print(f"   {key}: {value}")
    print("---")

def main():
    """Main function to run the processing pipeline."""
    # Initialize processor with API key
    api_key = get_api_key()
    processor = LLMProcessor(api_key)
    
    # Define input data
    text_inputs = [
        "Design a concrete beam with a rectangular cross-section 30 x 50 cm made of C30/37, length 10 m, supported at both ends, with a uniform live load of 10 kN/m.",
        "Analyze a concrete column with a circular cross-section 40 cm diameter made of C40/50, height 5 m, fixed at the base and free at the top, with an axial load of 500 kN.",
        "Generate a concrete slab with dimensions 5m x 5m x 0.2m and material C25/30, simply supported on all four edges, subjected to a uniform live load of 5 kN/m².",
        "Model a concrete wall with dimensions 8m x 3m x 0.3m and material C35/45, fixed at the base and free at the top, with a line load of 2 kN/m at the top.",
        "Generate a concrete wall with dimensions 4.2m hight and 11.4 length and thickness 25 cm. There is a door with 2.2 m height and 1.5 m width at 4.1 m from the left. Concrete grade is C30/37. apply a line load on the most upper edge with magnitude 13.5 kN/m. the wall is Navier supported at the top and bottom line of the wall."
    ]

    image_paths = [
        "1_Sketch_Plate.png",
        "2_Sketch_Wall.png",
        "3_Drawing_Plate.png",
        "4_Sketch_Beam.png",
        "5_Sketch_Beam.png",
    ]

    audio_paths = [
        "1_voice.mp3",
        "2_voice.mp3",
        "3_voice.mp3",
        "4_voice.mp3",
        "5_voice.mp3",
    ]

    results = []
    max_attempts = 5

    # Process text inputs
    logger.info("Starting to process text inputs.")
    text_results = run_study(processor, text_inputs, "text", len(results), max_attempts)
    results.extend(text_results)

    # Process image inputs
    logger.info("Starting to process image inputs.")
    image_results = run_study(processor, image_paths, "image", len(results), max_attempts)
    results.extend(image_results)

    # Process audio inputs
    logger.info("Starting to process audio inputs.")
    audio_results = run_study(processor, audio_paths, "audio", len(results), max_attempts)
    results.extend(audio_results)

    # Evaluate and print results
    evaluation_metrics = evaluate_results(results)
    print_evaluation(evaluation_metrics)

if __name__ == "__main__":
    main()