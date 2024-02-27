import moderngl
import numpy as np
import glfw


def main():
    # Initialize glfw
    if not glfw.init():
        return

    # Setting up window hints for OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World Triangle", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Create a ModernGL context
    ctx = moderngl.create_context()

    # Triangle vertices: X, Y, R, G, B
    vertices = np.array([
        -0.6, -0.6, 1.0, 0.0, 0.0,  # Bottom left, Red
         0.6, -0.6, 0.0, 1.0, 0.0,  # Bottom right, Green
         0.0,  0.6, 0.0, 0.0, 1.0   # Top, Blue
    ], dtype='f4')

    # Vertex Buffer Object
    vbo = ctx.buffer(vertices.tobytes())

    # Vertex Array Object
    vao = ctx.vertex_array(
        ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            in vec3 in_color;
            out vec3 color;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                color = in_color;
            }
            """,
            fragment_shader="""
            #version 330
            in vec3 color;
            out vec4 fragColor;
            void main() {
                fragColor = vec4(color, 1.0);
            }
            """,
        ),
        vbo,
        'in_vert', 'in_color'
    )

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here
        ctx.clear(0.1, 0.2, 0.3)
        vao.render(moderngl.TRIANGLES)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
