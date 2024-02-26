from utilities import utils_io


class Hand:

    def __init__(self, config_fpath: str):
        self.hand_config = utils_io.load_hand_configuration(yaml_fpath=config_fpath)
        self.left_hand = True

