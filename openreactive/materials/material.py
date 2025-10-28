import uuid
from ..core.math3d import Vector3


class Material:
    def __init__(self, name="Material"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = "Material"
        self.opacity = 1.0
        self.transparent = False
        self.side = "front"
        self.depth_test = True
        self.depth_write = True
        self.wireframe = False
        self.visible = True
        self.user_data = {}

    def clone(self):
        new_mat = Material(self.name)
        new_mat.opacity = self.opacity
        new_mat.transparent = self.transparent
        new_mat.side = self.side
        new_mat.depth_test = self.depth_test
        new_mat.depth_write = self.depth_write
        new_mat.wireframe = self.wireframe
        new_mat.visible = self.visible
        new_mat.user_data = self.user_data.copy()
        return new_mat

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "opacity": self.opacity,
            "transparent": self.transparent,
            "side": self.side,
            "depth_test": self.depth_test,
            "depth_write": self.depth_write,
            "wireframe": self.wireframe,
            "visible": self.visible
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
