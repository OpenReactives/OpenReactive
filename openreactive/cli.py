import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import BoxGeometry, SphereGeometry, PlaneGeometry
from openreactive.materials import StandardMaterial
from openreactive.renderer import Renderer
from openreactive.exporters import JavaScriptExporter, CSSExporter, HTMLExporter


@click.group()
@click.version_option(version='1.0.0')
def main():
    """OpenReactive - 3D Scene Processing and Projection System"""
    pass


@main.command()
@click.option('--output', '-o', default='scene.js', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['js', 'threejs', 'babylon']), default='js', help='Export format')
def create_demo(output, format):
    """Create a demo 3D scene and export it"""
    click.echo("Creating demo scene...")

    scene = Scene("DemoScene")

    camera = PerspectiveCamera(fov=60, aspect=16/9, near=0.1, far=1000)
    camera.transform.set_position(0, 2, 5)
    camera.transform.look_at(Vector3(0, 0, 0))
    scene.add(camera)

    box_geometry = BoxGeometry(1, 1, 1)
    box_material = StandardMaterial()
    box_material.color = Vector3(1, 0, 0)
    box_mesh = Mesh(box_geometry, box_material, "RedBox")
    box_mesh.transform.set_position(-2, 0, 0)
    scene.add(box_mesh)

    sphere_geometry = SphereGeometry(0.5, 32, 16)
    sphere_material = StandardMaterial()
    sphere_material.color = Vector3(0, 1, 0)
    sphere_mesh = Mesh(sphere_geometry, sphere_material, "GreenSphere")
    sphere_mesh.transform.set_position(0, 0, 0)
    scene.add(sphere_mesh)

    plane_geometry = PlaneGeometry(10, 10)
    plane_material = StandardMaterial()
    plane_material.color = Vector3(0.5, 0.5, 0.5)
    plane_mesh = Mesh(plane_geometry, plane_material, "GroundPlane")
    plane_mesh.transform.set_position(0, -1, 0)
    plane_mesh.transform.rotate_euler(1.57, 0, 0)
    scene.add(plane_mesh)

    exporter = JavaScriptExporter()
    if format == 'threejs':
        exporter.use_three_js = True
    elif format == 'babylon':
        exporter.use_babylon_js = True

    exporter.export_scene(scene, camera, output)
    click.echo(f"Scene exported to {output}")


@main.command()
@click.option('--width', '-w', default=800, help='Render width')
@click.option('--height', '-h', default=600, help='Render height')
@click.option('--output', '-o', default='render.png', help='Output image path')
def render_demo(width, height, output):
    """Render a demo scene to an image"""
    click.echo(f"Rendering scene at {width}x{height}...")

    scene = Scene("RenderDemo")

    camera = PerspectiveCamera(fov=60, aspect=width/height, near=0.1, far=1000)
    camera.transform.set_position(0, 2, 5)
    camera.transform.look_at(Vector3(0, 0, 0))
    scene.add(camera)

    sphere_geometry = SphereGeometry(1, 32, 16)
    sphere_material = StandardMaterial()
    sphere_material.color = Vector3(0.8, 0.4, 0.2)
    sphere_mesh = Mesh(sphere_geometry, sphere_material, "Sphere")
    scene.add(sphere_mesh)

    renderer = Renderer(width, height)
    renderer.set_clear_color(0.1, 0.1, 0.1, 1.0)
    renderer.render(scene, camera)
    renderer.save_screenshot(output)

    click.echo(f"Render saved to {output}")


@main.command()
@click.option('--output', '-o', default='scene.html', help='Output HTML file path')
@click.option('--format', '-f', type=click.Choice(['canvas', 'svg', 'webgl']), default='canvas', help='HTML format')
def export_html(output, format):
    """Export a scene to HTML"""
    click.echo(f"Exporting scene to HTML ({format})...")

    scene = Scene("HTMLScene")

    camera = PerspectiveCamera(fov=60, aspect=16/9)
    camera.transform.set_position(0, 0, 5)
    scene.add(camera)

    box_geometry = BoxGeometry(1, 1, 1)
    box_material = StandardMaterial()
    box_material.color = Vector3(0.2, 0.6, 0.9)
    box_mesh = Mesh(box_geometry, box_material, "Box")
    scene.add(box_mesh)

    exporter = HTMLExporter()
    if format == 'canvas':
        exporter.use_canvas = True
        exporter.use_webgl = False
    elif format == 'webgl':
        exporter.use_webgl = True
        exporter.use_canvas = False
    else:
        exporter.use_canvas = False
        exporter.use_webgl = False

    exporter.export_scene(scene, camera, output)
    click.echo(f"HTML scene exported to {output}")


@main.command()
@click.option('--output', '-o', default='scene.html', help='Output HTML file path')
def export_css(output):
    """Export a scene to CSS 3D"""
    click.echo("Exporting scene to CSS 3D...")

    scene = Scene("CSSScene")

    camera = PerspectiveCamera(fov=60, aspect=16/9)
    camera.transform.set_position(0, 0, 5)
    scene.add(camera)

    for i in range(3):
        box_geometry = BoxGeometry(1, 1, 1)
        box_material = StandardMaterial()
        box_material.color = Vector3(i * 0.3, (3 - i) * 0.3, 0.5)
        box_mesh = Mesh(box_geometry, box_material, f"Box{i}")
        box_mesh.transform.set_position(i - 1, 0, 0)
        scene.add(box_mesh)

    exporter = CSSExporter()
    result = exporter.export_scene(scene, camera, output)

    click.echo(f"CSS 3D scene exported to {output}")


@main.command()
@click.argument('scene_file')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['js', 'html', 'css']), default='js', help='Export format')
def export(scene_file, output, format):
    """Export a scene file to various formats"""
    click.echo(f"Exporting {scene_file}...")
    click.echo("Scene loading from file not implemented - use create-demo instead")


@main.command()
def info():
    """Display OpenReactive system information"""
    click.echo("OpenReactive v1.0.0")
    click.echo("3D Scene Processing and Projection System")
    click.echo("")
    click.echo("Features:")
    click.echo("  - Full 3D math library (vectors, matrices, quaternions)")
    click.echo("  - Scene graph with transform hierarchy")
    click.echo("  - Geometry primitives (box, sphere, plane, cylinder, cone, torus)")
    click.echo("  - Material system (Standard, Shader)")
    click.echo("  - OpenGL-style rendering pipeline")
    click.echo("  - JavaScript export (standalone, Three.js, Babylon.js)")
    click.echo("  - CSS 3D transforms export")
    click.echo("  - HTML Canvas/SVG/WebGL export")
    click.echo("")
    click.echo("Commands:")
    click.echo("  create-demo  - Create and export a demo scene")
    click.echo("  render-demo  - Render a demo scene to image")
    click.echo("  export-html  - Export scene to HTML")
    click.echo("  export-css   - Export scene to CSS 3D")
    click.echo("  info         - Display this information")


if __name__ == '__main__':
    main()
