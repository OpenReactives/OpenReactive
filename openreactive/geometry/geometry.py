import numpy as np
import uuid


class Geometry:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = ""
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.colors = []
        self.indices = []
        self.attributes = {}
        self.bounding_box = None
        self.bounding_sphere = None

    def set_attribute(self, name, data, item_size):
        self.attributes[name] = {
            "data": np.array(data, dtype=np.float32),
            "item_size": item_size
        }
        return self

    def get_attribute(self, name):
        return self.attributes.get(name)

    def set_index(self, indices):
        self.indices = np.array(indices, dtype=np.uint32)
        return self

    def compute_vertex_normals(self):
        if not self.indices or len(self.vertices) == 0:
            return

        normals = np.zeros((len(self.vertices), 3), dtype=np.float32)

        for i in range(0, len(self.indices), 3):
            i1, i2, i3 = self.indices[i], self.indices[i + 1], self.indices[i + 2]

            v1 = np.array(self.vertices[i1])
            v2 = np.array(self.vertices[i2])
            v3 = np.array(self.vertices[i3])

            edge1 = v2 - v1
            edge2 = v3 - v1
            normal = np.cross(edge1, edge2)

            normals[i1] += normal
            normals[i2] += normal
            normals[i3] += normal

        for i in range(len(normals)):
            norm = np.linalg.norm(normals[i])
            if norm > 0:
                normals[i] /= norm

        self.normals = normals.tolist()
        return self

    def compute_bounding_box(self):
        if len(self.vertices) == 0:
            return None

        vertices = np.array(self.vertices)
        min_point = vertices.min(axis=0)
        max_point = vertices.max(axis=0)

        self.bounding_box = {
            "min": min_point.tolist(),
            "max": max_point.tolist()
        }
        return self.bounding_box

    def compute_bounding_sphere(self):
        if len(self.vertices) == 0:
            return None

        vertices = np.array(self.vertices)
        center = vertices.mean(axis=0)

        max_distance = 0
        for vertex in vertices:
            distance = np.linalg.norm(vertex - center)
            max_distance = max(max_distance, distance)

        self.bounding_sphere = {
            "center": center.tolist(),
            "radius": max_distance
        }
        return self.bounding_sphere

    def translate(self, x, y, z):
        offset = np.array([x, y, z])
        for i in range(len(self.vertices)):
            self.vertices[i] = (np.array(self.vertices[i]) + offset).tolist()
        return self

    def scale(self, x, y, z):
        scale_vec = np.array([x, y, z])
        for i in range(len(self.vertices)):
            self.vertices[i] = (np.array(self.vertices[i]) * scale_vec).tolist()
        return self

    def rotate_x(self, angle):
        import math
        c = math.cos(angle)
        s = math.sin(angle)
        for i in range(len(self.vertices)):
            y = self.vertices[i][1]
            z = self.vertices[i][2]
            self.vertices[i][1] = c * y - s * z
            self.vertices[i][2] = s * y + c * z
        return self

    def rotate_y(self, angle):
        import math
        c = math.cos(angle)
        s = math.sin(angle)
        for i in range(len(self.vertices)):
            x = self.vertices[i][0]
            z = self.vertices[i][2]
            self.vertices[i][0] = c * x + s * z
            self.vertices[i][2] = -s * x + c * z
        return self

    def rotate_z(self, angle):
        import math
        c = math.cos(angle)
        s = math.sin(angle)
        for i in range(len(self.vertices)):
            x = self.vertices[i][0]
            y = self.vertices[i][1]
            self.vertices[i][0] = c * x - s * y
            self.vertices[i][1] = s * x + c * y
        return self

    def merge(self, other_geometry):
        vertex_offset = len(self.vertices)

        self.vertices.extend(other_geometry.vertices)
        self.normals.extend(other_geometry.normals)
        self.uvs.extend(other_geometry.uvs)
        self.colors.extend(other_geometry.colors)

        for index in other_geometry.indices:
            self.indices.append(index + vertex_offset)

        return self

    def clone(self):
        new_geom = Geometry()
        new_geom.name = self.name
        new_geom.vertices = [v[:] for v in self.vertices]
        new_geom.normals = [n[:] for n in self.normals]
        new_geom.uvs = [uv[:] for uv in self.uvs]
        new_geom.colors = [c[:] for c in self.colors]
        new_geom.indices = self.indices.copy() if isinstance(self.indices, np.ndarray) else self.indices[:]
        new_geom.attributes = {k: v.copy() for k, v in self.attributes.items()}
        return new_geom

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": "Geometry",
            "vertices": self.vertices,
            "normals": self.normals,
            "uvs": self.uvs,
            "colors": self.colors,
            "indices": self.indices.tolist() if isinstance(self.indices, np.ndarray) else self.indices,
            "vertex_count": len(self.vertices),
            "face_count": len(self.indices) // 3 if self.indices else 0
        }

    def __repr__(self):
        return f"Geometry(vertices={len(self.vertices)}, faces={len(self.indices) // 3 if self.indices else 0})"
