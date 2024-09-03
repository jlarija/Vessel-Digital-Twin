# ntnu-digitial-twin

Steps: 
1. Install requirements
2. Build npm in ocean-scene
3. Run flask app: flask --app .\app.py run

This project shows the movement of a vessel in the ocean. The algorithm is based on an adaptive extended Kalman filter (AEKF), which is based on the following paper: "Model-Based Fault Diagnosis Algorithms for Robotic Systems" by AGUS HASAN HENRIK MARYAMSADAT TAHAVORI SKOV MIDTIBY .

In this implementation we used React and Flask for the web based demonstration, and python for the back-end coding of the trajectory and implementation of the algorithm. 

A snapshot of the web based visualization is included below:
![image](https://github.com/user-attachments/assets/4b0b3a46-d6b1-40db-8579-abadfb8d7d8a)
