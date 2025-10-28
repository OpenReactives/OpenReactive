import numpy as np
import math


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.data = np.array([x, y, z], dtype=np.float32)

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, value):
        self.data[2] = value

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(*(self.data + other.data))
        return Vector3(*(self.data + other))

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(*(self.data - other.data))
        return Vector3(*(self.data - other))

    def __mul__(self, scalar):
        return Vector3(*(self.data * scalar))

    def __truediv__(self, scalar):
        return Vector3(*(self.data / scalar))

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def dot(self, other):
        return np.dot(self.data, other.data)

    def cross(self, other):
        return Vector3(*np.cross(self.data, other.data))

    def length(self):
        return np.linalg.norm(self.data)

    def length_squared(self):
        return np.dot(self.data, self.data)

    def normalize(self):
        length = self.length()
        if length > 0:
            return self / length
        return Vector3(0, 0, 0)

    def distance_to(self, other):
        return (self - other).length()

    def lerp(self, other, t):
        return self * (1 - t) + other * t

    def reflect(self, normal):
        return self - normal * (2 * self.dot(normal))

    def to_array(self):
        return self.data.tolist()

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    @staticmethod
    def zero():
        return Vector3(0, 0, 0)

    @staticmethod
    def one():
        return Vector3(1, 1, 1)

    @staticmethod
    def up():
        return Vector3(0, 1, 0)

    @staticmethod
    def down():
        return Vector3(0, -1, 0)

    @staticmethod
    def left():
        return Vector3(-1, 0, 0)

    @staticmethod
    def right():
        return Vector3(1, 0, 0)

    @staticmethod
    def forward():
        return Vector3(0, 0, 1)

    @staticmethod
    def back():
        return Vector3(0, 0, -1)


class Vector4:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.data = np.array([x, y, z, w], dtype=np.float32)

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, value):
        self.data[2] = value

    @property
    def w(self):
        return self.data[3]

    @w.setter
    def w(self, value):
        self.data[3] = value

    def __add__(self, other):
        if isinstance(other, Vector4):
            return Vector4(*(self.data + other.data))
        return Vector4(*(self.data + other))

    def __sub__(self, other):
        if isinstance(other, Vector4):
            return Vector4(*(self.data - other.data))
        return Vector4(*(self.data - other))

    def __mul__(self, scalar):
        return Vector4(*(self.data * scalar))

    def __truediv__(self, scalar):
        return Vector4(*(self.data / scalar))

    def to_vector3(self):
        if self.w != 0:
            return Vector3(self.x / self.w, self.y / self.w, self.z / self.w)
        return Vector3(self.x, self.y, self.z)

    def to_array(self):
        return self.data.tolist()

    def __repr__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"


