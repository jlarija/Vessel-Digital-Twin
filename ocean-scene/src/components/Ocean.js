import * as THREE from 'three';
import { useRef, useMemo } from 'react';
import { extend, useThree, useLoader, useFrame } from '@react-three/fiber';

import { Water } from 'three-stdlib';
extend({ Water });

function Ocean() {
    const ref = useRef();
    const gl = useThree((state) => state.gl);
    const waterNormals = useLoader(THREE.TextureLoader, '/waternormals.png');
    waterNormals.wrapS = waterNormals.wrapT = THREE.RepeatWrapping;
    const geom = useMemo(() => new THREE.PlaneGeometry(10000, 10000), []);
    const config = useMemo(
        () => ({
            textureWidth: 512,
            textureHeight: 512,
            waterNormals,
            sunDirection: new THREE.Vector3(),
            sunColor: 0xffffff,
            waterColor: 0x001e0f,
            distortionScale: 3.7,
            fog: false,
            format: gl.encoding
        }),
        [gl.encoding, waterNormals]
    );
    useFrame((state, delta) => { ref.current.material.uniforms.time.value += delta * 0.2; });
    return <water ref={ref} args={[geom, config]} rotation-x={-Math.PI / 2} />;
}

export default Ocean;