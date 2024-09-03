function CustomMesh() {
    return (
        <mesh position={[-3, 2, -1]}>
            <sphereGeometry args={[1, 62, 16]} />
            <meshNormalMaterial />
        </mesh>
    );
}

export default CustomMesh;