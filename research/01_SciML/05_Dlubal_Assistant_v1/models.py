from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Union, List, Optional, Dict

class MaterialDefinition(BaseModel):
    no: int = Field(..., description="Material Tag")
    name: str = Field(..., description="Name of Desired Material (As Named in RSTAB Database)")
    comment: Optional[str] = Field("", description="Comments")


class SectionType(str, Enum):
    STANDARD = "STANDARD"
    RECTANGULAR = "RECTANGULAR"
    CIRCULAR = "CIRCULAR"


class SectionDefinition(BaseModel):
    no: int = Field(..., description="Section Tag")
    section_type: SectionType = Field(..., description="Type of section (STANDARD, RECTANGULAR, CIRCULAR)")
    name: str = Field(..., description="Name of Desired Section")
    material_no: int = Field(..., description="Tag of Material assigned to Section")
    width: Optional[float] = Field(None, description="Width of rectangular section in m")
    height: Optional[float] = Field(None, description="Height of rectangular section in m")
    diameter: Optional[float] = Field(None, description="Diameter of circular section in m")
    comment: Optional[str] = Field("", description="Comments")

    @classmethod
    def create_section(cls, no: int, section_type: SectionType, material_no: int,
                       name: Optional[str] = None, width: Optional[float] = None,
                       height: Optional[float] = None, diameter: Optional[float] = None,
                       comment: str = "") -> "SectionDefinition":
        if section_type == SectionType.STANDARD:
            return cls(no=no, name=name, material_no=material_no, comment=comment)
        elif section_type == SectionType.RECTANGULAR:
            name = f"R_M1 {width}/{height}" #SQ
            return cls(no=no, section_type=section_type, name=name, material_no=material_no, width=width, height=height, diameter=diameter, comment=comment)
        elif section_type == SectionType.CIRCULAR:
            name = f"CIRCLE_M1 {diameter}"
            return cls(no=no, section_type=section_type, name=name, material_no=material_no, width=width, height=height, diameter=diameter, comment=comment)
        else:
            raise ValueError(f"Invalid section_type: {section_type}")

class ThicknessDefinition(BaseModel):
    no: int = Field(..., description="Thickness Tag")
    name: str = Field(..., description="Thickness Name")
    material_no: int = Field(..., description="Tag of Material assigned to Thickness")
    uniform_thickness_d: float = Field(..., description="Magnitude of Thickness in meters")
    comment: Optional[str] = Field("", description="Comments")


class NodeDefinition(BaseModel):
    no: int = Field(..., description="Node Tag")
    coordinate_X: float = Field(..., description="X-Coordinate in meters")
    coordinate_Y: float = Field(..., description="Y-Coordinate in meters")
    coordinate_Z: float = Field(..., description="Z-Coordinate in meters")
    comment: Optional[str] = Field("", description="Comments")

class LineType(str, Enum):
    TYPE_POLYLINE = "TYPE_POLYLINE"
    TYPE_ARC = "TYPE_ARC"
    TYPE_CIRCLE = "TYPE_CIRCLE"
    TYPE_ELLIPTICAL_ARC = "TYPE_ELLIPTICAL_ARC"
    TYPE_ELLIPSE = "TYPE_ELLIPSE"
    TYPE_PARABOLA = "TYPE_PARABOLA"
    TYPE_SPLINE = "TYPE_SPLINE"
    TYPE_NURBS = "TYPE_NURBS"

class LineArcAlphaAdjustmentTarget(str, Enum):
    ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC = "ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC"

