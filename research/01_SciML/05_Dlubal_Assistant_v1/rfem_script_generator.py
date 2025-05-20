from models import *
from typing import List, Optional, Union

def generate_rfem_script(template: RFEMTemplate) -> str:
    """Generate RFEM Python script from a template."""
    is_member_structure = bool(template.members)
    is_surface_structure = bool(template.surfaces)

    script = f"""
import os
import sys
from RFEM.initModel import Model, Calculate_all
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.thickness import Thickness
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.surface import Surface
from RFEM.BasicObjects.line import Line
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Loads.nodalLoad import NodalLoad
from RFEM.Loads.lineLoad import LineLoad
from RFEM.Loads.surfaceLoad import SurfaceLoad
from RFEM.TypesForNodes.nodalSupport import NodalSupport, NodalSupportType
from RFEM.TypesForLines.lineSupport import LineSupport, LineSupportType
from RFEM.enums import NodalLoadDirection, MemberLoadDirection, LineLoadDirection


# Initialize model and start modifying
Model(model_name="{template.project_name}")
Model.clientModel.service.begin_modification()

# Define materials
{generate_materials(template.materials)}

# Define sections
{generate_sections(template.sections) if template.sections else '# No sections defined'}

# Define thicknesses
{generate_thicknesses(template.thicknesses) if template.thicknesses else '# No thicknesses defined'}

# Define nodes
{generate_nodes(template.nodes) if template.nodes else '# No nodes defined'}

# Define lines
{generate_lines(template.lines) if template.lines else '# No lines defined'}

# Define supports
{generate_supports(template.supports, template.lines, template.nodes, template.members, template.surfaces)}

# Define members
{generate_members(template.members) if template.members else '# No members defined'}

# Define surfaces
{generate_surfaces(template.surfaces) if template.surfaces else '# No surfaces defined'}

# Define loads
{generate_loads(template.loads) if template.loads else '# No loads defined'}

Model.clientModel.service.finish_modification()

print("Calculating results.")
Calculate_all()

"""
    return script

def generate_materials(materials: List[MaterialDefinition]) -> str:
    """Generate RFEM code for materials."""
    if not materials:
        return "# No materials defined"
    return "\n".join([f'Material({m.no}, "{m.name}")' for m in materials])

def generate_sections(sections: Optional[List[SectionDefinition]]) -> str:
    """Generate RFEM code for sections."""
    if not sections:
        return "# No sections defined"
    return "\n".join([f'Section({s.no}, "{s.name}", {s.material_no})' for s in sections])

def generate_thicknesses(thicknesses: List[ThicknessDefinition]) -> str:
    """Generate RFEM code for thicknesses."""
    if not thicknesses:
        return "# No thicknesses defined"
    return "\n".join([f'Thickness(no={t.no}, name="{t.name}", material_no={t.material_no}, uniform_thickness_d={t.uniform_thickness_d})' for t in thicknesses])

def generate_nodes(nodes: Optional[List[NodeDefinition]]) -> str:
    """Generate RFEM code for nodes."""
    if not nodes:
        return "# No nodes defined"
    return "\n".join([f'Node({n.no}, {n.coordinate_X}, {n.coordinate_Y}, {n.coordinate_Z})' for n in nodes])

