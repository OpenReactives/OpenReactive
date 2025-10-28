from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import SphereGeometry, TorusGeometry
from openreactive.materials import StandardMaterial
from openreactive.exporters import JavaScriptExporter


scene = Scene("ThreeJSScene")

camera = PerspectiveCamera(fov=75, aspect=16/9, near=0.1, far=1000)
camera.transform.set_position(0, 3, 5)
camera.transform.look_at(Vector3(0, 0, 0))
scene.add(camera)

sphere_geometry = SphereGeometry(1, 32, 16)
sphere_material = StandardMaterial()
sphere_material.color = Vector3(0.3, 0.6, 0.9)
sphere_material.metalness = 0.8
sphere_material.roughness = 0.2
sphere_mesh = Mesh(sphere_geometry, sphere_material, "MetallicSphere")
scene.add(sphere_mesh)

torus_geometry = TorusGeometry(1.5, 0.3, 16, 100)
torus_material = StandardMaterial()
torus_material.color = Vector3(0.9, 0.3, 0.5)
torus_material.metalness = 0.3
torus_material.roughness = 0.7
torus_mesh = Mesh(torus_geometry, torus_material, "Torus")
torus_mesh.transform.rotate_euler(1.57, 0, 0)
scene.add(torus_mesh)

exporter = JavaScriptExporter()
exporter.use_three_js = True

exporter.export_scene(scene, camera, "threejs_scene.js")

print("Three.js scene exported to threejs_scene.js")
print("Import this in your Three.js project!")
