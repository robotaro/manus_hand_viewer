from src.renderables.renderable import Renderable
import numpy as np


class HelloTriangle(Renderable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vbo = self.ctx.buffer(self.get_vertex_data().astype("f4").tobytes())
        self.format = '2f 3f'
        self.attributes = ['in_vert', 'in_color']

    def get_vertex_data(self):

        # Triangle vertices: X, Y, R, G, B
        return np.array([
            -0.6, -0.6, 1.0, 0.0, 0.0,  # Bottom left, Red
             0.6, -0.6, 0.0, 1.0, 0.0,  # Bottom right, Green
             0.0,  0.6, 0.0, 0.0, 1.0   # Top, Blue
        ], dtype='f4')
