from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import BoxGeometry
from openreactive.materials import StandardMaterial
from openreactive.exporters import CSSExporter
import math


scene = Scene("CSS3DScene")

camera = PerspectiveCamera(fov=60, aspect=16/9)
camera.transform.set_position(0, 0, 5)
scene.add(camera)

colors = [
    Vector3(1, 0.2, 0.2),
    Vector3(0.2, 1, 0.2),
    Vector3(0.2, 0.2, 1),
    Vector3(1, 1, 0.2),
    Vector3(1, 0.2, 1)
]

for i in range(5):
    box_geometry = BoxGeometry(1, 1, 1)
    box_material = StandardMaterial()
    box_material.color = colors[i]
    box_mesh = Mesh(box_geometry, box_material, f"Box{i}")

    angle = (i / 5) * math.pi * 2
    radius = 2
    box_mesh.transform.set_position(
        math.cos(angle) * radius,
        math.sin(i) * 0.5,
        math.sin(angle) * radius
    )
    box_mesh.transform.rotate_euler(i * 0.5, i * 0.3, 0)

    scene.add(box_mesh)

exporter = CSSExporter()
exporter.perspective = 1200

result = exporter.export_scene(scene, camera, "css_3d_scene.html")

print("CSS 3D scene exported to css_3d_scene.html")
print("Open in a browser to see the interactive 3D scene!")