class Line(BaseModel):
    no: int = Field(1, description="Line Tag")
    type: LineType = Field(LineType.TYPE_POLYLINE, description="Line Type")
    nodes_no: Optional[str] = Field(None, description="Nodes Defining Line (e.g., '1 2')")
    comment: str = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")

    # Arc specific
    arc_first_node: Optional[int] = Field(None, description="First Node for Arc")
    arc_second_node: Optional[int] = Field(None, description="Second Node for Arc")
    control_point: Optional[List[float]] = Field(None, description="Control Point for Arc [X, Y, Z]")
    alpha_adjustment_target: LineArcAlphaAdjustmentTarget = Field(LineArcAlphaAdjustmentTarget.ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC, description="Arc Alpha Adjustment")

    # Circle Specific
    circle_center_coordinate: Optional[List[float]] = Field(None, description="Center of Circle [X, Y, Z]")
    circle_radius: Optional[float] = Field(None, description="Circle Radius")
    point_of_normal_to_circle_plane: Optional[List[float]] = Field(None, description="Vector from Circle Center to Point Normal to Circle Plane [X, Y, Z]")

    # Elliptical Arc Specific
    elliptical_arc_first_control_point: Optional[List[float]] = Field(None, description="Ellipse Arc Control Point 1 [X, Y, Z]")
    elliptical_arc_second_control_point: Optional[List[float]] = Field(None, description="Ellipse Arc Control Point 2 [X, Y, Z]")
    elliptical_arc_perimeter_control_point: Optional[List[float]] = Field(None, description="Ellipse Arc Perimeter Control Point [X, Y, Z]")
    arc_angle_alpha: Optional[float] = Field(None, description="Alpha Arc Angle (in Radians)")
    arc_angle_beta: Optional[float] = Field(None, description="Beta Arc Angle (in Radians)")

    # Ellipse Specific
    ellipse_first_node: Optional[int] = Field(None, description="First Node of Ellipse")
    ellipse_second_node: Optional[int] = Field(None, description="Second Node of Ellipse")
    ellipse_control_point: Optional[List[float]] = Field(None, description="Ellipse Control Point [X, Y, Z]")

    # Parabola Specific
    parabola_first_node: Optional[int] = Field(None, description="First Node for Parabola")
    parabola_second_node: Optional[int] = Field(None, description="Second Node for Parabola")
    parabola_control_point: Optional[List[float]] = Field(None, description="Parabola Control Point [X, Y, Z]")
    parabola_alpha: Optional[float] = Field(None, description="Alpha Angle (in Radians)")

    # NURBS Specific
    control_points: Optional[List[List[float]]] = Field(None, description="Nested List of Control Points [X, Y, Z]")
    weights: Optional[List[float]] = Field(None, description="Weights for NURBS Control Points")
    order: Optional[int] = Field(None, description="Order of NURBS Curve")

    # Methods for creating lines with specific types
    @classmethod
    def Polyline(cls, no: int = 1, nodes_no: str = '1 2', comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_POLYLINE, nodes_no=nodes_no, comment=comment, params=params)

    @classmethod
    def Arc(cls, no: int, nodes_no: List[int], control_point: List[float], alpha_adjustment_target: LineArcAlphaAdjustmentTarget = LineArcAlphaAdjustmentTarget.ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC, comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_ARC, nodes_no=' '.join(map(str, nodes_no)), arc_first_node=nodes_no[0], arc_second_node=nodes_no[1], control_point=control_point, alpha_adjustment_target=alpha_adjustment_target, comment=comment, params=params)

    @classmethod
    def Circle(cls, no: int = 1, center_of_circle: List[float] = [20,0,0], circle_radius: float = 1.0, point_of_normal_to_circle_plane: List[float] = [1,0,0], comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_CIRCLE, circle_center_coordinate=center_of_circle, circle_radius=circle_radius, point_of_normal_to_circle_plane=point_of_normal_to_circle_plane, comment=comment, params=params)

    @classmethod
    def EllipticalArc(cls, no: int = 1, p1_control_point: List[float] = [0,-6,0], p2_control_point: List[float] = [20,-6,0], p3_control_point: List[float] = [10,10,3], arc_angle_alpha: float = 0, arc_angle_beta: float = 3.141592653589793, comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_ELLIPTICAL_ARC, elliptical_arc_first_control_point=p1_control_point, elliptical_arc_second_control_point=p2_control_point, elliptical_arc_perimeter_control_point=p3_control_point, arc_angle_alpha=arc_angle_alpha, arc_angle_beta=arc_angle_beta, comment=comment, params=params)

    @classmethod
    def Ellipse(cls, no: int = 1, nodes_no: List[int] = [5,10], ellipse_control_point: List[float] = [18,-4.8,0], comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_ELLIPSE, nodes_no=' '.join(map(str, nodes_no)), ellipse_first_node=nodes_no[0], ellipse_second_node=nodes_no[1], ellipse_control_point=ellipse_control_point, comment=comment, params=params)

    @classmethod
    def Parabola(cls, no: int = 1, nodes_no: List[int] = [3,8], parabola_control_point: List[float] = [10,-3,0], parabola_alpha: float = 0, comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_PARABOLA, nodes_no=' '.join(map(str, nodes_no)), parabola_first_node=nodes_no[0], parabola_second_node=nodes_no[1], parabola_control_point=parabola_control_point, parabola_alpha=parabola_alpha, comment=comment, params=params)

    @classmethod
    def Spline(cls, no: int = 1, nodes_no: str = '1 3 5', comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_SPLINE, nodes_no=nodes_no, comment=comment, params=params)

    @classmethod
    def NURBS(cls, no: int = 1, nodes_no: str = '1 2', control_points: Optional[List[List[float]]] = None, weights: Optional[List[float]] = None, order: int = 0, comment: str = '', params: dict = None):
        return cls(no=no, type=LineType.TYPE_NURBS, nodes_no=nodes_no, control_points=control_points, weights=weights, order=order, comment=comment, params=params)


