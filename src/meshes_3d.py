import numpy as np
import trimesh

from src import mat4

KEY_SHAPE = "shape"
KEY_COLOR = "color"
KEY_RADIUS = "radius"
KEY_LENGTH = "length"
KEY_HEIGHT = "height"
KEY_WIDTH = "width"
KEY_SECTIONS = "sections"
KEY_SEGMENTS = "segments"
KEY_SUBDIVISIONS = "subdivisions"
KEY_DEPTH = "depth"
KEY_POINT_A = "point_a"
KEY_POINT_B = "point_b"
KEY_TRANSFORM = "transform"

KEY_PRIMITIVE_VERTICES = "vertices"
KEY_PRIMITIVE_NORMALS = "normals"
KEY_PRIMITIVE_UVS = "uvs"
KEY_PRIMITIVE_COLORS = "colors"
KEY_PRIMITIVE_INDICES = "indices"

KEY_SHAPE_CYLINDER = "cylinder"
KEY_SHAPE_BOX = "box"
KEY_SHAPE_CONE = "cone"
KEY_SHAPE_ICOSPHERE = "icosphere"
KEY_SHAPE_CAPSULE = "capsule"

DEFAULT_RADIUS = 0.5
DEFAULT_HEIGHT = 1.0
DEFAULT_COLOR = (1.0, 1.0, 1.0)
DEFAULT_CYLINDER_SECTIONS = 16  # Pie wedges
DEFAULT_CYLINDER_SEGMENTS = 1
DEFAULT_SUBDIVISIONS = 2


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

        shape = shape_blueprint.get(KEY_SHAPE, None)
        params = {key: value for key, value in shape_blueprint.items() if key != KEY_SHAPE}

        if shape is None:
            raise ValueError(f"[ERROR] Shape blueprint does not have a '{KEY_SHAPE}' field")

        mesh_data = create_mesh(shape=shape, params=params)

        vertices_list.append(mesh_data["vertices"])
        normals_list.append(mesh_data["normals"])
        colors_list.append(mesh_data["colors"])

        mesh_data["indices"] += total_num_vertices
        indices_list.append(mesh_data["indices"])
        total_num_vertices += mesh_data["vertices"].shape[0]

    # And Assemble final mesh here
    return {
        KEY_PRIMITIVE_VERTICES: np.concatenate(vertices_list, axis=0),
        KEY_PRIMITIVE_NORMALS: np.concatenate(normals_list, axis=0),
        KEY_PRIMITIVE_COLORS: np.concatenate(colors_list, axis=0),
        KEY_PRIMITIVE_INDICES: np.concatenate(indices_list, axis=0)
    }


def create_mesh(shape: str, params: dict) -> dict:

    vertices = None
    normals = None
    indices = None

    if shape == KEY_SHAPE_CYLINDER:

        point_a = params.get(KEY_POINT_A, (0, 0, 0))
        point_b = params.get(KEY_POINT_B, (0, 0, DEFAULT_HEIGHT))
        radius = params.get(KEY_RADIUS, DEFAULT_RADIUS)
        sections = params.get(KEY_SECTIONS, DEFAULT_CYLINDER_SECTIONS)
        primitive = trimesh.creation.cylinder(segment=(point_a, point_b),
                                              radius=radius,
                                              sections=sections)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == KEY_SHAPE_BOX:

        width = params.get(KEY_WIDTH, 1.0)
        height = params.get(KEY_HEIGHT, 1.0)
        depth = params.get(KEY_DEPTH, 1.0)
        primitive = trimesh.creation.box(extents=(width, height, depth))
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == KEY_SHAPE_CONE:
        radius = params.get(KEY_RADIUS, 0.5)
        height = params.get(KEY_HEIGHT, 0.5)
        segments = params.get(KEY_SECTIONS, 32)
        primitive = trimesh.creation.cone(radius=radius, height=height, sections=segments)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == KEY_SHAPE_ICOSPHERE:
        radius = params.get(KEY_RADIUS, DEFAULT_RADIUS)
        subdivisions = params.get(KEY_SUBDIVISIONS, DEFAULT_SUBDIVISIONS)
        primitive = trimesh.creation.icosphere(radius=radius, subdivisions=subdivisions)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    elif shape == KEY_SHAPE_CAPSULE:
        radius = params.get(KEY_RADIUS, 0.25)
        height = params.get(KEY_HEIGHT, 1.0)
        segments = params.get(KEY_SEGMENTS, 16)
        primitive = trimesh.creation.capsule(height=height, radius=radius, count=segments)
        vertices = np.array(primitive.vertices).astype('f4')
        normals = np.array(primitive.vertex_normals).astype('f4')
        indices = np.array(primitive.faces).astype('i4')

    else:
        raise Exception(f"[ERROR] Shape '{shape}' not supported")

    color = params.get("color", DEFAULT_COLOR)
    transform = params.get("transform", np.eye(4, dtype=np.float32))

    # Apply transform to both vertices and normals
    mat4.mul_vectors3(transform, vertices, vertices)
    mat4.mul_vectors3_rotation_only(transform, normals, normals)

    # All vertices receive the same color
    colors = np.tile(np.array(color, dtype=np.float32), (vertices.shape[0], 1))

    return {
        KEY_PRIMITIVE_VERTICES: vertices,
        KEY_PRIMITIVE_NORMALS: normals,
        KEY_PRIMITIVE_COLORS: colors,
        KEY_PRIMITIVE_INDICES: indices
    }


def convert_faces_to_triangles(vertices, uvs, faces):
    """
    From ChatGPT: This function takes the input vertices and UVs that share common vertex normals and
    recreate a list of triangles with unique normals for each vertex. UVs are also modified+ to follow
    the same logic
    """

    # Calculate flat normals for each face
    face_normals = np.cross(vertices[faces[:, 1]] - vertices[faces[:, 0]],
                            vertices[faces[:, 2]] - vertices[faces[:, 0]])
    face_normals /= np.linalg.norm(face_normals, axis=1)[:, np.newaxis]

    # Initialize arrays for the new vertices, normals, and UVs
    new_vertices = []
    new_normals = []
    new_uvs = []

    # Iterate through each face and populate the new arrays
    for i in range(len(faces)):
        face = faces[i]
        face_normal = face_normals[i]

        for vertex_idx in face:
            new_vertices.append(vertices[vertex_idx])
            new_normals.append(face_normal)
            if uvs is not None and len(uvs) > 0:
                new_uvs.append(uvs[vertex_idx])

    # Convert the lists to NumPy arrays
    new_vertices = np.array(new_vertices, dtype=np.float32)
    new_normals = np.array(new_normals, dtype=np.float32)
    new_uvs = np.array(new_uvs, dtype=np.float32)

    return new_vertices, new_normals, new_uvs