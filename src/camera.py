import glm
import glfw
import imgui
import numpy as np

import constants


class Camera:

    def __init__(self, window_size: tuple, position=(6, 6, 6), target=(0, 1, 4)):

        self.aspect_ratio = window_size[0] / window_size[1]
        self.position = glm.vec3(position)
        self.target = glm.vec3(target)

        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)
        self.forward = glm.normalize(self.target - self.position)

        # Calculate yaw and pitch from the direction vector
        self.yaw = glm.atan(self.forward.z, self.forward.x)
        self.pitch = glm.asin(self.forward.y)

        # Ensure yaw is in the range of [-π, π]
        if self.yaw < -glm.pi():
            self.yaw += 2 * glm.pi()
        elif self.yaw > glm.pi():
            self.yaw -= 2 * glm.pi()

        self.view_matrix = self.calculate_view_matrix()
        self.projection_matrix = self.calculate_projection_matrix()

        self.mouse_rotation_enabled = False
        self.mouse_x_past = None
        self.mouse_y_past = None

    def update(self, keyboard_state: np.array, delta_time: float):

        velocity = constants.CAMERA_SPEED * delta_time
        if keyboard_state[glfw.KEY_W] == constants.KEY_STATE_DOWN:
            self.position += self.forward * velocity
        if keyboard_state[glfw.KEY_S] == constants.KEY_STATE_DOWN:
            self.position -= self.forward * velocity
        if keyboard_state[glfw.KEY_A] == constants.KEY_STATE_DOWN:
            self.position -= self.right * velocity
        if keyboard_state[glfw.KEY_D] == constants.KEY_STATE_DOWN:
            self.position += self.right * velocity
        if keyboard_state[glfw.KEY_E] == constants.KEY_STATE_DOWN:
            self.position += self.up * velocity
        if keyboard_state[glfw.KEY_Q] == constants.KEY_STATE_DOWN:
            self.position -= self.up * velocity

        self.update_camera_vectors()
        self.view_matrix = self.calculate_view_matrix()

    def rotate(self, mouse_x: float, mouse_y: float):

        if not self.mouse_x_past:
            self.mouse_x_past = mouse_x
        if not self.mouse_y_past:
            self.mouse_y_past = mouse_y

        dx = mouse_x - self.mouse_x_past
        self.mouse_x_past = mouse_x
        dy = mouse_y - self.mouse_y_past
        self.mouse_y_past = mouse_y

        if not self.mouse_rotation_enabled:
            return

        self.yaw += dx * constants.CAMERA_MOUSE_SENSITIVITY
        self.pitch -= dy * constants.CAMERA_MOUSE_SENSITIVITY
        self.pitch = np.clip(self.pitch,
                             a_min=constants.CAMERA_MIN_PITCH_RADIANS,
                             a_max=constants.CAMERA_MAX_PITCH_RADIANS)

    def update_camera_vectors(self):

        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def calculate_view_matrix(self):
        # TODO: I believe the lookAt function already returns the inverse transform. That's why it
        #       works as the view_matrix out-of-the-box
        return glm.lookAt(self.position,
                          self.position + self.forward,
                          self.up)

    def calculate_projection_matrix(self):
        return glm.perspective(
            glm.radians(constants.CAMERA_FOV),
            self.aspect_ratio,
            constants.CAMERA_NEAR,
            constants.CAMERA_FAR)

    def on_imgui(self):
        imgui.begin(f"Scene", True)

        imgui.text(f"Camera")
        _, new_position = imgui.drag_float3("Position", *self.position, 0.01)
        self.position = new_position
        _, self.yaw = imgui.drag_float("Yaw", self.yaw, 0.1)
        _, self.pitch = imgui.drag_float("Pitch", self.pitch, 0.1)
        imgui.spacing()

        # imgui.set_window_position(300, 150)
        #imgui.set_window_size(500, 500)

        # draw text label inside of current window
        imgui.end()