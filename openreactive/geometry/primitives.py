from .geometry import Geometry
import math
import numpy as np


class BoxGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, width_segments=1, height_segments=1, depth_segments=1):
        super().__init__()
        self.name = "BoxGeometry"

        vertices = []
        normals = []
        uvs = []
        indices = []

        def build_plane(u, v, w, udir, vdir, width, height, depth, grid_x, grid_y):
            segmentWidth = width / grid_x
            segmentHeight = height / grid_y

            widthHalf = width / 2
            heightHalf = height / 2
            depthHalf = depth / 2

            gridX1 = grid_x + 1
            gridY1 = grid_y + 1

            vertex_counter = len(vertices) // 3

            for iy in range(gridY1):
                y = iy * segmentHeight - heightHalf

                for ix in range(gridX1):
                    x = ix * segmentWidth - widthHalf

                    vector = [0, 0, 0]
                    vector[u] = x * udir
                    vector[v] = y * vdir
                    vector[w] = depthHalf

                    vertices.extend(vector)

                    vector = [0, 0, 0]
                    vector[u] = 0
                    vector[v] = 0
                    vector[w] = 1 if depth > 0 else -1
                    normals.extend(vector)

                    uvs.extend([ix / grid_x, 1 - (iy / grid_y)])

            for iy in range(grid_y):
                for ix in range(grid_x):
                    a = vertex_counter + ix + gridX1 * iy
                    b = vertex_counter + ix + gridX1 * (iy + 1)
                    c = vertex_counter + (ix + 1) + gridX1 * (iy + 1)
                    d = vertex_counter + (ix + 1) + gridX1 * iy

                    indices.extend([a, b, d])
                    indices.extend([b, c, d])

        build_plane(2, 1, 0, -1, -1, depth, height, width, depth_segments, height_segments)
        build_plane(2, 1, 0, 1, -1, depth, height, -width, depth_segments, height_segments)
        build_plane(0, 2, 1, 1, 1, width, depth, height, width_segments, depth_segments)
        build_plane(0, 2, 1, 1, -1, width, depth, -height, width_segments, depth_segments)
        build_plane(0, 1, 2, 1, -1, width, height, depth, width_segments, height_segments)
        build_plane(0, 1, 2, -1, -1, width, height, -depth, width_segments, height_segments)

        self.vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
        self.normals = [normals[i:i+3] for i in range(0, len(normals), 3)]
        self.uvs = [uvs[i:i+2] for i in range(0, len(uvs), 2)]
        self.indices = indices


class SphereGeometry(Geometry):
    def __init__(self, radius=1, width_segments=32, height_segments=16, phi_start=0, phi_length=math.pi * 2,
                 theta_start=0, theta_length=math.pi):
        super().__init__()
        self.name = "SphereGeometry"

        vertices = []
        normals = []
        uvs = []
        indices = []

        width_segments = max(3, width_segments)
        height_segments = max(2, height_segments)

        theta_end = min(theta_start + theta_length, math.pi)

        index = 0
        grid = []

        for iy in range(height_segments + 1):
            vertices_row = []
            v = iy / height_segments

            uOffset = 0
            if iy == 0 and theta_start == 0:
                uOffset = 0.5 / width_segments
            elif iy == height_segments and theta_end == math.pi:
                uOffset = -0.5 / width_segments

            for ix in range(width_segments + 1):
                u = ix / width_segments

                px = -radius * math.cos(phi_start + u * phi_length) * math.sin(theta_start + v * theta_length)
                py = radius * math.cos(theta_start + v * theta_length)
                pz = radius * math.sin(phi_start + u * phi_length) * math.sin(theta_start + v * theta_length)

                vertices.extend([px, py, pz])

                length = math.sqrt(px * px + py * py + pz * pz)
                normals.extend([px / length, py / length, pz / length])

                uvs.extend([u + uOffset, 1 - v])

                vertices_row.append(index)
                index += 1

            grid.append(vertices_row)

        for iy in range(height_segments):
            for ix in range(width_segments):
                a = grid[iy][ix + 1]
                b = grid[iy][ix]
                c = grid[iy + 1][ix]
                d = grid[iy + 1][ix + 1]

                if iy != 0 or theta_start > 0:
                    indices.extend([a, b, d])
                if iy != height_segments - 1 or theta_end < math.pi:
                    indices.extend([b, c, d])

        self.vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
        self.normals = [normals[i:i+3] for i in range(0, len(normals), 3)]
        self.uvs = [uvs[i:i+2] for i in range(0, len(uvs), 2)]
        self.indices = indices


class PlaneGeometry(Geometry):
    def __init__(self, width=1, height=1, width_segments=1, height_segments=1):
        super().__init__()
        self.name = "PlaneGeometry"

        width_half = width / 2
        height_half = height / 2

        grid_x1 = width_segments + 1
        grid_y1 = height_segments + 1

        segment_width = width / width_segments
        segment_height = height / height_segments

        vertices = []
        normals = []
        uvs = []
        indices = []

        for iy in range(grid_y1):
            y = iy * segment_height - height_half

            for ix in range(grid_x1):
                x = ix * segment_width - width_half

                vertices.extend([x, -y, 0])
                normals.extend([0, 0, 1])
                uvs.extend([ix / width_segments, 1 - (iy / height_segments)])

        for iy in range(height_segments):
            for ix in range(width_segments):
                a = ix + grid_x1 * iy
                b = ix + grid_x1 * (iy + 1)
                c = (ix + 1) + grid_x1 * (iy + 1)
                d = (ix + 1) + grid_x1 * iy

                indices.extend([a, b, d])
                indices.extend([b, c, d])

        self.vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
        self.normals = [normals[i:i+3] for i in range(0, len(normals), 3)]
        self.uvs = [uvs[i:i+2] for i in range(0, len(uvs), 2)]
        self.indices = indices


