import moderngl

from render_passes.render_pass import RenderPass
from src.scene import Scene
from src.camera import Camera


class RenderPassHelloWorld(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, camera: Camera, renderables: list):
        for renderable in renderables:
            renderable.vaos[self.program_name].render(moderngl.TRIANGLES)


    