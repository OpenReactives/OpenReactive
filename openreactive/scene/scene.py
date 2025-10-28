from .object3d import Object3D, Camera, Light
from ..core.math3d import Vector3


class Scene(Object3D):
    def __init__(self, name="Scene"):
        super().__init__(name)
        self.background = None
        self.fog = None
        self.ambient_light = None
        self.environment = None
        self.auto_update = True

    def add(self, obj):
        if isinstance(obj, Object3D):
            return super().add(obj)
        return self

    def get_objects_by_type(self, obj_type):
        objects = []

        def collect(obj):
            if isinstance(obj, obj_type):
                objects.append(obj)

        self.traverse(collect)
        return objects

    def get_cameras(self):
        return self.get_objects_by_type(Camera)

    def get_lights(self):
        return self.get_objects_by_type(Light)

    def get_main_camera(self):
        cameras = self.get_cameras()
        return cameras[0] if cameras else None

    def to_dict(self):
        def object_to_dict(obj):
            data = {
                "id": obj.id,
                "name": obj.name,
                "type": obj.__class__.__name__,
                "visible": obj.visible,
                "position": obj.transform.position.to_array(),
                "rotation": [obj.transform.rotation.x, obj.transform.rotation.y,
                           obj.transform.rotation.z, obj.transform.rotation.w],
                "scale": obj.transform.scale.to_array(),
                "children": [object_to_dict(child) for child in obj.children]
            }

            if hasattr(obj, 'geometry') and obj.geometry:
                data["geometry"] = obj.geometry.id

            if hasattr(obj, 'material') and obj.material:
                data["material"] = obj.material.id

            if hasattr(obj, 'color'):
                data["color"] = obj.color.to_array()

            if hasattr(obj, 'intensity'):
                data["intensity"] = obj.intensity

            if hasattr(obj, 'fov'):
                data["fov"] = obj.fov
                data["aspect"] = obj.aspect
                data["near"] = obj.near
                data["far"] = obj.far

            return data

        return {
            "scene": object_to_dict(self),
            "metadata": {
                "version": "1.0",
                "type": "Scene",
                "generator": "OpenReactive"
            }
        }

    def clone(self, recursive=True):
        new_scene = Scene(self.name)
        new_scene.background = self.background
        new_scene.fog = self.fog
        new_scene.ambient_light = self.ambient_light
        new_scene.environment = self.environment

        if recursive:
            for child in self.children:
                new_scene.add(child.clone(recursive))

        return new_scene


class Fog:
    def __init__(self, color, near=1, far=1000):
        self.color = color
        self.near = near
        self.far = far

    def to_dict(self):
        return {
            "type": "Fog",
            "color": self.color.to_array() if hasattr(self.color, 'to_array') else self.color,
            "near": self.near,
            "far": self.far
        }


class FogExp2:
    def __init__(self, color, density=0.00025):
        self.color = color
        self.density = density

    def to_dict(self):
        return {
            "type": "FogExp2",
            "color": self.color.to_array() if hasattr(self.color, 'to_array') else self.color,
            "density": self.density
        }
