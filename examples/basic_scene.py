from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import BoxGeometry, SphereGeometry
from openreactive.materials import StandardMaterial
from openreactive.renderer import Renderer
from openreactive.exporters import JavaScriptExporter


scene = Scene("BasicScene")

camera = PerspectiveCamera(fov=60, aspect=16/9, near=0.1, far=1000)
camera.transform.set_position(0, 2, 5)
camera.transform.look_at(Vector3(0, 0, 0))
scene.add(camera)

box_geometry = BoxGeometry(1, 1, 1)
box_material = StandardMaterial()
box_material.color = Vector3(1, 0.5, 0.2)
box_mesh = Mesh(box_geometry, box_material, "Box")
scene.add(box_mesh)

sphere_geometry = SphereGeometry(0.5, 32, 16)
sphere_material = StandardMaterial()
sphere_material.color = Vector3(0.2, 0.6, 0.9)
sphere_mesh = Mesh(sphere_geometry, sphere_material, "Sphere")
sphere_mesh.transform.set_position(2, 0, 0)
scene.add(sphere_mesh)

renderer = Renderer(800, 600)
renderer.render(scene, camera)
renderer.save_screenshot("output.png")

exporter = JavaScriptExporter()
exporter.export_scene(scene, camera, "scene.js")

print("Scene created and exported successfully!")
