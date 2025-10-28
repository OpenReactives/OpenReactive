from jinja2 import Template
import json


class HTMLExporter:
    def __init__(self):
        self.use_canvas = True
        self.use_webgl = False
        self.interactive = True

    def export_scene(self, scene, camera=None, output_path=None):
        if self.use_webgl:
            html_code = self._generate_webgl_html(scene, camera)
        elif self.use_canvas:
            html_code = self._generate_canvas_html(scene, camera)
        else:
            html_code = self._generate_svg_html(scene, camera)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(html_code)

        return html_code

    def _serialize_scene(self, scene, camera):
        data = {
            "scene": self._serialize_object(scene),
            "camera": self._serialize_object(camera) if camera else None
        }
        return data

    def _serialize_object(self, obj):
        if obj is None:
            return None

        data = {
            "id": obj.id,
            "name": obj.name,
            "type": obj.__class__.__name__,
            "position": obj.transform.position.to_array(),
            "rotation": [obj.transform.rotation.x, obj.transform.rotation.y,
                        obj.transform.rotation.z, obj.transform.rotation.w],
            "scale": obj.transform.scale.to_array(),
            "visible": obj.visible,
            "children": []
        }

        if hasattr(obj, 'geometry') and obj.geometry:
            data["geometry"] = {
                "vertices": obj.geometry.vertices,
                "indices": obj.geometry.indices.tolist() if hasattr(obj.geometry.indices, 'tolist') else obj.geometry.indices
            }

        if hasattr(obj, 'material') and obj.material:
            material_data = {"type": obj.material.type}
            if hasattr(obj.material, 'color'):
                material_data["color"] = obj.material.color.to_array()
            material_data["opacity"] = obj.material.opacity
            data["material"] = material_data

        for child in obj.children:
            data["children"].append(self._serialize_object(child))

        return data

    def _generate_canvas_html(self, scene, camera):
        scene_data = self._serialize_scene(scene, camera)

        template = Template('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenReactive Canvas Scene</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a1a;
        }
        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <canvas id="scene-canvas"></canvas>
    <div id="info">
        <div>OpenReactive Scene</div>
        <div>Objects: <span id="object-count">0</span></div>
        <div>FPS: <span id="fps">0</span></div>
    </div>

    <script>
        const sceneData = {{ scene_json }};
        const canvas = document.getElementById('scene-canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        class Matrix4 {
            constructor() {
                this.elements = new Float32Array([
                    1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                ]);
            }

            multiply(other) {
                const result = new Matrix4();
                const a = this.elements;
                const b = other.elements;
                const r = result.elements;

                for (let i = 0; i < 4; i++) {
                    for (let j = 0; j < 4; j++) {
                        r[i * 4 + j] =
                            a[i * 4 + 0] * b[0 * 4 + j] +
                            a[i * 4 + 1] * b[1 * 4 + j] +
                            a[i * 4 + 2] * b[2 * 4 + j] +
                            a[i * 4 + 3] * b[3 * 4 + j];
                    }
                }

                return result;
            }

            static perspective(fov, aspect, near, far) {
                const mat = new Matrix4();
                const f = 1.0 / Math.tan(fov / 2);
                const rangeInv = 1.0 / (near - far);

                mat.elements[0] = f / aspect;
                mat.elements[5] = f;
                mat.elements[10] = (near + far) * rangeInv;
                mat.elements[11] = -1;
                mat.elements[14] = near * far * rangeInv * 2;
                mat.elements[15] = 0;

                return mat;
            }

            transformPoint(point) {
                const e = this.elements;
                const x = point[0], y = point[1], z = point[2];
                const w = e[3] * x + e[7] * y + e[11] * z + e[15];

                return [
                    (e[0] * x + e[4] * y + e[8] * z + e[12]) / w,
                    (e[1] * x + e[5] * y + e[9] * z + e[13]) / w,
                    (e[2] * x + e[6] * y + e[10] * z + e[14]) / w
                ];
            }
        }

        let objectCount = 0;
        let rotation = 0;

        function drawScene() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const camera = sceneData.camera || {
                fov: Math.PI / 3,
                aspect: canvas.width / canvas.height,
                near: 0.1,
                far: 1000,
                position: [0, 0, 5]
            };

            const projectionMatrix = Matrix4.perspective(
                camera.fov,
                camera.aspect,
                camera.near,
                camera.far
            );

            objectCount = 0;
            rotation += 0.01;

            function drawObject(obj) {
                if (!obj.visible) return;
                objectCount++;

                if (obj.type === 'Mesh' && obj.geometry) {
                    drawMesh(obj, projectionMatrix);
                }

                if (obj.children) {
                    obj.children.forEach(drawObject);
                }
            }

            drawObject(sceneData.scene);

            document.getElementById('object-count').textContent = objectCount;
        }

        function drawMesh(mesh, projectionMatrix) {
            const geometry = mesh.geometry;
            if (!geometry.vertices || !geometry.indices) return;

            const color = mesh.material?.color
                ? `rgb(${mesh.material.color[0] * 255}, ${mesh.material.color[1] * 255}, ${mesh.material.color[2] * 255})`
                : '#888888';

            ctx.strokeStyle = color;
            ctx.fillStyle = color;
            ctx.globalAlpha = mesh.material?.opacity || 1.0;

            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const scale = 200;

            for (let i = 0; i < geometry.indices.length; i += 3) {
                const i0 = geometry.indices[i];
                const i1 = geometry.indices[i + 1];
                const i2 = geometry.indices[i + 2];

                if (i0 >= geometry.vertices.length || i1 >= geometry.vertices.length || i2 >= geometry.vertices.length) {
                    continue;
                }

                const v0 = geometry.vertices[i0];
                const v1 = geometry.vertices[i1];
                const v2 = geometry.vertices[i2];

                const rotY = rotation;
                const rotX = rotation * 0.5;

                function rotatePoint(p) {
                    let [x, y, z] = p;

                    let cosY = Math.cos(rotY);
                    let sinY = Math.sin(rotY);
                    let nx = x * cosY + z * sinY;
                    let nz = -x * sinY + z * cosY;
                    x = nx;
                    z = nz;

                    let cosX = Math.cos(rotX);
                    let sinX = Math.sin(rotX);
                    let ny = y * cosX - z * sinX;
                    nz = y * sinX + z * cosX;
                    y = ny;
                    z = nz;

                    z += 5;

                    const perspective = 500 / (500 + z);
                    return [
                        centerX + x * scale * perspective,
                        centerY - y * scale * perspective
                    ];
                }

                const p0 = rotatePoint(v0);
                const p1 = rotatePoint(v1);
                const p2 = rotatePoint(v2);

                ctx.beginPath();
                ctx.moveTo(p0[0], p0[1]);
                ctx.lineTo(p1[0], p1[1]);
                ctx.lineTo(p2[0], p2[1]);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;
        }

        let lastTime = performance.now();
        let frameCount = 0;

        function animate() {
            drawScene();

            frameCount++;
            const currentTime = performance.now();
            if (currentTime - lastTime >= 1000) {
                document.getElementById('fps').textContent = frameCount;
                frameCount = 0;
                lastTime = currentTime;
            }

            requestAnimationFrame(animate);
        }

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        animate();
    </script>
</body>
</html>''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))

    def _generate_svg_html(self, scene, camera):
        scene_data = self._serialize_scene(scene, camera)

        template = Template('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenReactive SVG Scene</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a1a;
        }
        svg {
            width: 100vw;
            height: 100vh;
        }
    </style>
