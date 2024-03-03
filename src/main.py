from utilities import utils_io
from hand import Hand
from engine import Engine
import os
import glm

import constants


def main():

    engine = Engine(vertical_sync=True)

    # Configure hand
    config_fpath = os.path.join(constants.CONFIG_DIR, "default_hand.yaml")
    animation_fpath = os.path.join(constants.DATA_DIR, "animation_1.txt")
    hand = Hand(engine=engine,
                hand_config_yaml_fpath=config_fpath,
                hand_animation_txt_fpath=animation_fpath)

    # And now you can run it :)
    engine.run()


if __name__ == "__main__":
    main()
