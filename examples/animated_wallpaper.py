from openrakix import WallpaperEngine
from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import SphereGeometry
from openreactive.materials import StandardMaterial
from openreactive.renderer import Renderer
import math


scene = Scene("AnimatedWallpaper")

camera = PerspectiveCamera(fov=60, aspect=16/9, near=0.1, far=1000)
camera.transform.set_position(0, 3, 8)
camera.transform.look_at(Vector3(0, 0, 0))
scene.add(camera)

for i in range(5):
    sphere_geometry = SphereGeometry(0.5, 32, 16)
    sphere_material = StandardMaterial()
    sphere_material.color = Vector3(
        0.2 + i * 0.15,
        0.3 + i * 0.1,
        0.9 - i * 0.1
    )
    sphere_mesh = Mesh(sphere_geometry, sphere_material, f"Sphere{i}")
    angle = (i / 5) * math.pi * 2
    sphere_mesh.transform.set_position(
        math.cos(angle) * 3,
        0,
        math.sin(angle) * 3
    )
    scene.add(sphere_mesh)

renderer = Renderer(1920, 1080)
renderer.set_clear_color(0.05, 0.05, 0.1, 1.0)

engine = WallpaperEngine()
engine.initialize()
engine.set_resolution(1920, 1080)
engine.set_frame_rate(30)
engine.set_renderer(renderer)
engine.set_scene(scene)

rotation = 0

def update_callback(scene):
    global rotation
    rotation += 0.02

    for i, obj in enumerate(scene.children):
        if hasattr(obj, 'geometry'):
            angle = (i / 5) * math.pi * 2 + rotation
            obj.transform.set_position(
                math.cos(angle) * 3,
                math.sin(rotation * 2 + i) * 0.5,
                math.sin(angle) * 3
            )
            obj.transform.set_rotation_euler(rotation, rotation * 0.5, 0)

print("Starting animated wallpaper... Press Ctrl+C to stop")
try:
    engine.start_live_wallpaper(update_callback)
except KeyboardInterrupt:
    print("\nStopping...")
    engine.stop()
