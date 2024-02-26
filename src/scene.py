import moderngl

from texture_library import TextureLibrary
from utilities import utils_io
from src.light import Light
from src.camera import Camera


class Scene:

    def __init__(self, ctx: moderngl.Context, texture_library: TextureLibrary):
        self.ctx = ctx
        self.light = Light()
        self.renderables = []

        self.texture_library = texture_library
        self.depth_texture = texture_library.textures["depth_texture"]
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

        # Flags
        self.left_hand = True