</head>
<body>
    <svg id="scene-svg" xmlns="http://www.w3.org/2000/svg">
        <g id="scene-group"></g>
    </svg>

    <script>
        const sceneData = {{ scene_json }};
        const svg = document.getElementById('scene-svg');
        const sceneGroup = document.getElementById('scene-group');

        function renderScene() {
            sceneGroup.innerHTML = '';

            function renderObject(obj, parentGroup) {
                if (!obj.visible) return;

                const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                group.setAttribute('id', obj.id);
                group.setAttribute('data-name', obj.name);

                if (obj.type === 'Mesh' && obj.geometry) {
                    renderMesh(obj, group);
                }

                if (obj.children) {
                    obj.children.forEach(child => renderObject(child, group));
                }

                parentGroup.appendChild(group);
            }

            renderObject(sceneData.scene, sceneGroup);
        }

        function renderMesh(mesh, group) {
            const geometry = mesh.geometry;
            if (!geometry.vertices || !geometry.indices) return;

            const color = mesh.material?.color
                ? `rgb(${mesh.material.color[0] * 255}, ${mesh.material.color[1] * 255}, ${mesh.material.color[2] * 255})`
                : '#888888';

            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;
            const scale = 100;

            for (let i = 0; i < geometry.indices.length; i += 3) {
                const i0 = geometry.indices[i];
                const i1 = geometry.indices[i + 1];
                const i2 = geometry.indices[i + 2];

                if (i0 >= geometry.vertices.length || i1 >= geometry.vertices.length || i2 >= geometry.vertices.length) {
                    continue;
                }

                const v0 = geometry.vertices[i0];
                const v1 = geometry.vertices[i1];
                const v2 = geometry.vertices[i2];

                const points = [
                    [centerX + v0[0] * scale, centerY - v0[1] * scale],
                    [centerX + v1[0] * scale, centerY - v1[1] * scale],
                    [centerX + v2[0] * scale, centerY - v2[1] * scale]
                ];

                const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                polygon.setAttribute('points', points.map(p => p.join(',')).join(' '));
                polygon.setAttribute('fill', color);
                polygon.setAttribute('stroke', color);
                polygon.setAttribute('stroke-width', '1');
                polygon.setAttribute('opacity', mesh.material?.opacity || 1.0);

                group.appendChild(polygon);
            }
        }

        renderScene();
    </script>
