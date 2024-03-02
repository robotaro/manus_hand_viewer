from src import constants
import numpy as np

from src.renderables.renderable import Renderable
from src import meshes_3d


class ChessboardPlane(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_vertex_data(self):

        color_light = self.params.get("color_light", (0.95, 0.95, 0.95))
        color_dark = self.params.get("color_dark", (0.35, 0.35, 0.35))
        plane_axes = self.params.get("plane_axes", "xz")
        plane_size = self.params.get("plane_size", 10.0)
        num_squares = self.params.get("num_squares", 10)

        # Axis vectors based on the chosen plane
        if plane_axes == "xz":
            normal = np.array([0, 1, 0], dtype=np.float32)
            v1 = np.array([1, 0, 0], dtype=np.float32)
            v2 = np.array([0, 0, 1], dtype=np.float32)
        elif plane_axes == "xy":
            normal = np.array([0, 0, 1], dtype=np.float32)
            v1 = np.array([1, 0, 0], dtype=np.float32)
            v2 = np.array([0, 1, 0], dtype=np.float32)
        else:  # "yz"
            normal = np.array([1, 0, 0], dtype=np.float32)
            v1 = np.array([0, 1, 0], dtype=np.float32)
            v2 = np.array([0, 0, 1], dtype=np.float32)

        square_size = plane_size / num_squares

        vertices = []
        normals = []
        colors = []
        indices = []

        for i in range(num_squares):
            for j in range(num_squares):
                # Calculate the bottom left corner of the current square
                corner = (i * v1 + j * v2) * square_size - np.array([plane_size / 2, 0, plane_size / 2]) * np.array(
                    [v1, normal, v2]).sum(axis=0)
                square_vertices = [
                    corner,
                    corner + v2 * square_size,
                    corner + v1 * square_size,
                    corner + v1 * square_size + v2 * square_size
                ]

                # Choose color based on the square's position
                square_color = color_light if (i + j) % 2 == 0 else color_dark

                # Add vertices and colors for two triangles per square
                vertices.extend(square_vertices)
                colors.extend([square_color] * 4)  # Same color for all vertices in the square
                normals.extend([normal] * 4)

                # Calculate indices (two triangles per square)
                base_index = 4 * (i * num_squares + j)
                indices.extend(
                    [base_index, base_index + 1, base_index + 2, base_index + 2, base_index + 1, base_index + 3])

        vertices = np.array(vertices, dtype=np.float32).reshape(-1, 3)
        normals = np.array(normals, dtype=np.float32).reshape(-1, 3)
        colors = np.array(colors, dtype=np.float32).reshape(-1, 3)
        indices = np.array(indices, dtype=np.uint32)

        return {
            constants.KEY_PRIMITIVE_VERTICES: vertices,
            constants.KEY_PRIMITIVE_NORMALS: normals,
            constants.KEY_PRIMITIVE_COLORS: colors,
            constants.KEY_PRIMITIVE_INDICES: indices
        }

    def get_format_and_attributes(self) -> tuple:
        data_format = "3f 3f 3f"
        attributes = ['in_position', 'in_normal', 'in_color']
        return data_format, attributes


