import { MeshStandardMaterial, Mesh, MathUtils } from 'three';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';
// import fontSource from ;
export default class Text {
	constructor(scene, text, fontPath, size, depth, color, name, position, cameraPosition)
	{
		this.scene = scene;
		this.text = text;
		this.fontPath = fontPath;
		this.size = size;
		this.depth = depth;
		this.color = color;
		this.name = name;
		this.position = position;
		this.cameraPosition = cameraPosition;
		this.bevelThickness = 1;
		this.bevelSize = 0.35;

		this.fontLoader = new FontLoader();
		this.fontLoader.load(fontPath, (font) => {
		this.textGeometry = new TextGeometry(this.text, {
				font: font,
				size: this.size,
				depth: this.depth,
				curveSegments: 12,
				bevelEnabled: true,
				bevelThickness: this.bevelThickness,
				bevelSize: this.bevelSize,
				color: this.color,
				// curveSegments: 4,
			});

			this.textMaterial = new MeshStandardMaterial({
				color: this.color,
				roughness: 0.4,
				metalness: 0.3,
				emissive: this.color,
				emissiveIntensity: 0.4,
			});

			this.textMesh = new Mesh(this.textGeometry, this.textMaterial);

			this.textMesh.lookAt(this.cameraPosition);
			this.textMesh.name = this.name;
			this.textMesh.position.set(this.position.x - 15, this.position.y + 35, this.position.z  + 10);
			this.textMesh.visible = false;
			this.scene.add(this.textMesh);
			this.textMesh.castShadow = true;
			this.textMesh.receiveShadow = true;
		});
	}
	show()
	{
		if (this.textMesh)
			this.textMesh.visible = true;
	}

	hide()
	{
		if (this.textMesh)
			this.textMesh.visible = false;
	}
	
	rotate(x, y, z)
	{
		if (this.textMesh) {
			this.textMesh.rotation.set(
				MathUtils.degToRad(x),
				MathUtils.degToRad(y),
				MathUtils.degToRad(z)
			);
		} else {
			console.warn('textMesh is not yet created.');
		}
	}
}
