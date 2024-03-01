from src.renderables.renderable import Renderable
from src import meshes_3d
import numpy as np


class Cylinder(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vbo = self.ctx.buffer(self.get_vertex_data().astype("f4").tobytes())

        self.format = "3f 3f 3f"
        self.attributes = ['in_position', 'in_normal', 'in_color']

    def get_vertex_data(self):

        mesh_data = meshes_3d.create_mesh(shape="cylinder", params=self.params)

        return np.hstack([mesh_data["vertices"],
                          mesh_data["normals"],
                          mesh_data["colors"]])
