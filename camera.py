import glm
import glfw
import numpy as np

import constants


class Camera:
    def __init__(self, window_size: tuple, position=(0, 0, 4), yaw=-90, pitch=0):

        self.aspect_ratio = window_size[0] / window_size[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.delta_time = 0
        self.view_matrix = self.get_view_matrix()
        self.projection_matrix = self.get_projection_matrix()

        self.mouse_x_past = None
        self.mouse_y_past = None

    def update(self, delta_time: float):
        self.delta_time = delta_time
        self.update_camera_vectors()
        self.view_matrix = self.get_view_matrix()

    def move(self, keyboard_state: np.array):
        velocity = constants.CAMERA_SPEED * self.delta_time
        if keyboard_state[glfw.KEY_W]:
            self.position += self.forward * velocity
        if keyboard_state[glfw.KEY_S]:
            self.position -= self.forward * velocity
        if keyboard_state[glfw.KEY_A]:
            self.position -= self.right * velocity
        if keyboard_state[glfw.KEY_D]:
            self.position += self.right * velocity
        if keyboard_state[glfw.KEY_E]:
            self.position += self.up * velocity
        if keyboard_state[glfw.KEY_Q]:
            self.position -= self.up * velocity

    def rotate(self, mouse_x: float, mouse_y: float):

        if not self.mouse_x_past:
            self.mouse_x_past = mouse_x
        if not self.mouse_y_past:
            self.mouse_y_past = mouse_y

        dx = mouse_x - self.mouse_x_past
        self.mouse_x_past = mouse_x
        dy = mouse_y - self.mouse_y_past
        self.mouse_y_past = mouse_y

        self.yaw += dx * constants.CAMERA_SENSITIVITY
        self.pitch -= dy * constants.CAMERA_SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

        #print((mouse_x, mouse_y))
        #print((self.pitch, self.yaw))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(
            glm.radians(constants.CAMERA_FOV),
            self.aspect_ratio,
            constants.CAMERA_NEAR,
            constants.CAMERA_FAR)