import moderngl
import glfw
import numpy as np
import glm
from PIL import Image

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Configure GLFW window
window = glfw.create_window(640, 480, "Rotating Blue Cube with Light", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)

# Initialize ModernGL
ctx = moderngl.create_context()

# Define vertex shader
vertex_shader = '''
    #version 330
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    in vec3 in_vert;
    in vec3 in_norm;
    out vec3 v_norm;
    out vec3 v_vert;
    void main() {
        gl_Position = projection * view * model * vec4(in_vert, 1.0);
        v_vert = in_vert;
        v_norm = in_norm;
    }
'''

# Define fragment shader
fragment_shader = '''
    #version 330
    uniform vec3 light;
    in vec3 v_norm;
    in vec3 v_vert;
    out vec4 f_color;
    void main() {
        float lum = dot(normalize(light - v_vert), normalize(v_norm));
        lum = acos(lum) / 3.14159265;
        lum = clamp(lum, 0.0, 1.0);
        f_color = vec4(0.0, 0.0, lum + 0.3, 1.0); // Blue cube with lighting
    }
'''

# Define cube vertices and normals
vertices = np.array([
    -0.5, -0.5, -0.5, 0, 0, -1,
    0.5, -0.5, -0.5, 0, 0, -1,
    0.5, 0.5, -0.5, 0, 0, -1,
    -0.5, 0.5, -0.5, 0, 0, -1,
    -0.5, -0.5, 0.5, 0, 0, 1,
    0.5, -0.5, 0.5, 0, 0, 1,
    0.5, 0.5, 0.5, 0, 0, 1,
    -0.5, 0.5, 0.5, 0, 0, 1,
    # More vertices needed for a complete cube...
], dtype='f4')

# Define indices for cube faces
indices = np.array([
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    # More indices needed for a complete cube...
], dtype='i4')

# Create vertex array object
prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
vbo = ctx.buffer(vertices.tobytes())
ibo = ctx.buffer(indices.tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_norm', index_buffer=ibo)

# Uniforms for transformation and lighting
proj = glm.perspective(glm.radians(45.0), 640 / 480, 0.1, 100.0)
view = glm.lookAt(
    glm.vec3(3, 3, 3),  # Camera position
    glm.vec3(0, 0, 0),  # Target position
    glm.vec3(0, 0, 1),  # Up vector
)
prog['projection'].write(np.ascontiguousarray(proj, dtype=np.float32))
prog['view'].write(np.ascontiguousarray(view, dtype=np.float32))


# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    ctx.clear(0.9, 0.9, 0.9)
    ctx.enable(moderngl.DEPTH_TEST)

    rotate = glm.rotate(glm.mat4(1), glm.radians(glfw.get_time() * 50), glm.vec3(1, 1, 1))
    prog['model'].write(np.ascontiguousarray(rotate, dtype=np.float32))
    prog['light'].value = (1, 1, 1)

    vao.render(moderngl.TRIANGLES)

    glfw.swap_buffers(window)

# Terminate GLFW
glfw.terminate()