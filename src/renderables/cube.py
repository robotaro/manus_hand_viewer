from src.renderables.renderable import Renderable
from src.mesh_factory import MeshFactory
import numpy as np


class Cube(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vertex_data = self.get_vertex_data(scale=self.params.get("scale", 1.0))
        self.vbo = self.ctx.buffer(vertex_data.astype("f4").tobytes())

        self.format = "3f 3f"
        self.attributes = ['in_position', 'in_normal']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self, scale=1.0):
        vertices = [(-scale, -scale, scale),
                    (scale, -scale, scale),
                    (scale, scale, scale),
                    (-scale, scale, scale),
                    (-scale, scale, -scale),
                    (-scale, -scale, -scale),
                    (scale, -scale, -scale),
                    (scale, scale, -scale)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([vertex_data, normals])
        return vertex_data