import logging
import os
import numpy as np

# ===============================================================================
#                              Global
# ===============================================================================

# Default directories
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
SHADERS_DIR = os.path.join(ROOT_DIR, "shaders")
TEXTURES_DIR = os.path.join(ROOT_DIR, "textures")

# Logging
LOGGING_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# Camera variables
CAMERA_FOV = 50  # deg
CAMERA_NEAR = 0.1
CAMERA_FAR = 100
CAMERA_SPEED = 5.0
CAMERA_MOUSE_SENSITIVITY = 0.001
CAMERA_MIN_PITCH_RADIANS = -np.pi / 2.0 - 0.01
CAMERA_MAX_PITCH_RADIANS = np.pi / 2.0 - 0.01


# Mouse Input
MOUSE_LEFT = 0
MOUSE_RIGHT = 1
MOUSE_MIDDLE = 2
MOUSE_BUTTONS = (MOUSE_LEFT, MOUSE_RIGHT, MOUSE_MIDDLE)
MOUSE_POSITION = 'position'
MOUSE_POSITION_LAST_FRAME = 'position_last_frame'
MOUSE_SCROLL_POSITION = 'scroll_position'
MOUSE_SCROLL_POSITION_LAST_FRAME = 'scroll_position_last_frame'

BUTTON_PRESSED = 0
BUTTON_DOWN = 1
BUTTON_RELEASED = 2
BUTTON_UP = 3

# Keyboard
KEYBOARD_SIZE = 512
KEY_STATE_DOWN = 0
KEY_STATE_UP = 1
KEY_LEFT_CTRL = 29
KEY_LEFT_SHIFT = 42
KEY_LEFT_ALT = 56

# ===============================================================================
#                                  Hand
# ===============================================================================
TERMINAL_RE_PATTERN = (r"datetime\.datetime\((\d{4}, \d{1,2}, \d{1,2}, \d{1,2}, "
                       r"\d{1,2}, \d{1,2}, \d{1,6})\), \[([-\d\., ']+)\]")

FINGER_NAMES = [
    "thumb",
    "index",
    "middle",
    "ring",
    "pinky"
]

FINGER_JOINT_ORDER = ['cmc', 'mcp', 'ip', 'pip', 'dip', 'tip']

# Joint axis labels
THUMB_CMC_X = "thumb_cmc_x"
THUMB_CMC_Y = "thumb_cmc_y"
THUMB_MCP_X = "thumb_mcp_x"
THUMB_IP_X = "thumb_ip_x"

INDEX_MCP_X = "index_mcp_x"
INDEX_MCP_Y = "index_mcp_y"
INDEX_PIP_X = "index_pip_x"
INDEX_DIP_X = "index_dip_x"

MIDDLE_MCP_X = "middle_mcp_x"
MIDDLE_MCP_Y = "middle_mcp_y"
MIDDLE_PIP_X = "middle_pip_x"
MIDDLE_DIP_X = "middle_dip_x"

RING_MCP_X = "ring_mcp_x"
RING_MCP_Y = "ring_mcp_y"
RING_PIP_X = "ring_pip_x"
RING_DIP_X = "ring_dip_x"

PINKY_MCP_X = "pinky_mcp_x"
PINKY_MCP_Y = "pinky_mcp_y"
PINKY_PIP_X = "pinky_pip_x"
PINKY_DIP_X = "pinky_dip_x"

JOINT_NAMES = [
    THUMB_CMC_X,
    THUMB_CMC_Y,
    THUMB_MCP_X,
    THUMB_IP_X,
    INDEX_MCP_X,
    INDEX_MCP_Y,
    INDEX_PIP_X,
    INDEX_DIP_X,
    MIDDLE_MCP_X,
    MIDDLE_MCP_Y,
    MIDDLE_PIP_X,
    MIDDLE_DIP_X,
    RING_MCP_X,
    RING_MCP_Y,
    RING_PIP_X,
    RING_DIP_X,
    PINKY_MCP_X,
    PINKY_MCP_Y,
    PINKY_PIP_X,
    PINKY_DIP_X
]

RENDERABLES_PARENT_CHILD = [
    ("root", "thumb_cmc"),
    ("thumb_cmc", "thumb_mcp"),
    ("thumb_mcp", "thumb_ip"),
    ("thumb_ip", "thumb_tip"),

    ("root", "index_cmc"),
    ("index_cmc", "index_mcp"),
    ("index_mcp", "index_pip"),
    ("index_pip", "index_dip"),
    ("index_dip", "index_tip"),

    ("root", "middle_cmc"),
    ("middle_cmc", "middle_mcp"),
    ("middle_mcp", "middle_pip"),
    ("middle_pip", "middle_dip"),
    ("middle_dip", "middle_tip"),

    ("root", "ring_cmc"),
    ("ring_cmc", "ring_mcp"),
    ("ring_mcp", "ring_pip"),
    ("ring_pip", "ring_dip"),
    ("ring_dip", "ring_tip"),

    ("root", "pinky_cmc"),
    ("pinky_cmc", "pinky_mcp"),
    ("pinky_mcp", "pinky_pip"),
    ("pinky_pip", "pinky_dip"),
    ("pinky_dip", "pinky_tip"),
]