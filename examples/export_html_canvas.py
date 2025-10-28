from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import BoxGeometry, SphereGeometry, ConeGeometry
from openreactive.materials import StandardMaterial
from openreactive.exporters import HTMLExporter


scene = Scene("HTMLCanvasScene")

camera = PerspectiveCamera(fov=60, aspect=16/9)
camera.transform.set_position(0, 2, 5)
scene.add(camera)

box_geometry = BoxGeometry(1, 1, 1)
box_material = StandardMaterial()
box_material.color = Vector3(0.9, 0.2, 0.3)
box_mesh = Mesh(box_geometry, box_material, "RedBox")
box_mesh.transform.set_position(-2, 0, 0)
scene.add(box_mesh)

sphere_geometry = SphereGeometry(0.6, 32, 16)
sphere_material = StandardMaterial()
sphere_material.color = Vector3(0.2, 0.8, 0.4)
sphere_mesh = Mesh(sphere_geometry, sphere_material, "GreenSphere")
sphere_mesh.transform.set_position(0, 0, 0)
scene.add(sphere_mesh)

cone_geometry = ConeGeometry(0.5, 1.5, 32)
cone_material = StandardMaterial()
cone_material.color = Vector3(0.3, 0.4, 0.9)
cone_mesh = Mesh(cone_geometry, cone_material, "BlueCone")
cone_mesh.transform.set_position(2, 0, 0)
scene.add(cone_mesh)

exporter = HTMLExporter()
exporter.use_canvas = True
exporter.use_webgl = False

exporter.export_scene(scene, camera, "canvas_scene.html")

print("HTML Canvas scene exported to canvas_scene.html")
