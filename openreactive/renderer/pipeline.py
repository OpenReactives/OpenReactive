import numpy as np
from ..core.math3d import Vector3, Vector4, Matrix4
from ..scene.object3d import Mesh, Light, Camera


class RenderPipeline:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 4), dtype=np.float32)
        self.depth_buffer = np.ones((height, width), dtype=np.float32) * float('inf')
        self.clear_color = Vector4(0, 0, 0, 1)
        self.viewport = (0, 0, width, height)
        self.culling_enabled = True
        self.depth_test_enabled = True

    def clear(self, color=True, depth=True):
        if color:
            self.color_buffer[:] = [self.clear_color.x, self.clear_color.y,
                                   self.clear_color.z, self.clear_color.w]
        if depth:
            self.depth_buffer[:] = float('inf')

    def set_clear_color(self, r, g, b, a=1.0):
        self.clear_color = Vector4(r, g, b, a)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 4), dtype=np.float32)
        self.depth_buffer = np.ones((height, width), dtype=np.float32) * float('inf')

    def render(self, scene, camera):
        self.clear()

        if not camera:
            return

        view_matrix = camera.get_view_matrix()
        projection_matrix = camera.get_projection_matrix()
        view_projection = projection_matrix * view_matrix

        renderables = []
        lights = []

        def collect_objects(obj):
            if not obj.visible:
                return

            if isinstance(obj, Mesh) and obj.geometry and obj.material:
                renderables.append(obj)
            elif isinstance(obj, Light):
                lights.append(obj)

        scene.traverse(collect_objects)

        renderables.sort(key=lambda x: x.render_order)

        for mesh in renderables:
            self._render_mesh(mesh, view_projection, lights, camera)

    def _render_mesh(self, mesh, view_projection, lights, camera):
        geometry = mesh.geometry
        material = mesh.material

        if not geometry.vertices or not geometry.indices:
            return

        model_matrix = mesh.get_world_matrix()
        mvp_matrix = view_projection * model_matrix

        vertices = geometry.vertices
        normals = geometry.normals if geometry.normals else []
        indices = geometry.indices

        transformed_vertices = []
        for vertex in vertices:
            v = Vector3(*vertex)
            clip_space = mvp_matrix * v
            transformed_vertices.append(clip_space)

        for i in range(0, len(indices), 3):
            if i + 2 >= len(indices):
                break

            i0, i1, i2 = indices[i], indices[i + 1], indices[i + 2]

            if i0 >= len(transformed_vertices) or i1 >= len(transformed_vertices) or i2 >= len(transformed_vertices):
                continue

            v0 = transformed_vertices[i0]
            v1 = transformed_vertices[i1]
            v2 = transformed_vertices[i2]

            if self.culling_enabled and self._is_back_facing(v0, v1, v2):
                continue

            ndc0 = self._to_ndc(v0)
            ndc1 = self._to_ndc(v1)
            ndc2 = self._to_ndc(v2)

            screen0 = self._ndc_to_screen(ndc0)
            screen1 = self._ndc_to_screen(ndc1)
            screen2 = self._ndc_to_screen(ndc2)

            color = self._calculate_color(material, lights, normals, i0 if i0 < len(normals) else None)
            self._rasterize_triangle(screen0, screen1, screen2, color)

    def _is_back_facing(self, v0, v1, v2):
        edge1 = Vector3(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
        edge2 = Vector3(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
        normal = edge1.cross(edge2)
        return normal.z < 0

    def _to_ndc(self, clip_space):
        if abs(clip_space.w) < 0.0001:
            return Vector3(clip_space.x, clip_space.y, clip_space.z)
        return Vector3(
            clip_space.x / clip_space.w,
            clip_space.y / clip_space.w,
            clip_space.z / clip_space.w
        )

    def _ndc_to_screen(self, ndc):
        x = (ndc.x + 1) * 0.5 * self.width
        y = (1 - ndc.y) * 0.5 * self.height
        return Vector3(x, y, ndc.z)

    def _calculate_color(self, material, lights, normals, normal_index):
        if hasattr(material, 'color'):
            base_color = material.color
        else:
            base_color = Vector3(0.8, 0.8, 0.8)

        if not lights or not normals or normal_index is None or normal_index >= len(normals):
            return [base_color.x, base_color.y, base_color.z, material.opacity]

        normal = Vector3(*normals[normal_index]).normalize()

        final_color = Vector3(0.1, 0.1, 0.1) * base_color

        for light in lights:
            light_intensity = light.intensity if hasattr(light, 'intensity') else 1.0
            light_color = light.color if hasattr(light, 'color') else Vector3(1, 1, 1)

            light_contribution = base_color * light_intensity * 0.5
            final_color = final_color + Vector3(
                light_contribution.x * light_color.x,
                light_contribution.y * light_color.y,
                light_contribution.z * light_color.z
            )

        final_color.x = min(1.0, final_color.x)
        final_color.y = min(1.0, final_color.y)
        final_color.z = min(1.0, final_color.z)

        return [final_color.x, final_color.y, final_color.z, material.opacity]

    def _rasterize_triangle(self, v0, v1, v2, color):
        min_x = int(max(0, min(v0.x, v1.x, v2.x)))
        max_x = int(min(self.width - 1, max(v0.x, v1.x, v2.x)))
        min_y = int(max(0, min(v0.y, v1.y, v2.y)))
        max_y = int(min(self.height - 1, max(v0.y, v1.y, v2.y)))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self._point_in_triangle(x, y, v0, v1, v2):
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.color_buffer[y, x] = color

    def _point_in_triangle(self, px, py, v0, v1, v2):
        def sign(p1x, p1y, p2x, p2y, p3x, p3y):
            return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)

        d1 = sign(px, py, v0.x, v0.y, v1.x, v1.y)
        d2 = sign(px, py, v1.x, v1.y, v2.x, v2.y)
        d3 = sign(px, py, v2.x, v2.y, v0.x, v0.y)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get_image_data(self):
        image_data = (self.color_buffer * 255).astype(np.uint8)
        return image_data

    def save_to_file(self, filename):
        from PIL import Image
        image_data = self.get_image_data()
        img = Image.fromarray(image_data, mode='RGBA')
        img.save(filename)
