import moderngl


class ShaderLibrary:

    PROGRAM_LIST = [
        "default",
        "skybox",
        "advanced_skybox",
        "shadow_map"]

    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.programs = {program_name: self.load_program(program_name)
                         for program_name in ShaderLibrary.PROGRAM_LIST}

    def load_program(self, shader_program_name):
        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader,
                                   fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
