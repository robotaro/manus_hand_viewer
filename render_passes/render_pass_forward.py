from render_passes.render_pass import RenderPass
from src.scene import Scene
from src.camera import Camera


class RenderPassForward(RenderPass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, scene: Scene, camera: Camera):

        # Prepare to render directly to the screen
        self.ctx.screen.use()

        # Set light
        self.program['light.position'].write(scene.light.position)
        self.program['light.Ia'].write(scene.light.Ia)
        self.program['light.Id'].write(scene.light.Id)
        self.program['light.Is'].write(scene.light.Is)

        # Set camera
        self.program['m_proj'].write(camera.projection_matrix)
        self.program['m_view'].write(camera.view_matrix)

        # Render objects
        for renderable in scene.renderables:
            self.program['m_model'].write(renderable.model_matrix)
            renderable.render(shader_name=self.render_pass_name)


    