# OpenReactive Documentation

## Overview

OpenReactive is an OpenGL-esque 3D processing system that allows you to create, manipulate, and project 3D scenes onto JavaScript, CSS, and HTML formats. It includes the eternal library OpenRakix (OpenRX) for projecting 3D scenes directly onto your operating system wallpaper.

## Features

### Core Features
- Full 3D mathematics library (Vector3, Vector4, Matrix4, Quaternion)
- Scene graph with hierarchical transforms
- Camera systems (Perspective, Orthographic)
- Lighting (Directional, Point, Spot, Ambient)
- Geometry primitives (Box, Sphere, Plane, Cylinder, Cone, Torus)
- Material system (Standard, Shader)
- OpenGL-style rendering pipeline

### Export Capabilities
- **JavaScript Export**: Standalone, Three.js, or Babylon.js compatible
- **CSS Export**: CSS 3D transforms with interactive controls
- **HTML Export**: Canvas 2D, SVG, or WebGL rendering

### OpenRakix (OpenRX)
- Cross-platform wallpaper management
- Live animated wallpapers
- Post-processing effects
- Desktop environment detection

## Installation

```bash
pip install -e .
```

## Quick Start

### Creating a Basic Scene

```python
from openreactive import Scene, Vector3, Mesh, PerspectiveCamera
from openreactive.geometry import SphereGeometry
from openreactive.materials import StandardMaterial

scene = Scene("MyScene")

camera = PerspectiveCamera(fov=60, aspect=16/9)
camera.transform.set_position(0, 0, 5)
scene.add(camera)

sphere = SphereGeometry(1, 32, 16)
material = StandardMaterial()
material.color = Vector3(0.3, 0.6, 0.9)
mesh = Mesh(sphere, material)
scene.add(mesh)
```

### Rendering to Image

```python
from openreactive.renderer import Renderer

renderer = Renderer(800, 600)
renderer.render(scene, camera)
renderer.save_screenshot("output.png")
```

### Exporting to JavaScript

```python
from openreactive.exporters import JavaScriptExporter

exporter = JavaScriptExporter()
exporter.use_three_js = True
exporter.export_scene(scene, camera, "scene.js")
```

### Setting Wallpaper with OpenRakix

```python
from openrakix import WallpaperEngine

engine = WallpaperEngine()
engine.initialize()
engine.set_renderer(renderer)
engine.render_to_wallpaper(scene, camera)
```

## CLI Commands

### OpenReactive

```bash
openreactive create-demo --output scene.js --format threejs
openreactive render-demo --width 1920 --height 1080 --output render.png
openreactive export-html --output scene.html --format canvas
openreactive export-css --output scene.html
openreactive info
```

### OpenRakix (OpenRX)

```bash
openrx init --platform auto
openrx set-wallpaper image.png
openrx render-scene --width 1920 --height 1080
openrx live-wallpaper --fps 30
openrx apply-effects image.png --effect blur --effect vignette
openrx list-effects
openrx info
```

## Core API

### Vector3

```python
v = Vector3(x, y, z)
v.length()
v.normalize()
v.dot(other)
v.cross(other)
```

### Matrix4

```python
m = Matrix4.identity()
m = Matrix4.translation(x, y, z)
m = Matrix4.rotation_y(angle)
m = Matrix4.perspective(fov, aspect, near, far)
result = m1 * m2
```

### Transform

```python
transform = Transform()
transform.set_position(x, y, z)
transform.set_rotation_euler(x, y, z)
transform.set_scale(x, y, z)
transform.rotate(axis, angle)
transform.look_at(target)
```

### Scene Graph

```python
scene = Scene("MyScene")
parent = Object3D("Parent")
child = Object3D("Child")
parent.add(child)
scene.add(parent)
scene.traverse(callback)
```

### Geometries

```python
BoxGeometry(width, height, depth, w_seg, h_seg, d_seg)
SphereGeometry(radius, width_seg, height_seg)
PlaneGeometry(width, height, w_seg, h_seg)
CylinderGeometry(radius_top, radius_bottom, height, radial_seg, height_seg)
ConeGeometry(radius, height, radial_seg)
TorusGeometry(radius, tube, radial_seg, tubular_seg)
```

### Materials

```python
material = StandardMaterial()
material.color = Vector3(r, g, b)
material.metalness = 0.5
material.roughness = 0.5
material.opacity = 1.0
material.transparent = False

shader_material = ShaderMaterial(vertex_shader, fragment_shader)
shader_material.set_uniform("time", 0.0)
```

### Cameras

```python
camera = PerspectiveCamera(fov=60, aspect=16/9, near=0.1, far=1000)
camera = OrthographicCamera(left, right, top, bottom, near, far)
camera.transform.set_position(0, 0, 5)
camera.update_projection_matrix()
```

### Lights

```python
DirectionalLight(color, intensity)
PointLight(color, intensity, distance, decay)
SpotLight(color, intensity, distance, angle, penumbra, decay)
AmbientLight(color, intensity)
```

## OpenRakix API

### WallpaperEngine

```python
engine = WallpaperEngine()
engine.initialize(platform="linux")
engine.set_resolution(1920, 1080)
engine.set_frame_rate(30)
engine.set_renderer(renderer)
engine.set_scene(scene)
engine.render_to_wallpaper(scene, camera)
engine.start_live_wallpaper(update_callback)
engine.stop()
```

### Compositor

```python
compositor = Compositor()
compositor.add_effect("blur", radius=5)
compositor.add_effect("vignette", strength=0.6)
compositor.add_effect("chromatic_aberration", offset=5)
processed = compositor.process(frame_data)
```

### Effects

Available effects:
- blur
- sharpen
- edge_enhance
- emboss
- brightness
- contrast
- saturation
- grayscale
- sepia
- vignette
- chromatic_aberration
- pixelate
- wave

## Platform Support

### Linux
- GNOME (gsettings)
- KDE Plasma (qdbus)
- XFCE (xfconf-query)
- MATE (gsettings)
- Generic (feh, nitrogen)

### macOS
- AppleScript integration

### Windows
- Win32 API

## Examples

See the `examples/` directory for complete working examples:
- `basic_scene.py` - Create and render a basic 3D scene
- `wallpaper_demo.py` - Render scene to OS wallpaper
- `animated_wallpaper.py` - Live animated wallpaper
- `export_html_canvas.py` - Export to HTML Canvas
- `export_css_3d.py` - Export to CSS 3D
- `export_threejs.py` - Export to Three.js

## Advanced Usage

### Custom Geometry

```python
geometry = Geometry()
geometry.vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
geometry.indices = [0, 1, 2]
geometry.compute_vertex_normals()
```

### Shader Materials

```python
vertex_shader = """
attribute vec3 position;
uniform mat4 mvp;
void main() {
    gl_Position = mvp * vec4(position, 1.0);
}
"""

fragment_shader = """
uniform vec3 color;
void main() {
    gl_FragColor = vec4(color, 1.0);
}
"""

material = ShaderMaterial(vertex_shader, fragment_shader)
material.set_uniform("color", [1, 0, 0])
```

### Scene Hierarchies

```python
root = Object3D("Root")
child1 = Mesh(geometry, material, "Child1")
child2 = Mesh(geometry, material, "Child2")

child1.transform.set_position(1, 0, 0)
child2.transform.set_position(-1, 0, 0)

root.add(child1)
root.add(child2)
scene.add(root)

root.transform.rotate_euler(0, 0.1, 0)
```

## License

MIT License

## Contributing

Contributions welcome! This is a complete implementation with all functionality.
