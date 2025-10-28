from .math3d import Vector3, Matrix4, Quaternion
import math


class Transform:
    def __init__(self):
        self.position = Vector3.zero()
        self.rotation = Quaternion.identity()
        self.scale = Vector3.one()
        self._local_matrix = None
        self._world_matrix = None
        self._dirty = True
        self.parent = None
        self.children = []

    def set_position(self, x, y, z):
        if isinstance(x, Vector3):
            self.position = x
        else:
            self.position = Vector3(x, y, z)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def set_rotation(self, rotation):
        if isinstance(rotation, Quaternion):
            self.rotation = rotation
        elif isinstance(rotation, Vector3):
            self.rotation = Quaternion.from_euler(rotation.x, rotation.y, rotation.z)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def set_rotation_euler(self, x, y, z):
        self.rotation = Quaternion.from_euler(x, y, z)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def set_scale(self, x, y=None, z=None):
        if isinstance(x, Vector3):
            self.scale = x
        elif y is None and z is None:
            self.scale = Vector3(x, x, x)
        else:
            self.scale = Vector3(x, y, z)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def translate(self, x, y=None, z=None):
        if isinstance(x, Vector3):
            self.position = self.position + x
        else:
            self.position = self.position + Vector3(x, y, z)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def rotate(self, axis, angle):
        q = Quaternion.from_axis_angle(axis, angle)
        self.rotation = self.rotation * q
        self._dirty = True
        self._mark_children_dirty()
        return self

    def rotate_euler(self, x, y, z):
        q = Quaternion.from_euler(x, y, z)
        self.rotation = self.rotation * q
        self._dirty = True
        self._mark_children_dirty()
        return self

    def look_at(self, target, up=None):
        if up is None:
            up = Vector3.up()

        direction = (target - self.position).normalize()
        if direction.length() < 0.0001:
            return self

        right = up.cross(direction).normalize()
        up = direction.cross(right).normalize()

        rotation_matrix = Matrix4()
        rotation_matrix.data[0, 0] = right.x
        rotation_matrix.data[1, 0] = right.y
        rotation_matrix.data[2, 0] = right.z

        rotation_matrix.data[0, 1] = up.x
        rotation_matrix.data[1, 1] = up.y
        rotation_matrix.data[2, 1] = up.z

        rotation_matrix.data[0, 2] = direction.x
        rotation_matrix.data[1, 2] = direction.y
        rotation_matrix.data[2, 2] = direction.z

        self.rotation = Quaternion.from_rotation_matrix(rotation_matrix)
        self._dirty = True
        self._mark_children_dirty()
        return self

    def get_local_matrix(self):
        if self._dirty or self._local_matrix is None:
            translation = Matrix4.translation(self.position.x, self.position.y, self.position.z)
            rotation = self.rotation.to_matrix4()
            scale = Matrix4.scaling(self.scale.x, self.scale.y, self.scale.z)
            self._local_matrix = translation * rotation * scale
            self._dirty = False
        return self._local_matrix

    def get_world_matrix(self):
        if self._world_matrix is None or self._dirty:
            if self.parent is None:
                self._world_matrix = self.get_local_matrix()
            else:
                self._world_matrix = self.parent.get_world_matrix() * self.get_local_matrix()
        return self._world_matrix

    def get_world_position(self):
        world_mat = self.get_world_matrix()
        return Vector3(world_mat.data[0, 3], world_mat.data[1, 3], world_mat.data[2, 3])

    def get_forward(self):
        return self.rotation * Vector3.forward()

    def get_right(self):
        return self.rotation * Vector3.right()

    def get_up(self):
        return self.rotation * Vector3.up()

    def add_child(self, child_transform):
        if child_transform not in self.children:
            if child_transform.parent:
                child_transform.parent.remove_child(child_transform)
            child_transform.parent = self
            self.children.append(child_transform)
            child_transform._mark_dirty()

    def remove_child(self, child_transform):
        if child_transform in self.children:
            child_transform.parent = None
            self.children.remove(child_transform)
            child_transform._mark_dirty()

    def _mark_dirty(self):
        self._dirty = True
        self._world_matrix = None
        self._mark_children_dirty()

    def _mark_children_dirty(self):
        for child in self.children:
            child._mark_dirty()

    def decompose_matrix(self, matrix):
        self.position = Vector3(
            matrix.data[0, 3],
            matrix.data[1, 3],
            matrix.data[2, 3]
        )

        scale_x = Vector3(matrix.data[0, 0], matrix.data[1, 0], matrix.data[2, 0]).length()
        scale_y = Vector3(matrix.data[0, 1], matrix.data[1, 1], matrix.data[2, 1]).length()
        scale_z = Vector3(matrix.data[0, 2], matrix.data[1, 2], matrix.data[2, 2]).length()
        self.scale = Vector3(scale_x, scale_y, scale_z)

        rotation_matrix = Matrix4()
        rotation_matrix.data[0, 0] = matrix.data[0, 0] / scale_x
        rotation_matrix.data[1, 0] = matrix.data[1, 0] / scale_x
        rotation_matrix.data[2, 0] = matrix.data[2, 0] / scale_x

        rotation_matrix.data[0, 1] = matrix.data[0, 1] / scale_y
        rotation_matrix.data[1, 1] = matrix.data[1, 1] / scale_y
        rotation_matrix.data[2, 1] = matrix.data[2, 1] / scale_y

        rotation_matrix.data[0, 2] = matrix.data[0, 2] / scale_z
        rotation_matrix.data[1, 2] = matrix.data[1, 2] / scale_z
        rotation_matrix.data[2, 2] = matrix.data[2, 2] / scale_z

        self.rotation = Quaternion.from_rotation_matrix(rotation_matrix)
        self._dirty = True

    def clone(self):
        new_transform = Transform()
        new_transform.position = Vector3(self.position.x, self.position.y, self.position.z)
        new_transform.rotation = Quaternion(self.rotation.x, self.rotation.y, self.rotation.z, self.rotation.w)
        new_transform.scale = Vector3(self.scale.x, self.scale.y, self.scale.z)
        return new_transform

    def __repr__(self):
        return f"Transform(pos={self.position}, rot={self.rotation}, scale={self.scale})"
