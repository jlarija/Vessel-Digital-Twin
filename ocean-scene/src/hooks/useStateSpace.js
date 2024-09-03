import { useState, useEffect } from "react";
import axios from "axios";

const useStateSpace = () => {

    const [data, setData] = useState({})

    const myReallyBadHardCodedAPIPath = "http://localhost:4999";

    useEffect(() => {
        if (!Object.keys(data).length){
            axios.get(`${myReallyBadHardCodedAPIPath}/sim`).then(
                function (result) {
                    setData(result.data);
                }
            );
        }
    });

    return data
}

export default useStateSpace