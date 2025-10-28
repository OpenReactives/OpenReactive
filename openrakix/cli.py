import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openrakix import WallpaperEngine, Compositor
from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import SphereGeometry, BoxGeometry
from openreactive.materials import StandardMaterial
from openreactive.renderer import Renderer


@click.group()
@click.version_option(version='1.0.0')
def main():
    """OpenRakix (OpenRX) - 3D Scene to OS Wallpaper Engine"""
    pass


@main.command()
@click.option('--platform', '-p', type=click.Choice(['linux', 'macos', 'windows', 'auto']), default='auto', help='Target platform')
def init(platform):
    """Initialize OpenRakix for your platform"""
    click.echo("Initializing OpenRakix...")

    if platform == 'auto':
        platform = None

    engine = WallpaperEngine()
    engine.initialize(platform)

    click.echo(f"OpenRakix initialized successfully")


@main.command()
@click.argument('image_path')
def set_wallpaper(image_path):
    """Set a static image as wallpaper"""
    if not os.path.exists(image_path):
        click.echo(f"Error: Image file not found: {image_path}", err=True)
        return

    click.echo(f"Setting wallpaper to {image_path}...")

    engine = WallpaperEngine()
    engine.initialize()
    engine.set_wallpaper(image_path)

    click.echo("Wallpaper set successfully")


@main.command()
@click.option('--width', '-w', default=1920, help='Wallpaper width')
@click.option('--height', '-h', default=1080, help='Wallpaper height')
def render_scene(width, height):
    """Render a 3D scene to wallpaper"""
    click.echo(f"Rendering 3D scene at {width}x{height}...")

    scene = Scene("WallpaperScene")

    camera = PerspectiveCamera(fov=60, aspect=width/height, near=0.1, far=1000)
    camera.transform.set_position(0, 2, 5)
    camera.transform.look_at(Vector3(0, 0, 0))
    scene.add(camera)

    sphere_geometry = SphereGeometry(1, 32, 16)
    sphere_material = StandardMaterial()
    sphere_material.color = Vector3(0.3, 0.6, 0.9)
    sphere_mesh = Mesh(sphere_geometry, sphere_material, "Sphere")
    sphere_mesh.transform.set_position(0, 0, 0)
    scene.add(sphere_mesh)

    box_geometry = BoxGeometry(0.5, 0.5, 0.5)
    box_material = StandardMaterial()
    box_material.color = Vector3(0.9, 0.4, 0.2)
    box_mesh = Mesh(box_geometry, box_material, "Box")
    box_mesh.transform.set_position(-2, 0, 0)
    scene.add(box_mesh)

    renderer = Renderer(width, height)
    renderer.set_clear_color(0.1, 0.1, 0.15, 1.0)

    engine = WallpaperEngine()
    engine.initialize()
    engine.set_resolution(width, height)
    engine.set_renderer(renderer)
    engine.render_to_wallpaper(scene, camera)

    click.echo("3D scene rendered to wallpaper successfully")


@main.command()
@click.option('--width', '-w', default=1920, help='Wallpaper width')
@click.option('--height', '-h', default=1080, help='Wallpaper height')
@click.option('--fps', '-f', default=30, help='Frame rate')
@click.option('--duration', '-d', default=0, help='Duration in seconds (0 = infinite)')
def live_wallpaper(width, height, fps, duration):
    """Start a live animated 3D wallpaper"""
    click.echo(f"Starting live wallpaper at {width}x{height} @ {fps} FPS...")

    scene = Scene("LiveWallpaperScene")

    camera = PerspectiveCamera(fov=60, aspect=width/height, near=0.1, far=1000)
    camera.transform.set_position(0, 3, 6)
    camera.transform.look_at(Vector3(0, 0, 0))
    scene.add(camera)

    sphere_geometry = SphereGeometry(1, 32, 16)
    sphere_material = StandardMaterial()
    sphere_material.color = Vector3(0.3, 0.6, 0.9)
    sphere_mesh = Mesh(sphere_geometry, sphere_material, "AnimatedSphere")
    scene.add(sphere_mesh)

    renderer = Renderer(width, height)
    renderer.set_clear_color(0.05, 0.05, 0.1, 1.0)

    engine = WallpaperEngine()
    engine.initialize()
    engine.set_resolution(width, height)
    engine.set_frame_rate(fps)
    engine.set_renderer(renderer)
    engine.set_scene(scene)

    import time
    start_time = time.time()
    rotation = 0

    def update_callback(scene):
        nonlocal rotation
        rotation += 0.02

        for obj in scene.children:
            if hasattr(obj, 'geometry'):
                obj.transform.rotation = obj.transform.rotation
                obj.transform.set_rotation_euler(0, rotation, 0)

        if duration > 0 and time.time() - start_time > duration:
            engine.stop()

    click.echo("Live wallpaper running... Press Ctrl+C to stop")

    try:
        engine.start_live_wallpaper(update_callback)
    except KeyboardInterrupt:
        click.echo("\nStopping live wallpaper...")
        engine.stop()


