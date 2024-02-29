from src.renderables.renderable import Renderable
from src import meshes_3d
import numpy as np


class FingerMCPJoint(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vbo = self.ctx.buffer(self.get_vertex_data().astype("f4").tobytes())

        # Overwrite default values
        self.format = "3f 3f 3f"
        self.attributes = ['in_position', 'in_normal', 'in_color']

    def get_vertex_data(self):
        joint_radius = self.params.get("joint_radius", 0.1)
        bone_length = self.params.get("bone_length", 0.1)

        shape_blueprints = [
            {
                "shape": "cylinder",
                "point_a": (0, 0, 0),
                "point_b": (0, 0, bone_length),
                "radius": joint_radius * 0.8
            },
            {
                "shape": "create_icosphere",
                "radius": joint_radius
            },
        ]

        mesh_data = meshes_3d.create_composite_mesh(shape_blueprint_list=shape_blueprints)

        return np.hstack([mesh_data["vertices"],
                          mesh_data["normals"],
                          mesh_data["colors"]])
