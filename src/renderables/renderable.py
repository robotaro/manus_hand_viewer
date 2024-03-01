import moderngl
import glm
import numpy as np


class Renderable:

    def __init__(self, ctx: moderngl.Context, params=None, children=None):

        self.ctx = ctx
        self.children = children if children is not None else []
        self.params = params if params is not None else {}

        mesh_data = self.get_vertex_data()
        concatenated_data = np.hstack([mesh_data["vertices"],
                                       mesh_data["normals"],
                                       mesh_data["colors"]])
        self.vbo = self.ctx.buffer(concatenated_data.astype("f4").tobytes())
        self.ibo_indices = self.ctx.buffer(mesh_data["indices"].astype("i4").tobytes())
        self.format, self.attributes = self.get_format_and_attributes()

        self.vaos = {}
        self.program = None
        self.render_mode = moderngl.TRIANGLES

        # Transform parameters
        self.position = glm.vec3(self.params.get("position", (0, 0, 0)))
        self.rotation = glm.vec3(self.params.get("rotation", (0, 0, 0)))
        self.scale = glm.vec3(self.params.get("scale", (1, 1, 1)))

        # Transforms
        self.local_matrix = self.calculate_model_matrix()
        self.world_matrix = self.local_matrix

    def update(self, parent=None):

        """
        Update all transforms recursively to the last child
        :param parent:
        :return:
        """

        self.local_matrix = self.calculate_model_matrix()

        if parent:
            self.world_matrix = parent.world_matrix * self.local_matrix
        else:
            self.world_matrix = self.local_matrix

        for child in self.children:
            child.update(parent=self)

    def get_vertex_data(self):
        pass

    def get_format_and_attributes(self) -> tuple:
        pass

    def render(self, program_name: str):
        self.vaos[program_name].render(self.render_mode)

    def render_shadow(self):
        pass

    def calculate_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def release(self):
        for _, vao in self.vaos.items():
            vao.release()
        if self.vbo:
            self.vbo.release()


