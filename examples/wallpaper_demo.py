from openrakix import WallpaperEngine
from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import SphereGeometry, BoxGeometry
from openreactive.materials import StandardMaterial
from openreactive.renderer import Renderer


scene = Scene("WallpaperScene")

camera = PerspectiveCamera(fov=60, aspect=16/9, near=0.1, far=1000)
camera.transform.set_position(0, 3, 6)
camera.transform.look_at(Vector3(0, 0, 0))
scene.add(camera)

sphere_geometry = SphereGeometry(1.5, 32, 16)
sphere_material = StandardMaterial()
sphere_material.color = Vector3(0.3, 0.7, 0.9)
sphere_mesh = Mesh(sphere_geometry, sphere_material, "MainSphere")
scene.add(sphere_mesh)

box_geometry = BoxGeometry(0.8, 0.8, 0.8)
box_material = StandardMaterial()
box_material.color = Vector3(0.9, 0.3, 0.4)
box_mesh = Mesh(box_geometry, box_material, "Cube")
box_mesh.transform.set_position(-3, 0, 0)
scene.add(box_mesh)

renderer = Renderer(1920, 1080)
renderer.set_clear_color(0.05, 0.05, 0.15, 1.0)

engine = WallpaperEngine()
engine.initialize()
engine.set_resolution(1920, 1080)
engine.set_renderer(renderer)

engine.render_to_wallpaper(scene, camera)

print("3D scene rendered to wallpaper!")
