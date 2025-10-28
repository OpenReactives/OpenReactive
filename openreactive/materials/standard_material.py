from .material import Material
from ..core.math3d import Vector3


class StandardMaterial(Material):
    def __init__(self, name="StandardMaterial"):
        super().__init__(name)
        self.type = "StandardMaterial"
        self.color = Vector3(1, 1, 1)
        self.emissive = Vector3(0, 0, 0)
        self.emissive_intensity = 1.0
        self.metalness = 0.0
        self.roughness = 1.0
        self.map = None
        self.normal_map = None
        self.emissive_map = None
        self.roughness_map = None
        self.metalness_map = None
        self.ao_map = None
        self.env_map = None
        self.env_map_intensity = 1.0

    def clone(self):
        new_mat = StandardMaterial(self.name)
        new_mat.opacity = self.opacity
        new_mat.transparent = self.transparent
        new_mat.side = self.side
        new_mat.depth_test = self.depth_test
        new_mat.depth_write = self.depth_write
        new_mat.wireframe = self.wireframe
        new_mat.visible = self.visible
        new_mat.color = Vector3(self.color.x, self.color.y, self.color.z)
        new_mat.emissive = Vector3(self.emissive.x, self.emissive.y, self.emissive.z)
        new_mat.emissive_intensity = self.emissive_intensity
        new_mat.metalness = self.metalness
        new_mat.roughness = self.roughness
        new_mat.env_map_intensity = self.env_map_intensity
        new_mat.user_data = self.user_data.copy()
        return new_mat

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "color": self.color.to_array(),
            "emissive": self.emissive.to_array(),
            "emissive_intensity": self.emissive_intensity,
            "metalness": self.metalness,
            "roughness": self.roughness,
            "env_map_intensity": self.env_map_intensity
        })
        return data
