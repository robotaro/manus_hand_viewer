import moderngl

from texture_library import TextureLibrary
from utilities import utils_io


class Scene:

    def __init__(self, ctx: moderngl.Context, texture_library: TextureLibrary):
        self.ctx = ctx
        self.light = None
        self.camera = None
        self.renderables = []

        self.texture_library = texture_library
        self.depth_texture = texture_library.textures["depth_texture"]
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

        # Flags
        self.left_hand = True

    def render(self):

        # Shadow pass
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for renderable in self.renderables:
            renderable.render_shadow()

        # Forward pass
        self.ctx.screen.use()


        for renderable in self.renderables:
            renderable.render()
        #self.scene.skybox.render()


