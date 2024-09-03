import React, { useContext, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { useGLTF } from "@react-three/drei";
import { Context } from "../App";
import { StateContext } from "../App";
import { Material } from "three";


export default function BoatKF(props) {
    const [frame, setFrame] = useState(0);
    const group = useRef();
    const tick = useRef(0);
    const tock = useRef(0);
    const { nodes, materials } = useGLTF("/origami_boat.glb");

    const data = useContext(Context)
    const stateData = useContext(StateContext)

    useFrame((state, delta) => {
        tick.current += delta
        if (tick.current - tock.current > 0.01) {
            if (Object.keys(data).length && frame < Object.keys(data).length) {
                group.current.position.z = data[frame]['x'] * 200;
                group.current.position.x = data[frame]['y'] * 200;
                group.current.position.y = 30;
                group.current.rotation.y = data[frame]['psi'];
                setFrame(frame+1)
            }
            tock.current = tick.current
        }

        console.log(stateData)

        if(frame >= Object.keys(data).length) {
            setFrame(0)
        }
    });

    return (
        <group ref={group} {...props} dispose={null} scale={0.4}>
            <mesh
                castShadow
                receiveShadow
                geometry={nodes.Plane015_Ships_0.geometry}
                scale={0.5}
            />
        </group>
    );
}

useGLTF.preload("/origami_boat.glb");


// import React, { useRef } from "react";
// import { useGLTF } from "@react-three/drei";

// export default function Model(props) {
//     const { nodes, materials } = useGLTF("/origami_boat.glb");
//     return (
//         <group {...props} dispose={null}>
//             <group rotation={[-Math.PI / 2, 0, 0]} scale={0}>
//                 <group rotation={[Math.PI / 2, 0, 0]}>
//                     <mesh
//                         castShadow
//                         receiveShadow
//                         geometry={nodes.Plane015_Ships_0.geometry}
//                         material={materials.Ships}
//                     />
//                 </group>
//             </group>
//         </group>
//     );
// }

// useGLTF.preload("/origami_boat.glb");