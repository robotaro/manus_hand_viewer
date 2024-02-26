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
    app.run()


if __name__ == "__main__":
    main()
