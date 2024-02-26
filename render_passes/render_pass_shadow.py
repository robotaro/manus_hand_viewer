from render_passes.render_pass import RenderPass

from src.scene import Scene
from src.camera import Camera


class RenderPassShadow(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, scene: Scene, camera: Camera):

        # Shadow pass
        """self.depth_fbo.clear()
        self.depth_fbo.use()
        for renderable in self.renderables:
            renderable.render_shadow()"""
        pass




