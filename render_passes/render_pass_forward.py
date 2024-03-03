import moderngl
import glm

from render_passes.render_pass import RenderPass
from src.scene import Scene
from src.camera import Camera


class RenderPassForward(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.program_name = "forward"
        self.program = self.load_program(program_name=self.program_name)

    def render(self, camera: Camera, renderables: list, directional_light=None):

        # Prepare to render directly to the screen
        self.ctx.screen.use()

        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Only working with one light for now
        if directional_light:
            self.program['light.position'].write(directional_light.position)
            self.program['light.Ia'].write(directional_light.Ia)
            self.program['light.Id'].write(directional_light.Id)
            self.program['light.Is'].write(directional_light.Is)

        # Set shadow settings
        self.program['shadowMap'] = 1
        self.program['u_resolution'].write(glm.vec2((1280, 720)))

        # Set camera
        self.program['m_proj'].write(camera.projection_matrix)
        self.program['m_view'].write(camera.view_matrix)

        # Render objects
        for renderable in renderables:

            self.program['m_model'].write(renderable.world_matrix)
            renderable.render(program_name=self.program_name)


    