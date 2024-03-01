from src.renderables.renderable import Renderable
from src import meshes_3d
import numpy as np


class FingerMCPJoint(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_vertex_data(self):

        color_bone = self.params.get("color_bone", (0.85, 0.85, 0.85))
        color_joint = self.params.get("color_bone", (0, 0.85, 0))
        joint_radius = self.params.get("joint_radius", 0.1)
        bone_length = self.params.get("bone_length", 0.1)

        shape_blueprints = [
            {
                # Bone
                "shape": "cylinder",
                "point_a": (0, 0, 0),
                "point_b": (0, 0, bone_length),
                "radius": joint_radius * 0.8,
                "color_bone": color_bone,
                "color_joint": color_joint
            },
            {
                "shape": "icosphere",
                "radius": joint_radius,

            },
        ]

        return meshes_3d.create_composite_mesh(shape_blueprint_list=shape_blueprints)

    def get_format_and_attributes(self) -> tuple:
        data_format = "3f 3f 3f"
        attributes = ['in_position', 'in_normal', 'in_color']
        return data_format, attributes