def generate_lines(lines: Optional[List[Line]]) -> str:
    """Generate RFEM code for lines."""
    if not lines:
        return "# No lines defined"
    
    line_strings = []
    for line in lines:
        if line.type == LineType.TYPE_POLYLINE:
            line_strings.append(f'Line.Polyline(no={line.no}, nodes_no="{line.nodes_no}")')
        elif line.type == LineType.TYPE_ARC:
            nodes = line.nodes_no.split() if line.nodes_no else [line.arc_first_node, line.arc_second_node]
            line_strings.append(f'Line.Arc(no={line.no}, nodes_no={nodes}, control_point={line.control_point})')
        elif line.type == LineType.TYPE_CIRCLE:
            line_strings.append(f'Line.Circle(no={line.no}, center_of_circle={line.circle_center_coordinate}, ' +
                              f'circle_radius={line.circle_radius}, point_of_normal_to_circle_plane={line.point_of_normal_to_circle_plane})')
        elif line.type == LineType.TYPE_ELLIPTICAL_ARC:
            line_strings.append(f'Line.EllipticalArc(no={line.no}, p1_control_point={line.elliptical_arc_first_control_point}, ' +
                              f'p2_control_point={line.elliptical_arc_second_control_point}, ' +
                              f'p3_control_point={line.elliptical_arc_perimeter_control_point}, ' + 
                              f'arc_angle_alpha={line.arc_angle_alpha}, arc_angle_beta={line.arc_angle_beta})')
        elif line.type == LineType.TYPE_ELLIPSE:
            nodes = line.nodes_no.split() if line.nodes_no else [line.ellipse_first_node, line.ellipse_second_node]
            line_strings.append(f'Line.Ellipse(no={line.no}, nodes_no={nodes}, ellipse_control_point={line.ellipse_control_point})')
        elif line.type == LineType.TYPE_PARABOLA:
            nodes = line.nodes_no.split() if line.nodes_no else [line.parabola_first_node, line.parabola_second_node]
            line_strings.append(f'Line.Parabola(no={line.no}, nodes_no={nodes}, parabola_control_point={line.parabola_control_point}, ' +
                              f'parabola_alpha={line.parabola_alpha})')
        elif line.type == LineType.TYPE_SPLINE:
            line_strings.append(f'Line.Spline(no={line.no}, nodes_no="{line.nodes_no}")')
        elif line.type == LineType.TYPE_NURBS:
            line_strings.append(f'Line.NURBS(no={line.no}, nodes_no="{line.nodes_no}", control_points={line.control_points}, ' +
                              f'weights={line.weights}, order={line.order})')
    
    return "\n".join(line_strings)

def generate_supports(
    supports: Optional[List[Union[NodalSupport, LineSupport]]],
    lines: Optional[List[Line]],
    nodes: Optional[List[NodeDefinition]],
    members: Optional[List[MemberDefinition]],
    surfaces: List[SurfaceDefinition]
) -> str:
    """Generate RFEM code for supports based on available structure elements."""
    support_strings = []
    
    # If supports are explicitly provided, use them
    if supports:
        for support in supports:
            if isinstance(support, NodalSupport):
                support_strings.append(f'NodalSupport({support.no}, "{support.nodes_no}", NodalSupportType.{support.support})')
            elif isinstance(support, LineSupport):
                support_strings.append(f'LineSupport({support.no}, "{support.lines_no}", LineSupportType.{support.support_type})')
    # If no explicit supports, infer from structural elements
    elif members and nodes:
        # Apply appropriate supports based on structure type
        nodal_supports = infer_nodal_supports_from_members(members, nodes)
        support_strings.extend(nodal_supports)
    elif surfaces and lines:
        # Apply hinged line support to all boundary lines of surfaces
        line_supports = infer_line_supports_from_surfaces(surfaces)
        support_strings.extend(line_supports)
    elif nodes:
        # Apply default supports if only nodes are present
        for i, node in enumerate(nodes):
            if i == 0:  # First node is fixed
                support_strings.append(f'NodalSupport({node.no}, "{node.no}", NodalSupportType.FIXED)')
            else:  # Other nodes have appropriate supports
                support_strings.append(f'NodalSupport({node.no}, "{node.no}", NodalSupportType.HINGED)')

    return "\n".join(support_strings) if support_strings else "# No supports defined"

def infer_nodal_supports_from_members(members: List[MemberDefinition], nodes: List[NodeDefinition]) -> List[str]:
    """Infer nodal supports from member structure."""
    support_strings = []
    
    # Identify all unique nodes in members
    all_nodes = set()
    for member in members:
        all_nodes.add(member.start_node_no)
        all_nodes.add(member.end_node_no)
    
    # Determine which nodes need support (typically endpoints)
    for node_no in sorted(all_nodes):
        # Simple heuristic: first node is fixed, others are roller
        if node_no == min(all_nodes):
            support_strings.append(f'NodalSupport({node_no}, "{node_no}", NodalSupportType.FIXED)')
        else:
            support_strings.append(f'NodalSupport({node_no}, "{node_no}", NodalSupportType.ROLLER)')
    
    return support_strings

