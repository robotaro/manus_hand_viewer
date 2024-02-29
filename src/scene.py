import moderngl

from texture_library import TextureLibrary
from utilities import utils_io
from src.light import Light
from src.camera import Camera


class Scene:

    def __init__(self, ctx: moderngl.Context, texture_library: TextureLibrary):

        self.ctx = ctx

        self.registered_render_passes = {}
        self.registered_renderables = {}

        self.render_passes = []
        self.renderables = []

        self.point_lights = []
        self.directional_lights = []

        self.texture_library = texture_library
        self.depth_texture = texture_library.textures["depth_texture"]
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def register_render_pass(self, type_id: str, render_pass_class):
        if type_id in self.registered_render_passes:
            raise KeyError(f"[ERROR] RenderPass '{type_id}' already registered")
        self.registered_render_passes[type_id] = render_pass_class

    def register_renderable(self, type_id: str, renderable_class):
        if type_id in self.registered_renderables:
            raise KeyError(f"[ERROR] Renderable '{type_id}' already registered")
        self.registered_renderables[type_id] = renderable_class

    def create_renderable(self, type_id: str, params=None):
        params = params if params is not None else {}
        new_renderable = self.registered_renderables[type_id](ctx=self.ctx, params=params)

        # Each renderable gets a VAO per render pass. It's how it works with ModernGL
        for render_pass in self.render_passes:
            new_renderable.vaos[render_pass.program_name] = self.ctx.vertex_array(
                render_pass.program,
                # TODO: You can change this list to individual VBOs!
                [(new_renderable.vbo, new_renderable.format, *new_renderable.attributes)],
                new_renderable.ibo,
                skip_errors=True)

        self.renderables.append(new_renderable)
        return new_renderable

    def create_render_pass(self, type_id: str, program_name: str):
        new_render_pass = self.registered_render_passes[type_id](
            ctx=self.ctx,
            program_name=program_name,
            texture_library=self.texture_library)
        self.render_passes.append(new_render_pass)
        return new_render_pass

    def render(self, camera: Camera):

        for render_pass in self.render_passes:
            render_pass.render(
                camera=camera,
                renderables=self.renderables,
                directional_lights=self.directional_lights)
