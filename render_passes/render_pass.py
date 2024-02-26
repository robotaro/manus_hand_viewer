import moderngl
import os

from src import constants
from src.scene import Scene
from src.camera import Camera
from src.texture_library import TextureLibrary


class RenderPass:

    def __init__(self, ctx: moderngl.Context, shader_program_name: str, texture_library: TextureLibrary):
        self.ctx = ctx
        self.render_pass_name = shader_program_name
        self.texture_library = texture_library
        self.program = self.load_program(shader_program_name=shader_program_name)

    def load_program(self, shader_program_name):
        fpath = os.path.join(constants.SHADERS_DIR, f"{shader_program_name}.vert")
        with open(fpath, "r") as file:
            vertex_shader = file.read()

        fpath = os.path.join(constants.SHADERS_DIR, f"{shader_program_name}.frag")
        with open(fpath, "r") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def render(self, scene: Scene, camera: Camera):
        pass
