import { useContext, useRef } from "react";
import { Context } from "../App";

import * as THREE from 'three';

function PathKF() {
    const data = useContext(Context)
    const group = useRef();
    const points = []
    if (Object.keys(data).length) {
        Object.keys(data).forEach((key, index) => points.push( new THREE.Vector3(data[key]['y'] * 200, 30, data[key]['x'] * 200)))
    }

    const lineGeometry = new THREE.BufferGeometry().setFromPoints(points)

    return (
        <>
            <group ref={group}>
                <line geometry={lineGeometry}> 
                    <lineBasicMaterial attach="material" color={'#ffffff'} linewidth={10} linecap={'round'} linejoin={'round'} />
                </line>
            </group>
        </>
    )
}

export default PathKF