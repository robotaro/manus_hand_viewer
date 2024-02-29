import numpy as np
from numba import njit, float32
from src import mat3

DEG2RAD = np.pi / 180.0


def compute_transform(position: tuple, rotation_rad: tuple, scale=1.0, order='xyz'):

    """
    #TODO: This is a SLOW implementation! Hard-code it if you are only going o use one rotation,
    #      and use Numba instead.

    Returns a 3x3 rotation matrix based on the angles and the rotation order
    :param x_rad: Angle in radians
    :param y_rad: Angle in radians
    :param z_rad: Angle in radians
    :param order: string with the order of axes
    :return: numpy ndarray (3, 3) <float32>
    """

    cx = np.cos(rotation_rad[0])
    sx = np.sin(rotation_rad[0])
    cy = np.cos(rotation_rad[1])
    sy = np.sin(rotation_rad[1])
    cz = np.cos(rotation_rad[2])
    sz = np.sin(rotation_rad[2])

    rx = np.asarray([[1, 0, 0],
                     [0, cx, -sx],
                     [0, sx, cx]], dtype=np.float32)
    ry = np.asarray([[cy, 0, sy],
                     [0, 1, 0],
                     [-sy, 0, cy]], dtype=np.float32)
    rz = np.asarray([[cz, -sz, 0],
                     [sz, cz, 0],
                     [0, 0, 1]], dtype=np.float32)

    rotation = np.eye(3, dtype=np.float32)

    for axis in order.lower():
        if axis == 'x':
            rotation = np.matmul(rotation, rx)
        elif axis == 'y':
            rotation = np.matmul(rotation, ry)
        else:
            rotation = np.matmul(rotation, rz)

    rotation *= scale

    transform = np.eye(4, dtype=np.float32)
    transform[:3, :3] = rotation
    transform[:3, 3] = position

    return transform


@njit(float32[:, :](float32[:], float32[:], float32[:]))
def create_transform_euler_xyz(position: np.array, rotation: np.array, scale: np.array):

    """
    Euler XYZ performs the rotation in the following order: R(z) @ R(y) @ R(x)
    :param position:
    :param rotation:
    :param scale:
    :return:
    """

    cx = np.cos(rotation[0])
    sx = np.sin(rotation[0])
    cy = np.cos(rotation[1])
    sy = np.sin(rotation[1])
    cz = np.cos(rotation[2])
    sz = np.sin(rotation[2])

    transform = np.eye(4, dtype=np.float32)

    # From wiki: https://en.wikipedia.org/wiki/Rotation_matrix
    transform[0, 0] = cy * cz * scale[0]
    transform[0, 1] = (sx * sy * cz - cx * sz) * scale[1]
    transform[0, 2] = (cx * sy * cz + sx * sz) * scale[2]

    transform[1, 0] = cy * sz * scale[0]
    transform[1, 1] = (sx * sy * sz + cx * cz) * scale[1]
    transform[1, 2] = (cx * sy * sz - sx * cz) * scale[2]

    transform[2, 0] = -sy * scale[0]
    transform[2, 1] = sx * cy * scale[1]
    transform[2, 2] = cx * cy * scale[2]

    transform[:3, 3] = position

    return transform


#@njit(float32[:](float32[:, :]), cache=True)
def to_euler_xyz(rotation_matrix) -> np.array:

    # Safety: Normalise matrix rotation first
    rotation_matrix[:, 0] /= np.linalg.norm(rotation_matrix[:, 0])
    rotation_matrix[:, 1] /= np.linalg.norm(rotation_matrix[:, 1])
    rotation_matrix[:, 2] /= np.linalg.norm(rotation_matrix[:, 2])

    ret = np.zeros((3,), dtype=np.float32)
    if np.abs(rotation_matrix[2, 0]) < 1.0:
        ret[1] = -np.arcsin(rotation_matrix[2, 0])
        c = 1.0 / np.cos(ret[1])
        ret[0] = np.arctan2(rotation_matrix[2, 1] * c, rotation_matrix[2, 2] * c)
        ret[2] = np.arctan2(rotation_matrix[1, 0] * c, rotation_matrix[0, 0] * c)
        return ret

    ret[2] = 0.0
    if not (rotation_matrix[2, 0] > -1.0):
        ret[0] = ret[2] + np.arctan2(rotation_matrix[0, 1], rotation_matrix[0, 2])
        ret[1] = np.pi / 2
        return ret

    ret[0] = -ret[2] + np.arctan2(-rotation_matrix[0, 1], -rotation_matrix[0, 2])
    ret[1] = -np.pi / 2

    return ret


@njit(cache=True)
def mul_vector3(in_mat4: np.ndarray, in_vec3: np.array) -> np.array:
    return np.dot(in_mat4[:3, :3], in_vec3) + in_mat4[:3, 3]


@njit(cache=True)
def mul_vectors3(in_mat4: np.ndarray, in_vec3_array: np.ndarray, out_vec3_array: np.ndarray):
    for i in range(in_vec3_array.shape[0]):
        out_vec3_array[i, :] = np.dot(in_mat4[:3, :3], in_vec3_array[i, :]) + in_mat4[:3, 3]


