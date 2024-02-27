import moderngl
import glm


class Renderable:

    def __init__(self, ctx: moderngl.Context, params=None):

        self.ctx = ctx
        self.vbo = None
        self.vaos = {}
        self.ibo = None
        self.format = None
        self.attributes = None
        self.program = None

        params = params if params is not None else {}

        # Transform parameters
        self.position = glm.vec3(params.get("position", (0, 0, 0)))
        self.rotation = glm.vec3(params.get("rotation", (0, 0, 0)))
        self.scale = glm.vec3(params.get("scale", (1, 1, 1)))

        # Transforms
        self.model_matrix = self.generate_model_matrix()

    def update(self):
        pass

    def get_vertex_data(self):
        pass

    def render(self, program_name: str):
        self.update()
        self.vaos[program_name].render(moderngl.TRIANGLES)

    def render_shadow(self):
        pass

    def generate_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def release(self):
        if self.vao:
            self.vao.release()
        if self.vbo:
            self.vbo.release()