@main.command()
@click.argument('image_path')
@click.option('--effect', '-e', multiple=True, help='Apply effects (blur, sepia, vignette, etc.)')
def apply_effects(image_path, effect):
    """Apply post-processing effects to an image and set as wallpaper"""
    if not os.path.exists(image_path):
        click.echo(f"Error: Image file not found: {image_path}", err=True)
        return

    click.echo(f"Applying effects to {image_path}...")

    from PIL import Image
    import numpy as np

    img = Image.open(image_path)
    img_data = np.array(img).astype(np.float32) / 255.0

    compositor = Compositor()
    for effect_name in effect:
        click.echo(f"  - Applying {effect_name}")
        if effect_name == 'blur':
            compositor.add_effect('blur', radius=5)
        elif effect_name == 'sepia':
            compositor.add_effect('sepia')
        elif effect_name == 'vignette':
            compositor.add_effect('vignette', strength=0.6)
        elif effect_name == 'grayscale':
            compositor.add_effect('grayscale')
        elif effect_name == 'wave':
            compositor.add_effect('wave', amplitude=15, frequency=0.01)
        else:
            compositor.add_effect(effect_name)

    processed_data = compositor.process(img_data)

    temp_path = "/tmp/openrx_processed.png"
    processed_img = (processed_data * 255).astype(np.uint8)
    Image.fromarray(processed_img).save(temp_path)

    engine = WallpaperEngine()
    engine.initialize()
    engine.set_wallpaper(temp_path)

    click.echo(f"Effects applied and wallpaper set successfully")


@main.command()
def list_effects():
    """List all available post-processing effects"""
    click.echo("Available Effects:")
    click.echo("  blur             - Gaussian blur")
    click.echo("  sharpen          - Sharpen image")
    click.echo("  edge_enhance     - Enhance edges")
    click.echo("  emboss           - Emboss effect")
    click.echo("  brightness       - Adjust brightness")
    click.echo("  contrast         - Adjust contrast")
    click.echo("  saturation       - Adjust color saturation")
    click.echo("  grayscale        - Convert to grayscale")
    click.echo("  sepia            - Apply sepia tone")
    click.echo("  vignette         - Add vignette effect")
    click.echo("  chromatic_aberration - Chromatic aberration")
    click.echo("  pixelate         - Pixelate effect")
    click.echo("  wave             - Wave distortion")


@main.command()
def info():
    """Display OpenRakix system information"""
    click.echo("OpenRakix (OpenRX) v1.0.0")
    click.echo("The Eternal Library for OS Wallpaper Projection")
    click.echo("")
    click.echo("Features:")
    click.echo("  - Cross-platform wallpaper management (Linux, macOS, Windows)")
    click.echo("  - 3D scene rendering to wallpaper")
    click.echo("  - Live animated wallpapers")
    click.echo("  - Post-processing effects (blur, sepia, vignette, etc.)")
    click.echo("  - Desktop environment detection (GNOME, KDE, XFCE, etc.)")
    click.echo("")
    click.echo("Supported Platforms:")
    click.echo("  Linux:")
    click.echo("    - GNOME (gsettings)")
    click.echo("    - KDE Plasma (qdbus)")
    click.echo("    - XFCE (xfconf-query)")
    click.echo("    - MATE (gsettings)")
    click.echo("    - Generic (feh, nitrogen)")
    click.echo("  macOS:")
    click.echo("    - AppleScript")
    click.echo("  Windows:")
    click.echo("    - Win32 API")
    click.echo("")
    click.echo("Commands:")
    click.echo("  init           - Initialize OpenRakix")
    click.echo("  set-wallpaper  - Set static image as wallpaper")
    click.echo("  render-scene   - Render 3D scene to wallpaper")
    click.echo("  live-wallpaper - Start animated wallpaper")
    click.echo("  apply-effects  - Apply effects and set wallpaper")
    click.echo("  list-effects   - List available effects")
    click.echo("  info           - Display this information")


if __name__ == '__main__':
    main()
