from src.renderables.renderable import Renderable
from src import meshes_3d
import numpy as np


class Mesh(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_vertex_data(self):

        if "shape" not in self.params:
            raise Exception("[ERROR] Cannot create mesh: 'shape not specified")

        return meshes_3d.create_mesh(shape=self.params["shape"], params=self.params)

    def get_format_and_attributes(self) -> tuple:
        data_format = "3f 3f 3f"
        attributes = ['in_position', 'in_normal', 'in_color']
        return data_format, attributes