class CylinderGeometry(Geometry):
    def __init__(self, radius_top=1, radius_bottom=1, height=1, radial_segments=32, height_segments=1,
                 open_ended=False, theta_start=0, theta_length=math.pi * 2):
        super().__init__()
        self.name = "CylinderGeometry"

        vertices = []
        normals = []
        uvs = []
        indices = []

        index = 0
        index_array = []
        half_height = height / 2

        def generate_torso():
            nonlocal index

            for y in range(height_segments + 1):
                index_row = []
                v = y / height_segments
                radius = v * (radius_bottom - radius_top) + radius_top

                for x in range(radial_segments + 1):
                    u = x / radial_segments
                    theta = u * theta_length + theta_start

                    sin_theta = math.sin(theta)
                    cos_theta = math.cos(theta)

                    vx = radius * sin_theta
                    vy = -v * height + half_height
                    vz = radius * cos_theta

                    vertices.extend([vx, vy, vz])

                    slope = (radius_bottom - radius_top) / height
                    nx = sin_theta
                    ny = slope
                    nz = cos_theta
                    length = math.sqrt(nx * nx + ny * ny + nz * nz)
                    normals.extend([nx / length, ny / length, nz / length])

                    uvs.extend([u, 1 - v])

                    index_row.append(index)
                    index += 1

                index_array.append(index_row)

            for x in range(radial_segments):
                for y in range(height_segments):
                    a = index_array[y][x]
                    b = index_array[y + 1][x]
                    c = index_array[y + 1][x + 1]
                    d = index_array[y][x + 1]

                    indices.extend([a, b, d])
                    indices.extend([b, c, d])

        def generate_cap(top):
            nonlocal index

            center_index_start = index

            radius = radius_top if top else radius_bottom
            sign = 1 if top else -1

            for x in range(radial_segments + 1):
                vertices.extend([0, half_height * sign, 0])
                normals.extend([0, sign, 0])
                uvs.extend([0.5, 0.5])
                index += 1

            center_index_end = index

            for x in range(radial_segments + 1):
                u = x / radial_segments
                theta = u * theta_length + theta_start

                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)

                vx = radius * sin_theta
                vy = half_height * sign
                vz = radius * cos_theta

                vertices.extend([vx, vy, vz])
                normals.extend([0, sign, 0])
                uvs.extend([(cos_theta * 0.5) + 0.5, (sin_theta * 0.5 * sign) + 0.5])
                index += 1

            for x in range(radial_segments):
                c = center_index_start + x
                i = center_index_end + x

                if top:
                    indices.extend([i, i + 1, c])
                else:
                    indices.extend([i + 1, i, c])

        generate_torso()

        if not open_ended:
            if radius_top > 0:
                generate_cap(True)
            if radius_bottom > 0:
                generate_cap(False)

        self.vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
        self.normals = [normals[i:i+3] for i in range(0, len(normals), 3)]
        self.uvs = [uvs[i:i+2] for i in range(0, len(uvs), 2)]
        self.indices = indices


class ConeGeometry(CylinderGeometry):
    def __init__(self, radius=1, height=1, radial_segments=32, height_segments=1,
                 open_ended=False, theta_start=0, theta_length=math.pi * 2):
        super().__init__(0, radius, height, radial_segments, height_segments,
                        open_ended, theta_start, theta_length)
        self.name = "ConeGeometry"


class TorusGeometry(Geometry):
    def __init__(self, radius=1, tube=0.4, radial_segments=12, tubular_segments=48,
                 arc=math.pi * 2):
        super().__init__()
        self.name = "TorusGeometry"

        vertices = []
        normals = []
        uvs = []
        indices = []

        for j in range(radial_segments + 1):
            for i in range(tubular_segments + 1):
                u = i / tubular_segments * arc
                v = j / radial_segments * math.pi * 2

                cx = (radius + tube * math.cos(v)) * math.cos(u)
                cy = (radius + tube * math.cos(v)) * math.sin(u)
                cz = tube * math.sin(v)

                vertices.extend([cx, cy, cz])

                nx = math.cos(v) * math.cos(u)
                ny = math.cos(v) * math.sin(u)
                nz = math.sin(v)
                normals.extend([nx, ny, nz])

                uvs.extend([i / tubular_segments, j / radial_segments])

        for j in range(radial_segments):
            for i in range(tubular_segments):
                a = (tubular_segments + 1) * j + i
                b = (tubular_segments + 1) * (j + 1) + i
                c = (tubular_segments + 1) * (j + 1) + i + 1
                d = (tubular_segments + 1) * j + i + 1

                indices.extend([a, b, d])
                indices.extend([b, c, d])

        self.vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
        self.normals = [normals[i:i+3] for i in range(0, len(normals), 3)]
        self.uvs = [uvs[i:i+2] for i in range(0, len(uvs), 2)]
        self.indices = indices
