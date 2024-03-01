import glm
import copy
from src.engine import Engine
from utilities import utils_io

from src import constants

HAND_SCALE = 50


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
        self.renderables = self.create_renderables()

        self.animation_timestamp = 0

        # Flags
        self.right_hand = True

    def create_renderables(self) -> dict:

        # Step 1) Create all blueprints
        blueprints = {}
        for (parent_key, child_key) in constants.RENDERABLES_PARENT_CHILD:

            if parent_key == "root":
                blueprints["root"] = {"position": glm.vec3(0, 0, 0)}
                continue

            finger_name, joint_name = parent_key.split("_")
            parent_joint = self.hand_config[finger_name][joint_name]
            finger_name, joint_name = child_key.split("_")
            child_joint = self.hand_config[finger_name][joint_name]

            parent_position = glm.vec3(parent_joint["position"]) * HAND_SCALE
            child_position = glm.vec3(child_joint["position"]) * HAND_SCALE  # relative position to parent
            bone_length = glm.length(child_position)
            bone_vector = child_position

            blueprints[parent_key] = {
                "position": parent_position,
                "bone_length": bone_length,
                "bone_vector": bone_vector
            }

        # Step 2) Create renderable based on blueprints
        renderables = {}
        for key, blueprint in blueprints.items():

            if key == "root":
                renderables[key] = self.engine.scene.create_renderable(
                    type_id="mesh",
                    params={"shape": "box",
                            "position": blueprint["position"],
                            "width": 0.5,
                            "height": 0.1,
                            "depth": 0.1,
                            "color": (0.0, 1.0, 1.0)})
                continue

            finger_name, joint_name = key.split("_")

            if joint_name == "mcp":
                renderables[key] = self.engine.scene.create_renderable(
                    type_id="finger_mcp_joint",
                    params={"position": blueprint["position"],
                            "bone_length": blueprint["bone_length"],
                            "bone_radius": 0.1,
                            "joint_radius": 0.15,
                            "color_bone": (0.1, 0.8, 0.0),
                            "color_joint": (0.1, 0.8, 0.0)})

                continue

            renderables[key] = self.engine.scene.create_renderable(
                type_id="mesh",
                params={"shape": "box",
                        "position": blueprint["position"],
                        "width": 0.1,
                        "height": 0.1,
                        "depth": 0.1,
                        "color": (1.0, 0.0, 0.0)})

        # Step 3) Connect renderables hierarchically
        for (parent_key, child_key) in constants.RENDERABLES_PARENT_CHILD:
            if child_key not in renderables:
                continue
            renderables[parent_key].children.append(renderables[child_key])

        # Step 4) Trigger update on all transforms so that their world matrices are validated
        renderables["root"].update()

        return renderables

    def create_fingers(self) -> dict:

        self.renderables["root"] = self.engine.scene.create_renderable(
            type_id="cube",
            params={"position": (0, 0, 0),
                    "width": 0.5,
                    "height": 0.1,
                    "depth": 0.1,
                    "color": (0.0, 1.0, 1.0)})

        fingers = {key: [] for key, _ in self.hand_config.items()}

        # Create renderables
        for finger_name, finger_blueprint in self.hand_config.items():

            previous_joint = None

            # Per Joint
            for index, joint_name in enumerate(constants.FINGER_JOINT_ORDER):

                current_joint = finger_blueprint.get(joint_name, None)
                if current_joint is None:
                    continue
                current_joint = copy.copy(current_joint)

                if joint_name == "mcp":
                    current_joint["renderable"] = self.engine.scene.create_renderable(
                        type_id="cube",
                        params={"position": current_joint["position"],
                                "width": 0.1,
                                "height": 0.1,
                                "depth": 0.1,
                                "color": (0.8, 0.0, 0.0)})

                if index == 0:
                    self.renderables["root"].children.append(current_joint["renderable"])
                    previous_renderable = current_joint["renderable"]
                    continue

                previous_renderable.children.append(current_joint["renderable"])
                previous_renderable = current_joint["renderable"]

        # Add hierarchy to renderables

        root.update()

    def update_animation(self, delta_time):
        pass

    def update_imgui(self):
        pass