class Matrix4:
    def __init__(self, data=None):
        if data is None:
            self.data = np.identity(4, dtype=np.float32)
        else:
            self.data = np.array(data, dtype=np.float32).reshape(4, 4)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            result = Matrix4()
            result.data = np.matmul(self.data, other.data)
            return result
        elif isinstance(other, Vector4):
            result_data = np.matmul(self.data, other.data)
            return Vector4(*result_data)
        elif isinstance(other, Vector3):
            v4 = Vector4(other.x, other.y, other.z, 1.0)
            result = self * v4
            return result.to_vector3()
        return NotImplemented

    def transform_point(self, point):
        v4 = Vector4(point.x, point.y, point.z, 1.0)
        result = self * v4
        return result.to_vector3()

    def transform_direction(self, direction):
        v4 = Vector4(direction.x, direction.y, direction.z, 0.0)
        result = self * v4
        return Vector3(result.x, result.y, result.z)

    def transpose(self):
        result = Matrix4()
        result.data = self.data.T
        return result

    def inverse(self):
        result = Matrix4()
        result.data = np.linalg.inv(self.data)
        return result

    def determinant(self):
        return np.linalg.det(self.data)

    def to_array(self):
        return self.data.flatten().tolist()

    def to_array_2d(self):
        return self.data.tolist()

    def __repr__(self):
        return f"Matrix4(\n{self.data}\n)"

    @staticmethod
    def identity():
        return Matrix4()

    @staticmethod
    def translation(x, y, z):
        mat = Matrix4()
        mat.data[0, 3] = x
        mat.data[1, 3] = y
        mat.data[2, 3] = z
        return mat

    @staticmethod
    def scaling(x, y, z):
        mat = Matrix4()
        mat.data[0, 0] = x
        mat.data[1, 1] = y
        mat.data[2, 2] = z
        return mat

    @staticmethod
    def rotation_x(angle_rad):
        mat = Matrix4()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        mat.data[1, 1] = c
        mat.data[1, 2] = -s
        mat.data[2, 1] = s
        mat.data[2, 2] = c
        return mat

    @staticmethod
    def rotation_y(angle_rad):
        mat = Matrix4()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        mat.data[0, 0] = c
        mat.data[0, 2] = s
        mat.data[2, 0] = -s
        mat.data[2, 2] = c
        return mat

    @staticmethod
    def rotation_z(angle_rad):
        mat = Matrix4()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        mat.data[0, 0] = c
        mat.data[0, 1] = -s
        mat.data[1, 0] = s
        mat.data[1, 1] = c
        return mat

    @staticmethod
    def rotation_axis(axis, angle_rad):
        axis = axis.normalize()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        t = 1 - c
        x, y, z = axis.x, axis.y, axis.z

        mat = Matrix4()
        mat.data[0, 0] = t * x * x + c
        mat.data[0, 1] = t * x * y - s * z
        mat.data[0, 2] = t * x * z + s * y
        mat.data[1, 0] = t * x * y + s * z
        mat.data[1, 1] = t * y * y + c
        mat.data[1, 2] = t * y * z - s * x
        mat.data[2, 0] = t * x * z - s * y
        mat.data[2, 1] = t * y * z + s * x
        mat.data[2, 2] = t * z * z + c
        return mat

    @staticmethod
    def perspective(fov_y_rad, aspect, near, far):
        mat = Matrix4(np.zeros((4, 4)))
        tan_half_fov = math.tan(fov_y_rad / 2)

        mat.data[0, 0] = 1 / (aspect * tan_half_fov)
        mat.data[1, 1] = 1 / tan_half_fov
        mat.data[2, 2] = -(far + near) / (far - near)
        mat.data[2, 3] = -(2 * far * near) / (far - near)
        mat.data[3, 2] = -1
        return mat

    @staticmethod
    def orthographic(left, right, bottom, top, near, far):
        mat = Matrix4()
        mat.data[0, 0] = 2 / (right - left)
        mat.data[1, 1] = 2 / (top - bottom)
        mat.data[2, 2] = -2 / (far - near)
        mat.data[0, 3] = -(right + left) / (right - left)
        mat.data[1, 3] = -(top + bottom) / (top - bottom)
        mat.data[2, 3] = -(far + near) / (far - near)
        return mat

    @staticmethod
    def look_at(eye, target, up):
        z_axis = (eye - target).normalize()
        x_axis = up.cross(z_axis).normalize()
        y_axis = z_axis.cross(x_axis)

        mat = Matrix4()
        mat.data[0, 0] = x_axis.x
        mat.data[0, 1] = x_axis.y
        mat.data[0, 2] = x_axis.z
        mat.data[0, 3] = -x_axis.dot(eye)

        mat.data[1, 0] = y_axis.x
        mat.data[1, 1] = y_axis.y
        mat.data[1, 2] = y_axis.z
        mat.data[1, 3] = -y_axis.dot(eye)

        mat.data[2, 0] = z_axis.x
        mat.data[2, 1] = z_axis.y
        mat.data[2, 2] = z_axis.z
        mat.data[2, 3] = -z_axis.dot(eye)

        return mat


