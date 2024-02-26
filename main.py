from utilities import utils_io
from hand import Hand
from app import App


def main():

    animation_fpath = r"D:\git_repositories\alexandrepv\machine_learning_toolbox\manus_glove_viewer\animation_data\data.txt"
    animation = utils_io.load_data_in_terminal_format(txt_fpath=animation_fpath)

    config_fpath = r"D:\git_repositories\alexandrepv\machine_learning_toolbox\manus_glove_viewer\hand_config\default_hand.yaml"
    hand = Hand(config_fpath=config_fpath)

    app = App()
    app.run()


if __name__ == "__main__":
    main()
