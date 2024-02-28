from utilities import utils_io
from hand import Hand
from app import App
import os

import constants


def main():

    animation_fpath = os.path.join(constants.DATA_DIR, "animation_1.txt")
    animation = utils_io.load_data_in_terminal_format(txt_fpath=animation_fpath)

    config_fpath = os.path.join(constants.CONFIG_DIR, "default_hand.yaml")
    hand = Hand(config_fpath=config_fpath)

    app = App()

    # Create render passes BEFORE adding the renderables
    app.scene.create_render_pass(type_id="forward", program_name="default_color")
    # self.scene.create_render_pass(type_id="hello_world", program_name="hello_world")

    dist = 1.0
    for i in range(10):
        for j in range(10):
            position = (i * dist - 5.0, 0.0, j * dist - 5.0)
            app.scene.create_renderable(type_id="cylinder",
                                        params={"position": position,
                                                })
    # self.scene.create_renderable(type_id="hello_triangle")

    app.run()


if __name__ == "__main__":
    main()
