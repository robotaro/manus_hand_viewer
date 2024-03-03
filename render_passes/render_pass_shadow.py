from render_passes.render_pass import RenderPass

from src.scene import Scene
from src.camera import Camera


class RenderPassShadow(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render(self, scene: Scene, camera: Camera, directional_lights=None):

        # Shadow pass
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for renderable in self.renderables:
            renderable.render_shadow()
        pass




