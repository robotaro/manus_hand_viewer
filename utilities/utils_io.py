import numpy as np
import pandas as pd
from datetime import datetime
import yaml
import re

import constants


def load_data_in_terminal_format(txt_fpath: str):

    with open(txt_fpath, "r") as file:

        lines = [line for line in file.readlines() if len(line.replace("\n", "")) > 0]
        timestamps = []
        hand_poses = []

        for line in lines:
            match = re.search(constants.TERMINAL_RE_PATTERN, line)
            if not match:
                continue

            # Timestamp
            datetime_part = match.group(1)
            year, month, day, hour, minute, second, microsecond = map(int, datetime_part.split(", "))
            dt = datetime(year, month, day, hour, minute, second, microsecond)
            timestamps.append(dt.timestamp())

            # Joint values
            joint_values_str = match.group(2).replace(",", "").replace("'", "").split(" ")
            hand_poses.append([float(value_str) for value_str in joint_values_str])

        timestamps_array = np.array(timestamps, dtype=np.float32).reshape(-1, 1)
        hand_poses_array = np.array(hand_poses, dtype=np.float32)

        columns = ["timestamps"] + constants.JOINT_NAMES
        data = np.concatenate([timestamps_array, hand_poses_array], axis=1)
        return pd.DataFrame(columns=columns, data=data)


def load_hand_configuration(yaml_fpath: str):
    with open(yaml_fpath) as file:
        return yaml.safe_load(file)
