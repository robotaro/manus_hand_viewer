import glm
import imgui
import numpy as np
from src.engine import Engine
from utilities import utils_io
import matplotlib.pyplot as plt

from src import constants

HAND_SCALE = 35


class Hand:

    def __init__(self,
                 engine: Engine,
                 hand_config_yaml_fpath: str,
                 hand_animation_txt_fpath: str):

        self.engine = engine
        self.engine.set_external_update_callback(self.on_update)
        self.engine.set_external_imgui_callback(self.on_imgui)

        self.hand_config = utils_io.load_hand_configuration(yaml_fpath=hand_config_yaml_fpath)
        self.hand_animation = utils_io.load_hand_animation(txt_fpath=hand_animation_txt_fpath)

        #self.renderables = self.create_renderables()
        self.renderables = self.create_demo_renderables()

        self.timestamps = self.hand_animation["timestamps"].values
        self.joint_values = self.hand_animation.iloc[:, 1:].values
        self.animation_duration = self.timestamps[-1]

        #plt.plot(self.timestamps, self.joint_values, '-o')
        #plt.show()

        self.time_dilation_factor = 0.25
        self.play_animation = False
        self.playback_timestamp = 0
        self.lower_index = 0

        # Flags
        self.right_hand = True

    def create_demo_renderables(self):

        renderables = {}

        renderables["cube"] = self.engine.scene.create_renderable(
            type_id="mesh",
            params={"shape": "box",
                    "position": (0, 2, 0),
                    "width": 1,
                    "height": 1,
                    "depth": 1,
                    "color": (1.0, 0.0, 0.0)})

        renderables["floor"] = self.engine.scene.create_renderable(
            type_id="chessboard_plane",
            params={
                "position": (0, 0, 0),
                "plane_size": 100,
                "num_squares": 10
            })

        return renderables

    def create_renderables(self) -> dict:

        # Step 1) Create all joint blueprints
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

            if joint_name == "mcp" and finger_name != "thumb":
                renderables[key] = self.engine.scene.create_renderable(
                    type_id="finger_joint",
                    params={"position": blueprint["position"],
                            "bone_length": blueprint["bone_length"],
                            "bone_radius": 0.1,
                            "joint_radius": 0.2,
                            "joint_type": "xy"})

                continue

            if finger_name == "thumb":
                if joint_name == "cmc":
                    renderables[key] = self.engine.scene.create_renderable(
                        type_id="finger_joint",
                        params={"position": blueprint["position"],
                                "bone_length": blueprint["bone_length"],
                                "bone_radius": 0.1,
                                "joint_radius": 0.2,
                                "joint_type": "xy"})
                    continue

                renderables[key] = self.engine.scene.create_renderable(
                    type_id="finger_joint",
                    params={"position": blueprint["position"],
                            "bone_length": blueprint["bone_length"],
                            "bone_radius": 0.1,
                            "joint_radius": 0.2,
                            "joint_color": (0.2, 0.8, 0.2),
                            "joint_type": "x"})
                continue

            if joint_name in ["pip", "dip", "ip"]:
                renderables[key] = self.engine.scene.create_renderable(
                    type_id="finger_joint",
                    params={"position": blueprint["position"],
                            "bone_length": blueprint["bone_length"],
                            "bone_radius": 0.1,
                            "joint_radius": 0.2,
                            "joint_type": "x"})
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

        # Step 5) Add any other enviromental meshes necessary for rendering
        self.engine.scene.create_renderable(
            type_id="chessboard_plane",
            params={
                "position": (0, -4, 0),
                "plane_size": 100,
                "num_squares": 10
            })

        return renderables

    def on_update(self, delta_time):

        if self.play_animation:
            self.playback_timestamp += delta_time * self.time_dilation_factor
            if self.playback_timestamp > self.animation_duration:
                self.playback_timestamp = 0.0

        self.update_hand_joints_from_animation(query_timestamp=self.playback_timestamp)

        if "root" in self.renderables:
            self.renderables["root"].update()

    def on_imgui(self):

        imgui.begin(f"Hand Animation", True)

        _, self.playback_timestamp = imgui.slider_float("Timestamp",
                                                        self.playback_timestamp,
                                                        0.0,
                                                        self.animation_duration,
                                                        "%.3f")
        imgui.text(f"Index: {self.lower_index}")
        _, self.play_animation = imgui.checkbox("Play animation", self.play_animation)
        imgui.end()

    def update_hand_joints_from_animation(self, query_timestamp: float):

        self.lower_index = self.get_lower_index(query_timestamp=query_timestamp)

        lower_index = self.lower_index
        joint_values = self.joint_values[lower_index, :]

        for renderable_name, renderable in self.renderables.items():

            if renderable_name == "root":
                continue

            matched_axes = [(column_index - 1, key) for column_index, key in enumerate(self.hand_animation.keys()) if key.startswith(renderable_name)]

            for (column_index, matched_axis) in matched_axes:
                angle = np.radians(joint_values[column_index])
                if matched_axis.endswith("x"):
                    renderable.rotation.x = angle
                elif matched_axis.endswith("y"):
                    renderable.rotation.y = angle
                elif matched_axis.endswith("z"):
                    renderable.rotation.z = angle

    def get_lower_index(self, query_timestamp: float) -> int:

        # Find indices for interpolation
        lower_values_mask = self.timestamps <= query_timestamp
        index = int(np.sum(lower_values_mask))

        return np.minimum(index, self.timestamps.size -1 )