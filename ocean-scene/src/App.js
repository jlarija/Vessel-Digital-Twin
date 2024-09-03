import './App.css';
import { Suspense, createContext } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sky } from '@react-three/drei';

import Ocean from './components/Ocean';
import Boat from './components/Boat';
import useStateSpace from './hooks/useStateSpace';
import Path from './components/Path';
import BoatKF from './components/BoatKF';
import PathKF from './components/PathKF';

export const Context = createContext()
export const StateContext = createContext()


function App() {

  const data = useStateSpace()

  return (
    <Context.Provider value={data}>
      <div id="canvas-container" style={{ width: "100vw", height: "100vh" }}>
        <Canvas camera={{ position: [0, 15, 50], fov: 55, near: 1, far: 20000 }}>
          <Suspense fallback={null}>
            <ambientLight intensity={0.1} />
            <directionalLight color="red" position={[0, 0, 5]} />
            <OrbitControls makeDefault minDistance={1} maxDistance={500} />
            <Sky />
            <Path />
            <PathKF />
            <Ocean />
            <Boat />
            <BoatKF />
          </Suspense>
        </Canvas>
      </div>
    </Context.Provider>
  );
}

export default App;
