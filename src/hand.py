import glm
from src.engine import Engine
from utilities import utils_io

from src import constants


class Hand:

    def __init__(self,
                 engine: Engine,
                 hand_config_yaml_fpath: str,
                 hand_animation_txt_fpath: str):

        self.engine = engine
        self.engine.set_external_update_callback(self.update_animation)
        self.engine.set_external_imgui_callback(self.update_imgui)

        self.hand_config = utils_io.load_hand_configuration(yaml_fpath=hand_config_yaml_fpath)
        self.hand_animation = utils_io.load_data_in_terminal_format(txt_fpath=hand_animation_txt_fpath)

        self.renderables = {}

        self.animation_timestamp = 0

        # Flags
        self.right_hand = True

        self.create_renderable_hand()

    def create_renderable_hand(self):

        root = self.engine.scene.create_renderable(
            type_id="cube",
            params={"position": (0, 0, 0),
                    "width": 0.1,
                    "height": 0.1,
                    "depth": 0.1,
                    "color": (0.0, 1.0, 1.0)})

        for finger_name, finger in self.hand_config.items():

            previous_renderable = None
            for index, joint_name in enumerate(constants.FINGER_JOINT_ORDER):

                if joint_name not in finger:
                    continue

                joint_params = finger[joint_name]
                position = glm.vec3(joint_params["position"]) * 50
                new_renderable = self.engine.scene.create_renderable(
                    type_id="cube",
                    params={"position": position,
                            "width": 0.1,
                            "height": 0.1,
                            "depth": 0.1,
                            "color": (0.8, 0.0, 0.0)})

                # Store this renderable for animating it later
                renderable_id = f"{finger_name}_{joint_name}"
                self.renderables[renderable_id] = new_renderable

                if index == 0:
                    root.children.append(new_renderable)
                    previous_renderable = new_renderable
                    continue

                previous_renderable.children.append(new_renderable)
                previous_renderable = new_renderable
        root.update()

    def update_animation(self, delta_time):
        pass

    def update_imgui(self):
        pass

