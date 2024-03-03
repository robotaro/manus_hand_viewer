import glfw
import moderngl
import time
import signal
import numpy as np
from typing import Callable
import inspect

import imgui
from imgui.integrations.glfw import GlfwRenderer

# Main components
import constants
from camera import Camera
from scene import Scene
from directional_light import DirectionalLight
from texture_library import TextureLibrary
from utilities import utils_logging

# Renderables
from src.renderables.mesh import Mesh
from src.renderables.chessboard_plane import ChessboardPlane
from src.renderables.hello_triangle import HelloTriangle
from src.renderables.finger_joint import FingerJoint

# Render passes
from render_passes.render_pass_forward import RenderPassForward
from render_passes.render_pass_shadow import RenderPassShadow
from render_passes.render_pass_hello_world import RenderPassHelloWorld


class Engine:

    def __init__(self,
                 window_title="Manus Hand Viewer",
                 window_size=(1280, 720),
                 vertical_sync=False,
                 log_level="info"):

        # Logging
        self.logger = utils_logging.get_logger()
        self.logger.setLevel(level=constants.LOGGING_MAP[log_level])

        # External callbacks
        self.external_update_callback = None
        self.external_imgui_callback = None

        if not glfw.init():
            raise ValueError("[ERROR] Failed to initialize GLFW")

        # Create GLFW window
        self.window_title = window_title
        self.window_size = window_size
        self.monitor_gltf = glfw.get_primary_monitor()
        self.window_glfw = glfw.create_window(width=self.window_size[0],
                                              height=self.window_size[1],
                                              title=self.window_title,
                                              monitor=None,
                                              share=None)
        if not self.window_glfw:
            glfw.terminate()
            raise Exception('[ERROR] Could not create GLFW window.')

        # Finish initialising GLFW context
        glfw.window_hint(glfw.SAMPLES, 4)  # TODO: Find out about samples hint before creating the window
        glfw.make_context_current(self.window_glfw)
        glfw.swap_interval(1 if vertical_sync else 0)

        # Assign window callback functions
        glfw.set_key_callback(self.window_glfw, self._glfw_callback_keyboard)
        glfw.set_char_callback(self.window_glfw, self._glfw_callback_char)
        glfw.set_cursor_pos_callback(self.window_glfw, self._glfw_callback_mouse_move)
        glfw.set_mouse_button_callback(self.window_glfw, self._glfw_callback_mouse_button)
        glfw.set_scroll_callback(self.window_glfw, self._glfw_callback_mouse_scroll)
        glfw.set_window_size_callback(self.window_glfw, self._glfw_callback_window_resize)
        glfw.set_framebuffer_size_callback(self.window_glfw, self._glfw_callback_framebuffer_size)
        glfw.set_drop_callback(self.window_glfw, self._glfw_callback_drop_files)

        # Create main moderngl Context
        self.ctx = moderngl.create_context()

        # Inputs
        self.mouse_state = self.initialise_mouse_state()
        self.keyboard_state = self.initialise_keyboard_state()

        # ImGUI
        imgui.create_context()
        self.imgui_renderer = GlfwRenderer(self.window_glfw, attach_callbacks=False)  # DISABLE attach_callbacks!!!!
        self.imgui_exit_popup_open = False

        # Internal Libraries
        self.texture_library = TextureLibrary(ctx=self.ctx, window_size=window_size)

        # Internal Components
        self.camera = Camera(window_size=window_size)
        self.scene = self.create_scene()

        # Add basic light
        self.scene.directional_light = DirectionalLight()

        # Flags
        self.close_application = False

        # Assign OS signal handling callback
        signal.signal(signal.SIGINT, self.callback_signal_handler)

    @staticmethod
    def initialise_mouse_state() -> dict:
        return {
            constants.MOUSE_LEFT: constants.BUTTON_UP,
            constants.MOUSE_RIGHT: constants.BUTTON_UP,
            constants.MOUSE_MIDDLE: constants.BUTTON_UP,
            constants.MOUSE_POSITION: (0, 0),
            constants.MOUSE_POSITION_LAST_FRAME: (0, 0),
            constants.MOUSE_SCROLL_POSITION: 0
        }

    @staticmethod
    def initialise_keyboard_state() -> np.array:
        return np.ones((constants.KEYBOARD_SIZE,), dtype=np.int8) * constants.KEY_STATE_UP

    def center_window_to_main_monitor(self):
        pos = glfw.get_monitor_pos(self.monitor_gltf)
        size = glfw.get_window_size(self.window_glfw)
        mode = glfw.get_video_mode(self.monitor_gltf)
        glfw.set_window_pos(
            self.window_glfw,
            int(pos[0] + (mode.size.width - size[0]) / 2),
            int(pos[1] + (mode.size.height - size[1]) / 2))

    def set_external_update_callback(self, callback_function: Callable):
        signature = inspect.signature(callback_function)
        parameters = signature.parameters.values()
        if len(parameters) == 1:
            self.external_update_callback = callback_function
        else:
            raise ValueError("Provided function must take exactly one argument (delta_time).")

    def set_external_imgui_callback(self, callback_function: Callable):
        signature = inspect.signature(callback_function)
        parameters = signature.parameters.values()
        if len(parameters) == 0:
            self.external_imgui_callback = callback_function
        else:
            raise ValueError("Provided function must take no arguments")

    def callback_signal_handler(self, signum, frame):
        self.logger.debug("Signal received : Closing editor now")
        self.close_application = True

    def imgui_start(self):
        self.imgui_renderer.process_inputs()
        imgui.get_io().ini_file_name = ""  # Disables creating an .ini file with the last window details
        imgui.new_frame()

    def imgui_stop(self):
        imgui.end_frame()
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def create_scene(self) -> Scene:
        new_scene = Scene(ctx=self.ctx, texture_library=self.texture_library)

        # Register Render Passes
        new_scene.register_render_pass(type_id="forward", render_pass_class=RenderPassForward)
        new_scene.register_render_pass(type_id="shadow", render_pass_class=RenderPassShadow)

        # Register Renderables
        new_scene.register_renderable(type_id="mesh", renderable_class=Mesh)
        new_scene.register_renderable(type_id="chessboard_plane", renderable_class=ChessboardPlane)
        new_scene.register_renderable(type_id="finger_joint", renderable_class=FingerJoint)

        # Add basic rendering passes (order matters!)
        new_scene.create_render_pass(type_id="shadow")
        new_scene.create_render_pass(type_id="forward")

        return new_scene

    def run(self):

        # Main loop
        self.close_application = False
        previous_time = time.perf_counter()
        while not glfw.window_should_close(self.window_glfw) and not self.close_application:

            # Clear framebuffer
            self.ctx.clear(color=(1.0, 1.0, 1.0))

            # Update all window events
            glfw.poll_events()

            current_time = time.perf_counter()
            delta_time = current_time - previous_time
            previous_time = current_time

            self.imgui_start()

            self.camera.update(delta_time=delta_time, keyboard_state=self.keyboard_state)

            if self.external_update_callback:
                self.external_update_callback(delta_time)

            self.scene.render(camera=self.camera)

            self.imgui_menu_bar()
            self.camera.on_imgui()
            if self.external_imgui_callback:
                self.external_imgui_callback()
            self.imgui_exit_modal()
            self.imgui_stop()

            glfw.swap_buffers(self.window_glfw)

        self.shutdown()

    # ========================================================================
    #                       GLFW Callback functions
    # ========================================================================

    def _glfw_callback_char(self, glfw_window, char):
        pass

    def _glfw_callback_keyboard(self, glfw_window, key, scancode, action, mods):

        # Updater internal keyboard states
        if action == glfw.PRESS:
            self.keyboard_state[key] = constants.KEY_STATE_DOWN

        if action == glfw.RELEASE:
            self.keyboard_state[key] = constants.KEY_STATE_UP

    def _glfw_callback_mouse_button(self, glfw_window, button, action, mods):

        if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_RIGHT:
            glfw.set_input_mode(self.window_glfw, glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.camera.mouse_rotation_enabled = True

        if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_RIGHT:
            glfw.set_input_mode(self.window_glfw, glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.camera.mouse_rotation_enabled = False

    def _glfw_callback_mouse_move(self, glfw_window, x, y):
        self.camera.rotate(mouse_x=x, mouse_y=y)

    def _glfw_callback_mouse_scroll(self, glfw_window, x_offset, y_offset):
        pass

    def _glfw_callback_window_resize(self, glfw_window, width, height):
        pass

    def _glfw_callback_framebuffer_size(self, glfw_window, width, height):
        pass

    def _glfw_callback_window_size(self, glfw_window, width, height):
        pass

    def _glfw_callback_drop_files(self, glfw_window, file_list):
        pass

    # ========================================================================
    #                            GUI Functions
    # ========================================================================

    def imgui_menu_bar(self):

        with imgui.begin_main_menu_bar() as main_menu_bar:

            # ========================[ File ]========================
            if imgui.begin_menu("File", True):

                # File -> Load
                clicked, selected = imgui.menu_item("Load Scene", None, False, True)

                # File -> Save
                clicked, selected = imgui.menu_item("Save Scene", None, False, True)

                imgui.separator()

                # File -> Quit
                clicked, selected = imgui.menu_item("Quit", "Ctrl + Q", False, True)
                if clicked:
                    self.imgui_exit_popup_open = True

                imgui.end_menu()

            # ========================[ Edit ]========================
            if imgui.begin_menu("Edit", True):
                if imgui.begin_menu("Light modes"):
                    _, default = imgui.menu_item("Default", None, True)

                    _, diffuse = imgui.menu_item("Diffuse", None, True)

                    imgui.end_menu()

                clicked, selected = imgui.menu_item("Preferences", "Ctrl + Q", False, True)

                imgui.end_menu()

    def imgui_exit_modal(self):

        if not self.imgui_exit_popup_open:
            return

        imgui.open_popup("Exit##exit-popup")

        if not imgui.begin_popup_modal("Exit##exit-popup", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)[0]:
            return

        imgui.text("Are you sure you want to exit?")
        imgui.spacing()

        # Draw a cancel and exit button on the same line using the available space
        button_width = (imgui.get_content_region_available()[0] - imgui.get_style().item_spacing[0]) * 0.5

        # Style the cancel with a grey color
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.5, 0.5, 0.5, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.6, 0.6, 0.6, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.7, 0.7, 0.7, 1.0)

        if imgui.button("cancel", width=button_width):
            imgui.close_current_popup()
            self.imgui_exit_popup_open = False

        imgui.pop_style_color()
        imgui.pop_style_color()
        imgui.pop_style_color()

        imgui.same_line()
        if imgui.button("exit", button_width):
            self.close_application = True

        imgui.end_popup()

    def shutdown(self):
        pass