</body>
</html>''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))

    def _generate_webgl_html(self, scene, camera):
        scene_data = self._serialize_scene(scene, camera)

        template = Template('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenReactive WebGL Scene</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a1a;
        }
        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
        }
    </style>
</head>
<body>
    <canvas id="webgl-canvas"></canvas>

    <script>
        const sceneData = {{ scene_json }};
        const canvas = document.getElementById('webgl-canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

        if (!gl) {
            alert('WebGL not supported');
            throw new Error('WebGL not supported');
        }

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        gl.viewport(0, 0, canvas.width, canvas.height);

        const vertexShaderSource = `
            attribute vec3 aPosition;
            attribute vec3 aNormal;
            uniform mat4 uModelViewProjection;
            varying vec3 vNormal;

            void main() {
                gl_Position = uModelViewProjection * vec4(aPosition, 1.0);
                vNormal = aNormal;
            }
        `;

        const fragmentShaderSource = `
            precision mediump float;
            varying vec3 vNormal;
            uniform vec3 uColor;

            void main() {
                vec3 light = normalize(vec3(0.5, 1.0, 0.5));
                float diffuse = max(dot(normalize(vNormal), light), 0.2);
                gl_FragColor = vec4(uColor * diffuse, 1.0);
            }
        `;

        function createShader(gl, type, source) {
            const shader = gl.createShader(type);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);

            if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
                console.error('Shader compilation error:', gl.getShaderInfoLog(shader));
                gl.deleteShader(shader);
                return null;
            }

            return shader;
        }

        const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
        const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

        const program = gl.createProgram();
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);

        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            console.error('Program linking error:', gl.getProgramInfoLog(program));
        }

        gl.useProgram(program);

        const aPosition = gl.getAttribLocation(program, 'aPosition');
        const aNormal = gl.getAttribLocation(program, 'aNormal');
        const uModelViewProjection = gl.getUniformLocation(program, 'uModelViewProjection');
        const uColor = gl.getUniformLocation(program, 'uColor');

        gl.enable(gl.DEPTH_TEST);
        gl.clearColor(0.1, 0.1, 0.1, 1.0);

        function render() {
            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

            const mvp = new Float32Array(16);
            for (let i = 0; i < 16; i++) {
                mvp[i] = i % 5 === 0 ? 1 : 0;
            }

            gl.uniformMatrix4fv(uModelViewProjection, false, mvp);
            gl.uniform3f(uColor, 0.8, 0.4, 0.2);

            requestAnimationFrame(render);
        }

        render();

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            gl.viewport(0, 0, canvas.width, canvas.height);
        });
    </script>
</body>
</html>''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))