class SurfaceDefinition(BaseModel):
    no: int = Field(..., description="Surface Tag")
    thickness_no: int = Field(..., description="Thickness Tag")
    boundary_lines: List[int] = Field(..., description="List of Boundary Line Tags")
    comment: Optional[str] = Field("", description="Comments")

class MemberDefinition(BaseModel):
    no: int = Field(..., description="Member Tag")
    start_node_no: int = Field(..., description="Start Node Tag")
    end_node_no: int = Field(..., description="End Node Tag")
    rotation_angle: float = Field(0.0, description="Rotation Angle")
    start_section_no: int = Field(..., description="Start Section Tag")
    end_section_no: int = Field(..., description="End Section Tag")
    start_member_hinge_no: int = Field(0, description="Start Member Hinge Tag")
    end_member_hinge_no: int = Field(0, description="End Member Hinge Tag")
    line: Optional[int] = Field(None, description="Line Tag")
    comment: str = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")



class NodalSupportType(str, Enum):
    FIXED = "FIXED"
    HINGED = "HINGED"
    ROLLER = "ROLLER"
    ROLLER_IN_X = "ROLLER_IN_X"
    ROLLER_IN_Y = "ROLLER_IN_Y"
    ROLLER_IN_Z = "ROLLER_IN_Z"
    FREE = "FREE"

class LineSupportType(str, Enum):
    FIXED = "FIXED"
    HINGED = "HINGED"
    SLIDING_IN_X_AND_Y = "SLIDING_IN_X_AND_Y"
    SLIDING_IN_X = "SLIDING_IN_X"
    SLIDING_IN_Y = "SLIDING_IN_Y"
    SLIDING_IN_Z = "SLIDING_IN_Z"
    FREE = "FREE"

