import moderngl
import glm


class Renderable:

    def __init__(self,
                 ctx: moderngl.Context,
                 shader_library,
                 position=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1)):

        self.ctx = ctx
        self.shader_library = shader_library

        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.model_matrix = self.generate_model_matrix()
        self.vbo = None
        self.vao = None
        self.program = None

    def on_init(self):
        pass

    def update(self):
        pass

    def get_vertex_data(self):
        pass


    def render(self):
        self.update()
        self.vao.render()

    def render_shadow(self):
        pass

    def create_vao(self, program, vbo, format: str, attributes: list):
        vao = self.ctx.vertex_array(program, [(vbo, format, *attributes)], skip_errors=True)
        return vao

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


