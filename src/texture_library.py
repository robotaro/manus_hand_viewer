import moderngl
from PIL import Image
import os

import constants


class TextureLibrary:

    def __init__(self, ctx: moderngl.Context, window_size: tuple):

        self.ctx = ctx
        self.window_size = window_size

        self.textures = {
            "depth_texture": self.generate_depth_texture()
        }

    def generate_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.window_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []

        for face in faces:
            # Load the image using Pillow
            texture = Image.open(os.path.join(dir_path, f"{face}.{ext}"))

            # Apply the necessary flips
            if face in ['right', 'left', 'front', 'back']:
                texture = texture.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                # For 'top' and 'bottom', flip vertically
                texture = texture.transpose(Image.FLIP_TOP_BOTTOM)

            textures.append(texture)

        # Assuming all textures have the same size
        width, height = textures[0].size
        texture_cube = self.ctx.texture_cube(size=(width, height), components=3, data=None)

        for i, texture in enumerate(textures):
            # Convert the image to raw bytes in RGB format
            texture_data = texture.convert("RGB").tobytes()
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def load_texture(self, path):
        # Load the image using Pillow
        texture_image = Image.open(path)

        # Flip the image vertically
        texture_image = texture_image.transpose(Image.FLIP_TOP_BOTTOM)

        # Convert the Pillow image to raw bytes in RGB format
        texture_data = texture_image.convert("RGB").tobytes()

        # Assuming texture_image.size returns (width, height)
        texture = self.ctx.texture(size=texture_image.size, components=3, data=texture_data)

        # mipmaps
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic Filtering (AF) - adjust the value as needed or make it configurable
        texture.anisotropy = 32.0

        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]