class NodalSupport(BaseModel):
    no: int = Field(1, description="Nodal Support Tag")
    nodes_no: str = Field("1 2", description="Assigned to Nodes (e.g., '1 2')")
    support: Union[NodalSupportType, List[float]] = Field(
        NodalSupportType.HINGED,
        description="Support Definition: NodalSupportType enum or list of 6 support condition values"
    )
    comment: Optional[str] = Field("", description="Comment")
    params: Optional[Dict] = Field(
        None,
        description="Any WS Parameter relevant to the object and its value in form of a dictionary"
    )
    # @model_validator(mode='after') #remoced for compatibility reasons
    def validate_support(cls, values):
        support = values.get('support')
        if isinstance(support, list):
            if len(support) != 6:
                raise ValueError('If support is a list, it must contain exactly 6 items.')
        elif not isinstance(support, NodalSupportType):
            raise ValueError('support must be either a valid NodalSupportType enum or a list of 6 items.')
        return values
    def to_client_object(self, model):
        clientObject = model.clientModel.factory.create('ns0:nodal_support')
        clearAttributes(clientObject)
        clientObject.no = self.no
        clientObject.nodes = ConvertToDlString(self.nodes_no)
        inf = float('inf')
        if self.support == NodalSupportType.FIXED:
            clientObject = setNodalSupportConditions(clientObject, inf, inf, inf, inf, inf, inf)
        elif self.support == NodalSupportType.HINGED:
            clientObject = setNodalSupportConditions(clientObject, inf, inf, inf, 0.0, 0.0, inf)
        elif self.support == NodalSupportType.ROLLER:
            clientObject = setNodalSupportConditions(clientObject, 0.0, 0.0, inf, 0.0, 0.0, inf)
        elif self.support == NodalSupportType.ROLLER_IN_X:
            clientObject = setNodalSupportConditions(clientObject, 0.0, inf, inf, 0.0, 0.0, inf)
        elif self.support == NodalSupportType.ROLLER_IN_Y:
            clientObject = setNodalSupportConditions(clientObject, inf, 0.0, inf, 0.0, 0.0, inf)
        elif self.support == NodalSupportType.ROLLER_IN_Z:
            clientObject = setNodalSupportConditions(clientObject, inf, inf, 0.0, 0.0, 0.0, inf)
        elif self.support == NodalSupportType.FREE:
            clientObject = setNodalSupportConditions(clientObject, 0, 0, 0, 0, 0, 0)
        elif isinstance(self.support, list):
            clientObject = setNodalSupportConditions(clientObject, *self.support)
        clientObject.comment = self.comment
        if self.params:
            for key, value in self.params.items():
                setattr(clientObject, key, value)
        deleteEmptyAttributes(clientObject)
        model.clientModel.service.set_nodal_support(clientObject)
        return clientObject

