import moderngl

from render_passes.render_pass import RenderPass
from src.scene import Scene
from src.camera import Camera


class RenderPassForward(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, camera: Camera, renderables: list, directional_lights=None):

        directional_lights = directional_lights if directional_lights is not None else []

        # Prepare to render directly to the screen
        self.ctx.screen.use()

        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Only working with one light for now
        if len(directional_lights) > 0:
            self.program['light.position'].write(directional_lights[0].position)
            self.program['light.Ia'].write(directional_lights[0].Ia)
            self.program['light.Id'].write(directional_lights[0].Id)
            self.program['light.Is'].write(directional_lights[0].Is)

        # Set camera
        self.program['m_proj'].write(camera.projection_matrix)
        self.program['m_view'].write(camera.view_matrix)

        # Render objects
        for renderable in renderables:

            self.program['m_model'].write(renderable.world_matrix)
            renderable.render(program_name=self.program_name)


    