import numpy as np
import trimesh
from src import constants

from src import mat4


def create_composite_mesh(shape_blueprint_list: list):

    """
    Input should be a list of dictionaries describing the shape
    :param shape_blueprint_list:
    :return:
    """

    vertices_list = []
    normals_list = []
    colors_list = []
    indices_list = []
    total_num_vertices = 0

    for blueprint_index, shape_blueprint in enumerate(shape_blueprint_list):

        shape = shape_blueprint.get(constants.KEY_SHAPE, None)
        params = {key: value for key, value in shape_blueprint.items() if key != constants.KEY_SHAPE}

        if shape is None:
            raise ValueError(f"[ERROR] Shape blueprint does not have a '{constants.KEY_SHAPE}' field")

        mesh_data = create_mesh(shape=shape, params=params)

        vertices_list.append(mesh_data["vertices"])
        normals_list.append(mesh_data["normals"])
        colors_list.append(mesh_data["colors"])

        mesh_data["indices"] += total_num_vertices
        indices_list.append(mesh_data["indices"])
        total_num_vertices += mesh_data["vertices"].shape[0]

    # And Assemble final mesh here
    return {
        constants.KEY_PRIMITIVE_VERTICES: np.concatenate(vertices_list, axis=0),
        constants.KEY_PRIMITIVE_NORMALS: np.concatenate(normals_list, axis=0),
        constants.KEY_PRIMITIVE_COLORS: np.concatenate(colors_list, axis=0),
        constants.KEY_PRIMITIVE_INDICES: np.concatenate(indices_list, axis=0)
    }


def create_mesh(shape: str, params: dict) -> dict:

    vertices = None
    normals = None
    indices = None

    if shape == constants.KEY_SHAPE_CYLINDER:

        point_a = params.get(constants.KEY_POINT_A, (0, 0, 0))
        point_b = params.get(constants.KEY_POINT_B, (0, 0, constants.DEFAULT_HEIGHT))
        radius = params.get(constants.KEY_RADIUS, constants.DEFAULT_RADIUS)
        sections = params.get(constants.KEY_SECTIONS, constants.DEFAULT_CYLINDER_SECTIONS)

        #vertices, normals, indices = generate_cylinder_mesh(point_a, point_b, radius, sections)
        primitive = trimesh.creation.cylinder(segment=(point_a, point_b),
                                              radius=radius,
                                              sections=sections)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == constants.KEY_SHAPE_BOX:
        width = params.get(constants.KEY_WIDTH, 1.0)
        height = params.get(constants.KEY_HEIGHT, 1.0)
        depth = params.get(constants.KEY_DEPTH, 1.0)
        vertices, normals, indices = generate_box_mesh(width=width, height=height, depth=depth)

    elif shape == constants.KEY_SHAPE_CONE:
        radius = params.get(constants.KEY_RADIUS, 0.5)
        height = params.get(constants.KEY_HEIGHT, 0.5)
        segments = params.get(constants.KEY_SECTIONS, 32)
        primitive = trimesh.creation.cone(radius=radius, height=height, sections=segments)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == constants.KEY_SHAPE_ICOSPHERE:
        radius = params.get(constants.KEY_RADIUS, constants.DEFAULT_RADIUS)
        subdivisions = params.get(constants.KEY_SUBDIVISIONS, constants.DEFAULT_SUBDIVISIONS)
        primitive = trimesh.creation.icosphere(radius=radius, subdivisions=subdivisions)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == constants.KEY_SHAPE_CAPSULE:
        radius = params.get(constants.KEY_RADIUS, 0.25)
        height = params.get(constants.KEY_HEIGHT, 1.0)
        segments = params.get(constants.KEY_SEGMENTS, 16)
        primitive = trimesh.creation.capsule(height=height, radius=radius, count=segments)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    else:
        raise Exception(f"[ERROR] Shape '{shape}' not supported")

    color = params.get(constants.KEY_COLOR, constants.DEFAULT_COLOR)
    transform = params.get("transform", np.eye(4, dtype=np.float32))

    # Apply transform to both vertices and normals
    mat4.mul_vectors3(transform, vertices, vertices)
    mat4.mul_vectors3_rotation_only(transform, normals, normals)

    # All vertices receive the same color
    colors = np.tile(np.array(color, dtype=np.float32), (vertices.shape[0], 1))

    return {
        constants.KEY_PRIMITIVE_VERTICES: vertices,
        constants.KEY_PRIMITIVE_NORMALS: normals,
        constants.KEY_PRIMITIVE_COLORS: colors,
        constants.KEY_PRIMITIVE_INDICES: indices
    }

