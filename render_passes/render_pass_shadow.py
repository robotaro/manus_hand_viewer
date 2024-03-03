from render_passes.render_pass import RenderPass

from src.scene import Scene
from src.camera import Camera


class RenderPassShadow(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.depth_texture = self.ctx.depth_texture((2048, 2048))
        self.depth_texture.repeat_x = False
        self.depth_texture.repeat_y = False
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render(self, camera: Camera, renderables: list, directional_light=None):

        # Shadow pass
        self.depth_fbo.clear()
        self.depth_fbo.use()

        for renderable in renderables:
            renderable.render_shadow()