class LineSupport(BaseModel):
    no: int = Field(1, description="Line Support Tag")
    lines_no: str = Field("1 2", description="Assigned Lines (e.g., '1 2')")
    support_type: Union[LineSupportType, List[float]] = Field(
        LineSupportType.HINGED,
        description="Line Support Type Enumeration or a list of 6 support condition values",
    )
    comment: Optional[str] = Field("", description="Comments")
    params: Optional[Dict] = Field(
        None,
        description="Any WS Parameter relevant to the object and its value in the form of a dictionary",
    )
    # @model_validator(mode='after') # removed for compatibility reasons
    def validate_support_type(cls, values):
        support_type = values.get('support_type')
        if isinstance(support_type, list):
            if len(support_type) != 6:
                raise ValueError("If support_type is a list, it must contain exactly 6 items.")
        elif not isinstance(support_type, LineSupportType):
            raise ValueError("support_type must be either a valid LineSupportType enum or a list of 6 items.")
        return values
    def to_client_object(self, model):
        client_object = model.clientModel.factory.create("ns0:line_support")
        clearAttributes(client_object)
        client_object.no = self.no
        client_object.lines = ConvertToDlString(self.lines_no)
        inf = float('inf')
        if self.support_type == LineSupportType.FIXED:
            client_object = setLineSupportConditions(client_object, inf, inf, inf, inf, inf, inf)
        elif self.support_type == LineSupportType.HINGED:
            client_object = setLineSupportConditions(client_object, inf, inf, inf, 0.0, 0.0, 0.0)
        elif self.support_type == LineSupportType.SLIDING_IN_X_AND_Y:
            client_object = setLineSupportConditions(client_object, 0.0, 0.0, inf, 0.0, 0.0, inf)
        elif self.support_type == LineSupportType.SLIDING_IN_X:
            client_object = setLineSupportConditions(client_object, 0.0, inf, inf, 0.0, 0.0, inf)
        elif self.support_type == LineSupportType.SLIDING_IN_Y:
            client_object = setLineSupportConditions(client_object, inf, 0.0, inf, 0.0, 0.0, inf)
        elif self.support_type == LineSupportType.SLIDING_IN_Z:
            client_object = setLineSupportConditions(client_object, inf, inf, 0.0, 0.0, 0.0, inf)
        elif self.support_type == LineSupportType.FREE:
            client_object = setLineSupportConditions(client_object, 10000.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elif isinstance(self.support_type, list):
            client_object = setLineSupportConditions(client_object, *self.support_type)
        client_object.comment = self.comment
        if self.params:
            for key, value in self.params.items():
                setattr(client_object, key, value)
        deleteEmptyAttributes(client_object)
        model.clientModel.service.set_line_support(client_object)
        return client_object


class LoadType(str, Enum):
    NODAL = "NODAL"
    MEMBER = "MEMBER"
    SURFACE = "SURFACE"
    LINE = "LINE"

class NodalLoadDirection(str, Enum):
    '''
    Nodal Load Direction
    '''
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U = "LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U"
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V = "LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V"
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W = "LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W"
    LOAD_DIRECTION_LOCAL_X = "LOAD_DIRECTION_LOCAL_X"
    LOAD_DIRECTION_LOCAL_Y = "LOAD_DIRECTION_LOCAL_Y"
    LOAD_DIRECTION_LOCAL_Z = "LOAD_DIRECTION_LOCAL_Z"


class MemberLoadDirection(str, Enum):
    '''
    Member Load Direction
    '''
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED = "LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED"
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE = "LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE"
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED = "LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED"
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE = "LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE"
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED = "LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED"
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE = "LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE"
    LOAD_DIRECTION_LOCAL_X = "LOAD_DIRECTION_LOCAL_X"
    LOAD_DIRECTION_LOCAL_Y = "LOAD_DIRECTION_LOCAL_Y"
    LOAD_DIRECTION_LOCAL_Z = "LOAD_DIRECTION_LOCAL_Z"
    LOAD_DIRECTION_PRINCIPAL_U = "LOAD_DIRECTION_PRINCIPAL_U"
    LOAD_DIRECTION_PRINCIPAL_V = "LOAD_DIRECTION_PRINCIPAL_V"


class LineLoadDirection(str, Enum):
    '''
    Line Load Direction
    '''
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED = "LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED"
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE = "LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE"
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED = "LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED"
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE = "LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE"
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED = "LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED"
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE = "LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE"
    LOAD_DIRECTION_LOCAL_X = "LOAD_DIRECTION_LOCAL_X"
    LOAD_DIRECTION_LOCAL_Y = "LOAD_DIRECTION_LOCAL_Y"
    LOAD_DIRECTION_LOCAL_Z = "LOAD_DIRECTION_LOCAL_Z"


class MemberLoad(BaseModel):
    no: int = Field(1, description="Load Tag")
    load_case_no: int = Field(1, description="Assigned Load Case")
    members_no: str = Field('1', description="Assigned Members")
    load_direction: MemberLoadDirection = Field(MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE, description="Load Direction Enumeration")
    magnitude: float = Field(2000, description="Load Magnitude in N/m")
    comment: Optional[str] = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")

class NodalLoad(BaseModel):
    no: int = Field(1, description="Load Tag")
    load_case_no: int = Field(1, description="Assigned Load Case")
    nodes_no: str = Field('1', description="Assigned Nodes")
    load_direction: NodalLoadDirection = Field(NodalLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, description="Load Direction Enumeration")
    magnitude: float = Field(0.0, description="Force Magnitude in N")
    comment: Optional[str] = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")

class SurfaceLoad(BaseModel):
    no: int = Field(1, description="Load Tag")
    load_case_no: int = Field(1, description="Assigned Load Case")
    surface_no: str = Field('1', description="Assigned Surfaces")
    magnitude: float = Field(1000.0, description="Load Magnitude in N per square meter")
    comment: Optional[str] = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")

class LineLoad(BaseModel):
    no: int = Field(1, description="Load Tag")
    load_case_no: int = Field(1, description="Assigned Load Case")
    lines_no: str = Field('1', description="Assigned Line(s)")
    load_direction: LineLoadDirection = Field(LineLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE, description="Load Direction Enumeration")
    magnitude: float = Field(0.0, description="Magnitude of Line Load in N/m")
    comment: Optional[str] = Field('', description="Comments")
    params: Optional[Dict] = Field(None, description="Any WS Parameter relevant to the object")


class LoadDefinition(BaseModel):
    no: int = Field(..., description="Load Tag")
    load_case_no: int = Field(..., description="Assigned Load Case")
    load_type: LoadType = Field(..., description="Load Type (NODAL, MEMBER, SURFACE, LINE)")
    # Load Type specifics
    nodal_load: Optional[NodalLoad] = Field(None, description="Nodal Load Details")
    member_load: Optional[MemberLoad] = Field(None, description="Member Load Details")
    surface_load: Optional[SurfaceLoad] = Field(None, description="Surface Load Details")
    line_load: Optional[LineLoad] = Field(None, description="Line Load Details")
    magnitude: float = Field(..., description="Load Magnitude")
    applied_to: List[int] = Field(..., description="List of Member, Surface, Node or Line Tags the load applies to")
    comment: Optional[str] = Field("", description="Comments")

    @classmethod
    def create_nodal_load(cls, no: int, load_case_no: int, nodes_no: str, load_direction: NodalLoadDirection, magnitude: float, comment: Optional[str] = None, params: Optional[Dict] = None):
        return cls(no=no, load_case_no=load_case_no, load_type=LoadType.NODAL, nodal_load=NodalLoad(no=no, load_case_no=load_case_no, nodes_no=nodes_no, load_direction=load_direction, magnitude=magnitude, comment=comment, params=params), magnitude=magnitude, applied_to=[int(n) for n in nodes_no.split()], comment=comment)

    @classmethod
    def create_member_load(cls, no: int, load_case_no: int, members_no: str, load_direction: MemberLoadDirection, magnitude: float, comment: Optional[str] = None, params: Optional[Dict] = None):
         return cls(no=no, load_case_no=load_case_no, load_type=LoadType.MEMBER, member_load=MemberLoad(no=no, load_case_no=load_case_no, members_no=members_no, load_direction=load_direction, magnitude=magnitude, comment=comment, params=params), magnitude=magnitude, applied_to=[int(m) for m in members_no.split()], comment=comment)

    @classmethod
    def create_surface_load(cls, no: int, load_case_no: int, surface_no: str, magnitude: float, comment: Optional[str] = None, params: Optional[Dict] = None):
        return cls(no=no, load_case_no=load_case_no, load_type=LoadType.SURFACE, surface_load=SurfaceLoad(no=no, load_case_no=load_case_no, surface_no=surface_no, magnitude=magnitude, comment=comment, params=params), magnitude=magnitude, applied_to=[int(s) for s in surface_no.split()], comment=comment)

    @classmethod
    def create_line_load(cls, no: int, load_case_no: int, lines_no: str, load_direction: LineLoadDirection, magnitude: float, comment: Optional[str] = None, params: Optional[Dict] = None):
        return cls(no=no, load_case_no=load_case_no, load_type=LoadType.LINE, line_load=LineLoad(no=no, load_case_no=load_case_no, lines_no=lines_no, load_direction=load_direction, magnitude=magnitude, comment=comment, params=params), magnitude=magnitude, applied_to=[int(l) for l in lines_no.split()], comment=comment)


class RFEMTemplate(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    filename: str = Field(..., description="File name of the project")
    input_type: str = Field(..., description="Input modus of the project")
    materials: List[MaterialDefinition] = Field(..., description="Definition of all materials in this project")
    sections: Optional[List[SectionDefinition]] = Field(None, description="Definition of all cross sections in this project")
    thicknesses: List[ThicknessDefinition] = Field(..., description="Definition of all surface thicknesses in this project")
    nodes: Optional[List[NodeDefinition]] = Field(None, description="Definition of all nodes for modelling geometry or loading places in this project")
    lines: Optional[List[Line]] = Field(None, description="Definition of all lines needed for modelling geometry or loading places in this project")
    members: Optional[List[MemberDefinition]] = Field(None, description="Definition of all structural members in this project")
    surfaces: List[SurfaceDefinition] = Field(..., description="Definition of all surfaces in this project")
    supports: Optional[List[Union[NodalSupport, LineSupport]]] = Field(None, description="Definition of all support conditions in this project")
    loads: List[LoadDefinition] = Field(..., description="Definition of all acting loads on elements in this project")