class Quaternion:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
                self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
                self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
                self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            )
        elif isinstance(other, Vector3):
            qv = Quaternion(other.x, other.y, other.z, 0)
            result = self * qv * self.conjugate()
            return Vector3(result.x, result.y, result.z)
        return NotImplemented

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def normalize(self):
        length = self.length()
        if length > 0:
            return Quaternion(
                self.x / length,
                self.y / length,
                self.z / length,
                self.w / length
            )
        return Quaternion()

    def to_matrix4(self):
        q = self.normalize()
        x2 = q.x * q.x
        y2 = q.y * q.y
        z2 = q.z * q.z
        xy = q.x * q.y
        xz = q.x * q.z
        yz = q.y * q.z
        wx = q.w * q.x
        wy = q.w * q.y
        wz = q.w * q.z

        mat = Matrix4()
        mat.data[0, 0] = 1 - 2 * (y2 + z2)
        mat.data[0, 1] = 2 * (xy - wz)
        mat.data[0, 2] = 2 * (xz + wy)

        mat.data[1, 0] = 2 * (xy + wz)
        mat.data[1, 1] = 1 - 2 * (x2 + z2)
        mat.data[1, 2] = 2 * (yz - wx)

        mat.data[2, 0] = 2 * (xz - wy)
        mat.data[2, 1] = 2 * (yz + wx)
        mat.data[2, 2] = 1 - 2 * (x2 + y2)

        return mat

    def to_euler(self):
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x * self.x + self.y * self.y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (self.w * self.y - self.z * self.x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y * self.y + self.z * self.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return Vector3(roll, pitch, yaw)

    def slerp(self, other, t):
        dot = self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

        if dot < 0:
            other = Quaternion(-other.x, -other.y, -other.z, -other.w)
            dot = -dot

        if dot > 0.9995:
            result = Quaternion(
                self.x + t * (other.x - self.x),
                self.y + t * (other.y - self.y),
                self.z + t * (other.z - self.z),
                self.w + t * (other.w - self.w)
            )
            return result.normalize()

        theta_0 = math.acos(dot)
        theta = theta_0 * t
        sin_theta = math.sin(theta)
        sin_theta_0 = math.sin(theta_0)

        s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0

        return Quaternion(
            s0 * self.x + s1 * other.x,
            s0 * self.y + s1 * other.y,
            s0 * self.z + s1 * other.z,
            s0 * self.w + s1 * other.w
        )

    def __repr__(self):
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"

    @staticmethod
    def identity():
        return Quaternion(0, 0, 0, 1)

    @staticmethod
    def from_euler(roll, pitch, yaw):
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        return Quaternion(
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )

    @staticmethod
    def from_axis_angle(axis, angle):
        half_angle = angle * 0.5
        s = math.sin(half_angle)
        axis = axis.normalize()
        return Quaternion(
            axis.x * s,
            axis.y * s,
            axis.z * s,
            math.cos(half_angle)
        )

    @staticmethod
    def from_rotation_matrix(mat):
        trace = mat.data[0, 0] + mat.data[1, 1] + mat.data[2, 2]

        if trace > 0:
            s = 0.5 / math.sqrt(trace + 1.0)
            return Quaternion(
                (mat.data[2, 1] - mat.data[1, 2]) * s,
                (mat.data[0, 2] - mat.data[2, 0]) * s,
                (mat.data[1, 0] - mat.data[0, 1]) * s,
                0.25 / s
            )
        elif mat.data[0, 0] > mat.data[1, 1] and mat.data[0, 0] > mat.data[2, 2]:
            s = 2.0 * math.sqrt(1.0 + mat.data[0, 0] - mat.data[1, 1] - mat.data[2, 2])
            return Quaternion(
                0.25 * s,
                (mat.data[0, 1] + mat.data[1, 0]) / s,
                (mat.data[0, 2] + mat.data[2, 0]) / s,
                (mat.data[2, 1] - mat.data[1, 2]) / s
            )
        elif mat.data[1, 1] > mat.data[2, 2]:
            s = 2.0 * math.sqrt(1.0 + mat.data[1, 1] - mat.data[0, 0] - mat.data[2, 2])
            return Quaternion(
                (mat.data[0, 1] + mat.data[1, 0]) / s,
                0.25 * s,
                (mat.data[1, 2] + mat.data[2, 1]) / s,
                (mat.data[0, 2] - mat.data[2, 0]) / s
            )
        else:
            s = 2.0 * math.sqrt(1.0 + mat.data[2, 2] - mat.data[0, 0] - mat.data[1, 1])
            return Quaternion(
                (mat.data[0, 2] + mat.data[2, 0]) / s,
                (mat.data[1, 2] + mat.data[2, 1]) / s,
                0.25 * s,
                (mat.data[1, 0] - mat.data[0, 1]) / s
            )
