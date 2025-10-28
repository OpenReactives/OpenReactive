import json
from jinja2 import Template


class JavaScriptExporter:
    def __init__(self):
        self.use_three_js = False
        self.use_babylon_js = False
        self.standalone = True
        self.minify = False

    def export_scene(self, scene, camera=None, output_path=None):
        scene_data = self._serialize_scene(scene, camera)

        if self.use_three_js:
            code = self._generate_threejs_code(scene_data)
        elif self.use_babylon_js:
            code = self._generate_babylonjs_code(scene_data)
        else:
            code = self._generate_standalone_code(scene_data)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(code)

        return code

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
            data["geometry"] = self._serialize_geometry(obj.geometry)

        if hasattr(obj, 'material') and obj.material:
            data["material"] = self._serialize_material(obj.material)

        if hasattr(obj, 'fov'):
            data["fov"] = obj.fov
            data["aspect"] = obj.aspect
            data["near"] = obj.near
            data["far"] = obj.far

        if hasattr(obj, 'color'):
            data["color"] = obj.color.to_array()

        if hasattr(obj, 'intensity'):
            data["intensity"] = obj.intensity

        for child in obj.children:
            data["children"].append(self._serialize_object(child))

        return data

    def _serialize_geometry(self, geometry):
        return {
            "id": geometry.id,
            "vertices": geometry.vertices,
            "normals": geometry.normals,
            "uvs": geometry.uvs,
            "indices": geometry.indices.tolist() if hasattr(geometry.indices, 'tolist') else geometry.indices
        }

    def _serialize_material(self, material):
        data = material.to_dict()
        return data

    def _generate_standalone_code(self, scene_data):
        template = Template('''
// OpenReactive Standalone Scene Export
const sceneData = {{ scene_json }};

class Vector3 {
    constructor(x = 0, y = 0, z = 0) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

class Object3D {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.type = data.type;
        this.position = new Vector3(...data.position);
        this.rotation = data.rotation;
        this.scale = new Vector3(...data.scale);
        this.visible = data.visible;
        this.children = data.children.map(child => new Object3D(child));

        if (data.geometry) {
            this.geometry = data.geometry;
        }

        if (data.material) {
            this.material = data.material;
        }
    }

    traverse(callback) {
        callback(this);
        this.children.forEach(child => child.traverse(callback));
    }
}

class Scene {
    constructor(data) {
        this.root = new Object3D(data.scene);
        this.camera = data.camera ? new Object3D(data.camera) : null;
    }

    render() {
        console.log("Rendering scene:", this.root.name);
        this.root.traverse(obj => {
            console.log(`  - ${obj.type}: ${obj.name}`);
        });
    }
}

const scene = new Scene(sceneData);
scene.render();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Scene, Object3D, Vector3, sceneData };
}
''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))

    def _generate_threejs_code(self, scene_data):
        template = Template('''
// OpenReactive Three.js Scene Export
import * as THREE from 'three';

const sceneData = {{ scene_json }};

function createScene(data) {
    const scene = new THREE.Scene();
    const camera = createCamera(data.camera);

    createObject(data.scene, scene);

    return { scene, camera };
}

function createCamera(data) {
    if (!data) {
        return new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    }

    const camera = new THREE.PerspectiveCamera(
        data.fov || 60,
        data.aspect || 1,
        data.near || 0.1,
        data.far || 1000
    );

    camera.position.set(...data.position);
    return camera;
}

function createObject(data, parent) {
    let object;

    if (data.type === 'Mesh' && data.geometry && data.material) {
        const geometry = createGeometry(data.geometry);
        const material = createMaterial(data.material);
        object = new THREE.Mesh(geometry, material);
    } else {
        object = new THREE.Object3D();
    }

    object.name = data.name;
    object.position.set(...data.position);
    object.quaternion.set(...data.rotation);
    object.scale.set(...data.scale);
    object.visible = data.visible;

    parent.add(object);

    if (data.children) {
        data.children.forEach(child => createObject(child, object));
    }

    return object;
}

function createGeometry(data) {
    const geometry = new THREE.BufferGeometry();

    const vertices = new Float32Array(data.vertices.flat());
    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

    if (data.normals && data.normals.length > 0) {
        const normals = new Float32Array(data.normals.flat());
        geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
    }

    if (data.uvs && data.uvs.length > 0) {
        const uvs = new Float32Array(data.uvs.flat());
        geometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
    }

    if (data.indices && data.indices.length > 0) {
        geometry.setIndex(data.indices);
    }

    return geometry;
}

function createMaterial(data) {
    const params = {
        color: data.color ? new THREE.Color(...data.color) : 0xffffff,
        transparent: data.transparent || false,
        opacity: data.opacity || 1,
        wireframe: data.wireframe || false
    };

    if (data.type === 'StandardMaterial') {
        params.metalness = data.metalness || 0;
        params.roughness = data.roughness || 1;
        return new THREE.MeshStandardMaterial(params);
    }

    return new THREE.MeshBasicMaterial(params);
}

const { scene, camera } = createScene(sceneData);

export { scene, camera, createScene };
''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))

    def _generate_babylonjs_code(self, scene_data):
        template = Template('''
// OpenReactive Babylon.js Scene Export
const sceneData = {{ scene_json }};

function createScene(engine, canvas) {
    const scene = new BABYLON.Scene(engine);
    const camera = createCamera(sceneData.camera, scene, canvas);

    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
    light.intensity = 0.7;

    createObject(sceneData.scene, scene, null);

    return { scene, camera };
}

function createCamera(data, scene, canvas) {
    let camera;

    if (data && data.type === 'PerspectiveCamera') {
        camera = new BABYLON.ArcRotateCamera(
            "camera",
            -Math.PI / 2,
            Math.PI / 2.5,
            5,
            new BABYLON.Vector3(...data.position),
            scene
        );
    } else {
        camera = new BABYLON.ArcRotateCamera(
            "camera",
            -Math.PI / 2,
            Math.PI / 2.5,
            5,
            BABYLON.Vector3.Zero(),
            scene
        );
    }

    camera.attachControl(canvas, true);
    return camera;
}

function createObject(data, scene, parent) {
    if (data.type === 'Mesh' && data.geometry && data.material) {
        const mesh = createMesh(data, scene);
        if (parent) {
            mesh.parent = parent;
        }

        if (data.children) {
            data.children.forEach(child => createObject(child, scene, mesh));
        }

        return mesh;
    }

    const object = new BABYLON.TransformNode(data.name, scene);
    object.position = new BABYLON.Vector3(...data.position);
    object.scaling = new BABYLON.Vector3(...data.scale);

    if (parent) {
        object.parent = parent;
    }

    if (data.children) {
        data.children.forEach(child => createObject(child, scene, object));
    }

    return object;
}

function createMesh(data, scene) {
    const geometry = data.geometry;
    const customMesh = new BABYLON.Mesh(data.name, scene);

    const positions = geometry.vertices.flat();
    const indices = geometry.indices;
    const normals = geometry.normals ? geometry.normals.flat() : [];

    const vertexData = new BABYLON.VertexData();
    vertexData.positions = positions;
    vertexData.indices = indices;
    if (normals.length > 0) {
        vertexData.normals = normals;
    }

    vertexData.applyToMesh(customMesh);

    const material = new BABYLON.StandardMaterial(data.material.name, scene);
    if (data.material.color) {
        material.diffuseColor = new BABYLON.Color3(...data.material.color);
    }
    material.alpha = data.material.opacity || 1;

    customMesh.material = material;
    customMesh.position = new BABYLON.Vector3(...data.position);
    customMesh.scaling = new BABYLON.Vector3(...data.scale);

    return customMesh;
}

export { createScene };
''')

        return template.render(scene_json=json.dumps(scene_data, indent=2))