def infer_line_supports_from_surfaces(surfaces: List[SurfaceDefinition]) -> List[str]:
    """Infer line supports from surface structure."""
    support_strings = []
    used_lines = set()
    
    for surface in surfaces:
        for line_no in surface.boundary_lines:
            if line_no not in used_lines:
                support_strings.append(f'LineSupport({line_no}, "{line_no}", LineSupportType.HINGED)')
                used_lines.add(line_no)
    
    return support_strings

def generate_members(members: Optional[List[MemberDefinition]]) -> str:
    """Generate RFEM code for members."""
    if not members:
        return "# No members defined"
    
    member_strings = []
    for m in members:
        member_str = (f'Member(no={m.no}, start_node_no={m.start_node_no}, end_node_no={m.end_node_no}, ' +
                     f'rotation_angle={m.rotation_angle}, start_section_no={m.start_section_no}')
        
        # Add end section if different from start section
        if m.end_section_no != m.start_section_no:
            member_str += f', end_section_no={m.end_section_no}'
            
        # Add hinges if present
        if m.start_member_hinge_no:
            member_str += f', start_member_hinge_no={m.start_member_hinge_no}'
        if m.end_member_hinge_no:
            member_str += f', end_member_hinge_no={m.end_member_hinge_no}'
            
        # Add comment if present
        if m.comment:
            member_str += f', comment="{m.comment}"'
            
        member_str += ')'
        member_strings.append(member_str)
        
    return "\n".join(member_strings)

def generate_surfaces(surfaces: List[SurfaceDefinition]) -> str:
    """Generate RFEM code for surfaces."""
    if not surfaces:
        return "# No surfaces defined"
    
    surface_strings = []
    for s in surfaces:
        boundary_lines = ",".join(map(str, s.boundary_lines))
        surface_strings.append(f'Surface({s.no}, "{boundary_lines}", {s.thickness_no})')
        
    return "\n".join(surface_strings)

def generate_loads(loads: List[LoadDefinition]) -> str:
    """Generate RFEM code for loads."""
    if not loads:
        return "# No loads defined"
    
    # Extract all unique load cases
    load_cases = set(load.load_case_no for load in loads)
    load_case_str = "\n".join([f'LoadCase({lc})' for lc in sorted(load_cases)])
    
    # Generate load statements
    load_str = "\n".join([generate_load(load) for load in loads])
    
    return f"{load_case_str}\n{load_str}"

def generate_load(load: LoadDefinition) -> str:
    """Generate RFEM code for a specific load."""
    applied_to_str = ", ".join(map(str, load.applied_to))
    
    if load.load_type == LoadType.NODAL:
        return (f'NodalLoad(no={load.no}, load_case_no={load.load_case_no}, ' +
               f'nodes_no="{applied_to_str}", ' +
               f'load_direction=NodalLoadDirection.{load.nodal_load.load_direction.name}, ' +
               f'magnitude={load.magnitude})')
    
    elif load.load_type == LoadType.MEMBER:
        return (f'MemberLoad(no={load.no}, load_case_no={load.load_case_no}, ' +
               f'members_no="{applied_to_str}", ' +
               f'load_direction=MemberLoadDirection.{load.member_load.load_direction.name}, ' +
               f'magnitude={load.magnitude})')
    
    elif load.load_type == LoadType.SURFACE:
        return (f'SurfaceLoad(no={load.no}, load_case_no={load.load_case_no}, ' +
               f'surface_no="{applied_to_str}", magnitude={load.magnitude})')
    
    elif load.load_type == LoadType.LINE:
        return (f'LineLoad(no={load.no}, load_case_no={load.load_case_no}, ' +
               f'lines_no="{applied_to_str}", ' +
               f'load_direction=LineLoadDirection.{load.line_load.load_direction.name}, ' +
               f'magnitude={load.magnitude})')
    
    else:
        return f"# Unsupported load type: {load.load_type}"

def format_nodes_no(nodes_no: str) -> str:
    """Format nodes string with proper spacing."""
    return ' '.join(nodes_no.replace(',', ' ').split())
