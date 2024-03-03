import glm

from render_passes.render_pass import RenderPass

from src.scene import Scene
from src.camera import Camera


class RenderPassShadow(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.program_name = "shadow_map"
        self.program = self.load_program(program_name=self.program_name)  # This is here for clarity

        self.shadow_texture_resolution = (1280, 720)
        self.depth_texture = self.ctx.depth_texture(self.shadow_texture_resolution)
        self.depth_texture.repeat_x = False
        self.depth_texture.repeat_y = False
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render(self, camera: Camera, renderables: list, directional_light=None):

        # Shadow pass
        self.depth_fbo.clear()
        self.depth_fbo.use()

        if directional_light:
            self.program['m_view_light'].write(directional_light.m_view_light)

        self.depth_texture.use(location=1)

        # Set Project for directional light
        self.program['m_proj'].write(camera.projection_matrix)

        for renderable in renderables:
            self.program['m_model'].write(renderable.world_matrix)
            renderable.render(program_name=self.program_name)