@njit(cache=True)
def mul_vectors3_rotation_only(in_mat4: np.ndarray, in_vec3_array: np.ndarray, out_vec3_array: np.ndarray):
    for i in range(in_vec3_array.shape[0]):
        out_vec3_array[i, :] = np.dot(in_mat4[:3, :3], in_vec3_array[i, :])


@njit(cache=True)
def fast_inverse(in_mat4: np.ndarray, out_mat4: np.ndarray):
    # IMPORTANT: This matrix assumes out_mat4 was already initialised as eye(4)!!!
    out_mat4[:3, :3] = np.linalg.inv(np.ascontiguousarray(in_mat4[:3, :3]))
    out_mat4[:3, 3] = -out_mat4[:3, :3] @ in_mat4[:3, 3]


@njit(cache=True)
def even_faster_inverse(in_mat4: np.ndarray, out_mat4: np.ndarray):
    # IMPORTANT: This matrix assumes out_mat4 was already initialised as eye(4)!!!
    out_mat4[:3, :3] = in_mat4[:3, :3].T  # R.T == R^-1
    out_mat4[:3, 3] = -out_mat4[:3, :3] @ in_mat4[:3, 3]


@njit(cache=True)
def compute_transform_not_so_useful(pos: tuple, rot: tuple, scale: float):
    # TODO: refactor this to simplify scale!

    rotation = np.eye(4)
    rotation[:3, :3] = np.array(rot)

    trans = np.eye(4)
    trans[:3, 3] = np.array(pos)

    scale = np.diag([scale, scale, scale, 1])

    return (trans @ rotation @ scale).astype("f4")


def create(position: np.array, rotation: mat3):

    mat = np.eye(4, dtype=np.float32)
    mat[:3, :3] = rotation
    mat[:3, 3] = position
    return mat

@njit
def normalize(x):
    return x / np.linalg.norm(x)


def look_at(position: np.array, target: np.array, up: np.array):

    direction = position - target

    rotation_mat = np.empty((3, 3), dtype=np.float32)
    mat3.look_at_direction(direction=direction, up_vector=up, output_mat3=rotation_mat)

    trans = np.eye(4)
    trans[:3, :3] = rotation_mat
    trans[:3, 3] = position

    return trans


def look_at_direction(position: np.array, direction: np.array, up: np.array):

    rotation_mat = np.empty((3, 3), dtype=np.float32)
    mat3.look_at_direction(direction=direction, up_vector=up, output_mat3=rotation_mat)

    transform = np.eye(4)
    transform[:3, :3] = rotation_mat
    transform[:3, 3] = position

    return transform


def look_at_inverse(position: np.array, target: np.array, up: np.array):
    """
    Create an affine transformation that locates the camera at `position`, s.t. it looks at `target`.
    :param position: The 3D position of the camera in world coordinates.
    :param target: The 3D target where the camera should look at in world coordinates.
    :param up: The vector that is considered to be up in world coordinates.
    :return: Returns the 4-by-4 affine transform that transforms a point in world space into the camera space, i.e.
      it returns the inverse of the camera's 6D pose matrix. Assumes right-multiplication, i.e. x' = [R|t] * x.
    """

    forward = normalize(position - target)  # forward actually points in the other direction than `target` is.
    right = normalize(np.cross(up, forward))
    camera_up = np.cross(forward, right)

    # We directly create the inverse matrix (i.e. world2cam) because this is typically how look-at is define.
    rot = np.eye(4)
    rot[0, :3] = right
    rot[1, :3] = camera_up
    rot[2, :3] = forward

    trans = np.eye(4)
    trans[:3, 3] = -position

    return rot @ trans


#@njit(cache=True)
def perspective_projection(fovy_rad: float, aspect: float, near: float, far: float):

    """
    Calculates the 4x4 perspective matrix

    :param fovy_rad: Vertical view angle in radians
    :param aspect: aspect ratio of the screen (width / height)
    :param near: Closest point that can be rendered inside the view frustum
    :param far: Furthest point that can be render inside the view frustum
    :return: numpy ndarray (4, 4) <float32>
    """

    s = 1.0 / np.tan(fovy_rad)
    sx, sy = s / aspect, s
    zz = (far + near) / (near - far)
    zw = 2 * far * near / (near - far)
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, zz, zw],
                     [0, 0, -1, 0]], dtype=np.float32)


def orthographic_projection(left: float32, right: float32, bottom: float32, top: float32, near: float32, far: float32):
    dx = right - left
    dy = top - bottom
    dz = far - near
    rx = -(right + left) / (right - left)
    ry = -(top + bottom) / (top - bottom)
    rz = -(far + near) / (far - near)
    return np.array([[2.0 / dx, 0, 0, rx],
                     [0, 2.0 / dy, 0, ry],
                     [0, 0, -2.0 / dz, rz],
                     [0, 0, 0, 1]], dtype=np.float32)
