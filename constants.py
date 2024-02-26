import logging
import os

# ===============================================================================
#                              Global
# ===============================================================================
ROOT_DIR = os.path.dirname(__file__)
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
CAMERA_SPEED = 0.005
CAMERA_SENSITIVITY = 0.04

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


# IO
TERMINAL_RE_PATTERN = (r"datetime\.datetime\((\d{4}, \d{1,2}, \d{1,2}, \d{1,2}, "
                       r"\d{1,2}, \d{1,2}, \d{1,6})\), \[([-\d\., ']+)\]")

FINGER_NAMES = [
    "thumb",
    "index",
    "middle",
    "ring",
    "pinky"
]

# Joint axis labels
THUMB_CMC_X = "thumb_cmc_x"
THUMB_CMC_Y = "thumb_cmc_y"
THUMB_MCP_X = "thumb_mcp_x"
THUMB_IP_X = "thumb_ip_x"

INDEX_MCP_X = "index_mcp_x"
INDEX_MCP_Y = "index_mcp_Y"
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

