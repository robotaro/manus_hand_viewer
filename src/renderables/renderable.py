import moderngl
import glm


class Renderable:

    def __init__(self,
                 ctx: moderngl.Context,
                 position=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1)):

        self.ctx = ctx
        self.vbo = None
        self.format = None
        self.attributes = None
        self.vaos = {}
        self.program = None

        # Transform parameters
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)

        # Transforms
        self.model_matrix = self.generate_model_matrix()

    def update(self):
        pass

    def get_vertex_data(self):
        pass

    def render(self, shader_name: str):
        self.update()

        #self.texture = self.app.mesh.texture.textures[self.tex_id]
        #self.program['u_texture_0'] = 0
        #self.texture.use(location=0)

        self.vaos[shader_name].render(moderngl.TRIANGLES)

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


