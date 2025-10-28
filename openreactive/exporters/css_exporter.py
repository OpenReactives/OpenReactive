from jinja2 import Template
import math


class CSSExporter:
    def __init__(self):
        self.use_3d_transforms = True
        self.perspective = 1000
        self.preserve_3d = True

    def export_scene(self, scene, camera=None, output_path=None):
        css_code = self._generate_css(scene, camera)
        html_structure = self._generate_html_structure(scene)

        result = {
            "css": css_code,
            "html": html_structure
        }

        if output_path:
            css_path = output_path.replace('.html', '.css')
            with open(css_path, 'w') as f:
                f.write(css_code)
            with open(output_path, 'w') as f:
                f.write(html_structure)

        return result

    def _generate_css(self, scene, camera):
        css_rules = []

        css_rules.append('''
/* OpenReactive CSS 3D Export */
.scene-container {
    perspective: ''' + str(self.perspective) + '''px;
    perspective-origin: 50% 50%;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
}

.scene {
    transform-style: preserve-3d;
    position: absolute;
    width: 100%;
    height: 100%;
    transform-origin: center center;
}

.object3d {
    transform-style: preserve-3d;
    position: absolute;
    transition: transform 0.3s ease;
}

.mesh {
    transform-style: preserve-3d;
    position: absolute;
}
''')

        def generate_object_css(obj, parent_id=""):
            obj_id = f"obj-{obj.id}"
            position = obj.transform.position
            scale = obj.transform.scale
            rotation = obj.transform.rotation.to_euler()

            transform_parts = []
            transform_parts.append(f"translate3d({position.x * 100}px, {-position.y * 100}px, {position.z * 100}px)")
            transform_parts.append(f"rotateX({rotation.x}rad)")
            transform_parts.append(f"rotateY({rotation.y}rad)")
            transform_parts.append(f"rotateZ({rotation.z}rad)")
            transform_parts.append(f"scale3d({scale.x}, {scale.y}, {scale.z})")

            transform_value = " ".join(transform_parts)

            rule = f'''
#{obj_id} {{
    transform: {transform_value};
    opacity: {1 if obj.visible else 0};
}}
'''
            css_rules.append(rule)

            if hasattr(obj, 'material') and obj.material:
                material = obj.material
                if hasattr(material, 'color'):
                    color = material.color
                    rgb = f"rgb({int(color.x * 255)}, {int(color.y * 255)}, {int(color.z * 255)})"
                    material_rule = f'''
#{obj_id} .mesh-face {{
    background-color: {rgb};
    opacity: {material.opacity};
}}
'''
                    css_rules.append(material_rule)

        scene.traverse(generate_object_css)

        return "\n".join(css_rules)

    def _generate_html_structure(self, scene):
        html_parts = []

        html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenReactive CSS 3D Scene</title>
    <link rel="stylesheet" href="scene.css">
    <style>
        body { margin: 0; padding: 0; overflow: hidden; }
    </style>
</head>
<body>
    <div class="scene-container">
        <div class="scene">
''')

        def generate_object_html(obj, depth=0):
            indent = "            " + "    " * depth
            obj_id = f"obj-{obj.id}"
            class_name = "object3d"

            if hasattr(obj, 'geometry'):
                class_name = "mesh"

            html = f'{indent}<div id="{obj_id}" class="{class_name}" data-name="{obj.name}">\n'

            if hasattr(obj, 'geometry') and obj.geometry:
                html += f'{indent}    <div class="mesh-face"></div>\n'

            for child in obj.children:
                html += generate_object_html(child, depth + 1)

            html += f'{indent}</div>\n'
            return html

        for child in scene.children:
            html_parts.append(generate_object_html(child))

        html_parts.append('''        </div>
    </div>
    <script>
        const scene = document.querySelector('.scene');
        let mouseX = 0, mouseY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = (e.clientY / window.innerHeight) * 2 - 1;
            scene.style.transform = `rotateY(${mouseX * 20}deg) rotateX(${-mouseY * 20}deg)`;
        });
    </script>
</body>
</html>''')

        return "\n".join(html_parts)

    def export_animation(self, scene, keyframes, duration=1.0, output_path=None):
        animation_css = self._generate_animation_css(scene, keyframes, duration)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(animation_css)

        return animation_css

    def _generate_animation_css(self, scene, keyframes, duration):
        animations = []

        for obj_id, frames in keyframes.items():
            animation_name = f"anim-{obj_id}"
            keyframe_css = f"@keyframes {animation_name} {{\n"

            for percent, transform in frames:
                keyframe_css += f"    {percent}% {{\n"
                keyframe_css += f"        transform: {transform};\n"
                keyframe_css += f"    }}\n"

            keyframe_css += "}\n\n"

            animations.append(keyframe_css)

            animations.append(f"#obj-{obj_id} {{\n")
            animations.append(f"    animation: {animation_name} {duration}s ease-in-out infinite;\n")
            animations.append(f"}}\n\n")

        return "".join(animations)
