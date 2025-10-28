from .material import Material


class ShaderMaterial(Material):
    def __init__(self, vertex_shader="", fragment_shader="", name="ShaderMaterial"):
        super().__init__(name)
        self.type = "ShaderMaterial"
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.uniforms = {}
        self.defines = {}
        self.extensions = {}

    def set_uniform(self, name, value):
        self.uniforms[name] = value
        return self

    def get_uniform(self, name):
        return self.uniforms.get(name)

    def set_define(self, name, value):
        self.defines[name] = value
        return self

    def clone(self):
        new_mat = ShaderMaterial(self.vertex_shader, self.fragment_shader, self.name)
        new_mat.opacity = self.opacity
        new_mat.transparent = self.transparent
        new_mat.side = self.side
        new_mat.depth_test = self.depth_test
        new_mat.depth_write = self.depth_write
        new_mat.wireframe = self.wireframe
        new_mat.visible = self.visible
        new_mat.uniforms = self.uniforms.copy()
        new_mat.defines = self.defines.copy()
        new_mat.extensions = self.extensions.copy()
        new_mat.user_data = self.user_data.copy()
        return new_mat

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "vertex_shader": self.vertex_shader,
            "fragment_shader": self.fragment_shader,
            "uniforms": self.uniforms,
            "defines": self.defines
        })
        return data
