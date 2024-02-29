from src.renderables.renderable import Renderable
from src.mesh_factory import MeshFactory
import numpy as np


class Cube(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vbo = self.ctx.buffer(self.get_vertex_data().astype("f4").tobytes())

        self.format = "3f 3f 3f"
        self.attributes = ['in_position', 'in_normal', 'in_color']

    def get_vertex_data(self):
        factory = MeshFactory()

        mesh_data = factory.create_box(width=self.params.get("width", 1.0),
                                       height=self.params.get("height", 1.0),
                                       depth=self.params.get("depth", 1.0),
                                       color=self.params.get("color", (0.85, 0.85, 0.85)),)

        return np.hstack([mesh_data["vertices"],
                          mesh_data["normals"],
                          mesh_data["colors"]])