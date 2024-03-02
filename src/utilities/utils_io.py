import numpy as np
import pandas as pd
from datetime import datetime
import yaml
import re

from src import constants


def load_hand_animation(txt_fpath: str, use_uniform_timestamps=True, ):

    """
    This function is specific tailored to parse a terminal dump txt file. This recording contains errors.
    - Fix 1) Timestamps are in bursts, so they need to be smoothed out
    - Fix 2) Thumb joints finger joints are reversed

    :param txt_fpath:
    :param use_uniform_timestamps:
    :return:
    """

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

        timestamps_array = np.array(timestamps, dtype=float).reshape(-1, 1)
        timestamps_array -= timestamps_array[0]  # Time starts from zero

        if use_uniform_timestamps:
            # Replaces all timestamps with a linearly spaced version of them
            duration = np.max(timestamps_array)
            timestamps_array = np.linspace(start=0,
                                           stop=duration,
                                           num=timestamps_array.size,
                                           endpoint=True).reshape(-1, 1)

        hand_poses_array = np.array(hand_poses, dtype=float)

        columns = ["timestamps"] + constants.JOINT_NAMES
        data = np.concatenate([timestamps_array, hand_poses_array], axis=1)
        df = pd.DataFrame(columns=columns, data=data)

        # Fix finger MCP joint swaps

        # Fix thumb


        # Fix joints
        #df["index_mcp_x"], df["index_mcp_y"] = df["index_mcp_y"], df["index_mcp_x"]

        return df


def load_hand_configuration(yaml_fpath: str):
    with open(yaml_fpath) as file:
        return yaml.safe_load(file)
