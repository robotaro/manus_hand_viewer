from src.renderables.renderable import Renderable
from src import meshes_3d
import numpy as np


class FingerJoint(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_vertex_data(self):

        bone_radius = self.params.get("bone_radius", 0.1)
        joint_radius = self.params.get("joint_radius", 0.1)
        bone_length = self.params.get("bone_length", 0.1)
        joint_type = self.params.get("joint_type", "xy")

        # Select joint type based on the number of axes
        if joint_type == "x":
            joint_blueprint = {
                "shape": "cylinder",
                "point_a": (-bone_radius * 1.25, 0, 0),
                "point_b": (bone_radius * 1.25, 0, 0),
                "radius": joint_radius,
                "segments": 32,
                "color": (0.9, 0, 0)
            }

        elif joint_type == "y":
            joint_blueprint = {
                "shape": "cylinder",
                "point_a": (0, -bone_radius * 1.1, 0),
                "point_b": (0, bone_radius * 1.1, 0),
                "radius": joint_radius,
                "segments": 32,
                "color": (0, 0.9, 0)
            }

        elif joint_type == "xy":
            joint_blueprint = {
                "shape": "icosphere",
                "radius": joint_radius,
                "subdivisions": 3,
                "color": (0.3, 0.5, 0.9)
            }

        else:
            raise Exception(f"[ERROR] Joint type '{joint_type}' not suported")

        # Select bone type based on whether or not it is a the tip of the finger
        bone_blueprint = {
            "shape": "cylinder",
            "point_a": (0, 0, 0),
            "point_b": (0, 0, bone_length),
            "radius": bone_radius,
            "color": (0.85, 0.85, 0.85)
        }

        shape_blueprints = [
            joint_blueprint,
            bone_blueprint
        ]

        return meshes_3d.create_composite_mesh(shape_blueprint_list=shape_blueprints)

    def get_format_and_attributes(self) -> tuple:
        data_format = "3f 3f 3f"
        attributes = ['in_position', 'in_normal', 'in_color']
        return data_format, attributes
