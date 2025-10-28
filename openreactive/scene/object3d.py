from ..core.transform import Transform
from ..core.math3d import Vector3, Matrix4
import uuid


class Object3D:
    def __init__(self, name="Object3D"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.transform = Transform()
        self.visible = True
        self.parent = None
        self.children = []
        self.user_data = {}
        self.layers = [0]
        self.render_order = 0

    def add(self, child):
        if child == self:
            return self

        if child.parent:
            child.parent.remove(child)

        child.parent = self
        self.children.append(child)
        self.transform.add_child(child.transform)
        return self

    def remove(self, child):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            self.transform.remove_child(child.transform)
        return self

    def get_child_by_name(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_child_by_id(self, obj_id):
        for child in self.children:
            if child.id == obj_id:
                return child
        return None

    def traverse(self, callback):
        callback(self)
        for child in self.children:
            child.traverse(callback)

    def traverse_visible(self, callback):
        if not self.visible:
            return
        callback(self)
        for child in self.children:
            child.traverse_visible(callback)

    def get_world_position(self):
        return self.transform.get_world_position()

    def get_world_matrix(self):
        return self.transform.get_world_matrix()

    def update_matrix(self):
        self.transform.get_local_matrix()

    def update_matrix_world(self, force=False):
        self.update_matrix()
        self.transform.get_world_matrix()

        for child in self.children:
            child.update_matrix_world(force)

    def clone(self, recursive=True):
        new_obj = Object3D(self.name)
        new_obj.transform = self.transform.clone()
        new_obj.visible = self.visible
        new_obj.user_data = self.user_data.copy()
        new_obj.layers = self.layers.copy()
        new_obj.render_order = self.render_order

        if recursive:
            for child in self.children:
                new_obj.add(child.clone(recursive))

        return new_obj

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id}')"


class Mesh(Object3D):
    def __init__(self, geometry=None, material=None, name="Mesh"):
        super().__init__(name)
        self.geometry = geometry
        self.material = material
        self.cast_shadow = True
        self.receive_shadow = True
        self.frustum_culled = True

    def clone(self, recursive=True):
        new_mesh = Mesh(self.geometry, self.material, self.name)
        new_mesh.transform = self.transform.clone()
        new_mesh.visible = self.visible
        new_mesh.user_data = self.user_data.copy()
        new_mesh.layers = self.layers.copy()
        new_mesh.render_order = self.render_order
        new_mesh.cast_shadow = self.cast_shadow
        new_mesh.receive_shadow = self.receive_shadow
        new_mesh.frustum_culled = self.frustum_culled

        if recursive:
            for child in self.children:
                new_mesh.add(child.clone(recursive))

        return new_mesh


class Camera(Object3D):
    def __init__(self, name="Camera"):
        super().__init__(name)
        self.projection_matrix = Matrix4.identity()
        self.view_matrix = Matrix4.identity()
        self.near = 0.1
        self.far = 1000.0

    def get_view_matrix(self):
        world_matrix = self.get_world_matrix()
        self.view_matrix = world_matrix.inverse()
        return self.view_matrix

    def get_projection_matrix(self):
        return self.projection_matrix

    def update_projection_matrix(self):
        pass


class PerspectiveCamera(Camera):
    def __init__(self, fov=60.0, aspect=1.0, near=0.1, far=1000.0, name="PerspectiveCamera"):
        super().__init__(name)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.update_projection_matrix()

    def update_projection_matrix(self):
        import math
        fov_rad = math.radians(self.fov)
        self.projection_matrix = Matrix4.perspective(fov_rad, self.aspect, self.near, self.far)

    def clone(self, recursive=True):
        new_cam = PerspectiveCamera(self.fov, self.aspect, self.near, self.far, self.name)
        new_cam.transform = self.transform.clone()
        new_cam.visible = self.visible
        new_cam.user_data = self.user_data.copy()
        new_cam.layers = self.layers.copy()

        if recursive:
            for child in self.children:
                new_cam.add(child.clone(recursive))

        return new_cam


class OrthographicCamera(Camera):
    def __init__(self, left=-1, right=1, top=1, bottom=-1, near=0.1, far=1000.0, name="OrthographicCamera"):
        super().__init__(name)
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far
        self.update_projection_matrix()

    def update_projection_matrix(self):
        self.projection_matrix = Matrix4.orthographic(
            self.left, self.right, self.bottom, self.top, self.near, self.far
        )

    def clone(self, recursive=True):
        new_cam = OrthographicCamera(
            self.left, self.right, self.top, self.bottom,
            self.near, self.far, self.name
        )
        new_cam.transform = self.transform.clone()
        new_cam.visible = self.visible
        new_cam.user_data = self.user_data.copy()
        new_cam.layers = self.layers.copy()

        if recursive:
            for child in self.children:
                new_cam.add(child.clone(recursive))

        return new_cam


class Light(Object3D):
    def __init__(self, color=None, intensity=1.0, name="Light"):
        super().__init__(name)
        self.color = color if color else Vector3(1, 1, 1)
        self.intensity = intensity
        self.cast_shadow = False


class DirectionalLight(Light):
    def __init__(self, color=None, intensity=1.0, name="DirectionalLight"):
        super().__init__(color, intensity, name)
        self.target = Object3D("DirectionalLightTarget")

    def clone(self, recursive=True):
        new_light = DirectionalLight(
            Vector3(self.color.x, self.color.y, self.color.z),
            self.intensity,
            self.name
        )
        new_light.transform = self.transform.clone()
        new_light.visible = self.visible
        new_light.cast_shadow = self.cast_shadow

        if recursive:
            for child in self.children:
                new_light.add(child.clone(recursive))

        return new_light


class PointLight(Light):
    def __init__(self, color=None, intensity=1.0, distance=0, decay=1, name="PointLight"):
        super().__init__(color, intensity, name)
        self.distance = distance
        self.decay = decay

    def clone(self, recursive=True):
        new_light = PointLight(
            Vector3(self.color.x, self.color.y, self.color.z),
            self.intensity,
            self.distance,
            self.decay,
            self.name
        )
        new_light.transform = self.transform.clone()
        new_light.visible = self.visible
        new_light.cast_shadow = self.cast_shadow

        if recursive:
            for child in self.children:
                new_light.add(child.clone(recursive))

        return new_light


class SpotLight(Light):
    def __init__(self, color=None, intensity=1.0, distance=0, angle=60, penumbra=0, decay=1, name="SpotLight"):
        super().__init__(color, intensity, name)
        self.distance = distance
        self.angle = angle
        self.penumbra = penumbra
        self.decay = decay
        self.target = Object3D("SpotLightTarget")

    def clone(self, recursive=True):
        new_light = SpotLight(
            Vector3(self.color.x, self.color.y, self.color.z),
            self.intensity,
            self.distance,
            self.angle,
            self.penumbra,
            self.decay,
            self.name
        )
        new_light.transform = self.transform.clone()
        new_light.visible = self.visible
        new_light.cast_shadow = self.cast_shadow

        if recursive:
            for child in self.children:
                new_light.add(child.clone(recursive))

        return new_light


class AmbientLight(Light):
    def __init__(self, color=None, intensity=1.0, name="AmbientLight"):
        super().__init__(color, intensity, name)

    def clone(self, recursive=True):
        new_light = AmbientLight(
            Vector3(self.color.x, self.color.y, self.color.z),
            self.intensity,
            self.name
        )
        new_light.visible = self.visible

        if recursive:
            for child in self.children:
                new_light.add(child.clone(recursive))

        return new_light
