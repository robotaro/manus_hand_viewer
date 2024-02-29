from src.renderables.renderable import Renderable
from src.mesh_factory import MeshFactory
import numpy as np


class Cylinder(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vbo = self.ctx.buffer(self.get_vertex_data().astype("f4").tobytes())

        self.format = "3f 3f 3f"
        self.attributes = ['in_position', 'in_normal', 'in_color']

    def get_vertex_data(self):

        factory = MeshFactory(use_triangle_normals=False)

        mesh_data = factory.create_cylinder(point_a=(0.0, 0.0, 0.0),
                                            point_b=(0.0, 1.0, 0.0),
                                            color=(0.5, 1.0, 0.2),
                                            radius=0.2,
                                            sections=16)

        return np.hstack([mesh_data["vertices"],
                          mesh_data["normals"],
                          mesh_data["colors"]])