def generate_box_mesh(width: float, height: float, depth: float):
    vertices = np.array([
        # Back face
        [-0.5, -0.5, -0.5],  [0.5, 0.5, -0.5], [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5],
        # Front face
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5],
        [-0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
        # Bottom face
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5, 0.5],
        [-0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5],
        # Top face
        [-0.5, 0.5, -0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5],
        # Left face
        [-0.5, -0.5, -0.5], [-0.5, 0.5, 0.5],[-0.5, 0.5, -0.5],
        [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5],
        # Right face
        [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5],
        [0.5, -0.5, -0.5], [0.5, 0.5, 0.5], [0.5, -0.5, 0.5],
    ], dtype='f4')

    vertices *= np.array([width, height, depth], dtype='f4')

    # Normals for each triangle, duplicated per vertex
    normals = np.array([
        # Back face
        [0, 0, -1], [0, 0, -1], [0, 0, -1],
        [0, 0, -1], [0, 0, -1], [0, 0, -1],
        # Front face
        [0, 0, 1], [0, 0, 1], [0, 0, 1],
        [0, 0, 1], [0, 0, 1], [0, 0, 1],
        # Bottom face
        [0, -1, 0], [0, -1, 0], [0, -1, 0],
        [0, -1, 0], [0, -1, 0], [0, -1, 0],
        # Top face
        [0, 1, 0], [0, 1, 0], [0, 1, 0],
        [0, 1, 0], [0, 1, 0], [0, 1, 0],
        # Left face
        [-1, 0, 0], [-1, 0, 0], [-1, 0, 0],
        [-1, 0, 0], [-1, 0, 0], [-1, 0, 0],
        # Right face
        [1, 0, 0], [1, 0, 0], [1, 0, 0],
        [1, 0, 0], [1, 0, 0], [1, 0, 0],
    ], dtype='f4')

    # Indices for each triangle, since vertices are now unique per triangle, we just go sequentially
    indices = np.array([
        i for i in range(36)
    ], dtype='i4')

    return vertices, normals, indices


def generate_cylinder_mesh(point_a, point_b, radius, num_sections):
    # Calculate directional vector and length between points
    dir_vector = np.array(point_b) - np.array(point_a)
    length = np.linalg.norm(dir_vector)
    cylinder_axis = dir_vector / length

    # Create a rotation matrix that aligns the z-axis to the cylinder axis
    z_axis = np.array([0, 0, 1])
    axis = np.cross(z_axis, cylinder_axis)
    axis_length = np.linalg.norm(axis)
    if axis_length != 0:
        axis /= axis_length
        angle = np.arccos(np.dot(z_axis, cylinder_axis))
        K = np.array([[0, -axis[2], axis[1]],
                      [axis[2], 0, -axis[0]],
                      [-axis[1], axis[0], 0]])
        rotation_matrix = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
    else:
        rotation_matrix = np.eye(3) if np.dot(z_axis, cylinder_axis) > 0 else np.eye(3) * np.array([1, 1, -1])

    # Generate circle points
    angle_step = 2 * np.pi / num_sections
    circle_points = np.array([
        [np.cos(i * angle_step) * radius, np.sin(i * angle_step) * radius, 0] for i in range(num_sections)
    ])

    # Rotate circle points and translate to create top and bottom vertices
    bottom_vertices = np.dot(circle_points, rotation_matrix.T) + point_a
    top_vertices = np.dot(circle_points, rotation_matrix.T) + point_b

    # Side vertices: duplicate for separate normals
    vertices = np.vstack((bottom_vertices, top_vertices, bottom_vertices, top_vertices))

    # Normals
    bottom_normals = np.tile([0, 0, -1], (num_sections, 1))
    top_normals = np.tile([0, 0, 1], (num_sections, 1))
    side_normals = np.vstack((
        np.dot(circle_points[:, :3], rotation_matrix.T)[:, :3],
        np.dot(circle_points[:, :3], rotation_matrix.T)[:, :3]
    ))
    normals = np.vstack((np.dot(bottom_normals, rotation_matrix.T),
                         np.dot(top_normals, rotation_matrix.T),
                         side_normals))

    # Indices
    indices = []
    for i in range(num_sections):
        next_i = (i + 1) % num_sections
        # Sides - corrected to reference the duplicated vertices correctly
        base_index_for_sides = 2 * num_sections  # Starting index for the side vertices

        # Each side face is defined by two triangles, hence four indices are involved: i, next_i, i + num_sections, next_i + num_sections
        # First triangle
        indices.append([base_index_for_sides + i,
                        base_index_for_sides + next_i,
                        base_index_for_sides + num_sections + i])
        # Second triangle
        indices.append([base_index_for_sides + next_i,
                        base_index_for_sides + num_sections + next_i,
                        base_index_for_sides + num_sections + i])

    center_bottom_index = len(vertices) - 2
    center_top_index = len(vertices) - 1

    # Top Lid
    for i in range(num_sections):
        next_i = (i + 1) % num_sections
        indices.append([num_sections + i,
                        num_sections + next_i,
                        center_top_index])

    # Bottom lid
    for i in range(num_sections):
        next_i = (i + 1) % num_sections
        indices.append([next_i, i, center_bottom_index])

    return np.array(vertices, dtype='f4'), np.array(normals, dtype='f4'), np.array(indices, dtype='i4')
