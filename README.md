# Vessel Movement Simulation in the Ocean

This project simulates the movement of a vessel in the ocean using an Adaptive Extended Kalman Filter (AEKF). The web-based demonstration is built with React for the frontend, Flask for the backend, and Python for the core algorithm and trajectory calculations.

## Overview

This simulation models how a vessel navigates through the ocean, leveraging the Adaptive Extended Kalman Filter (AEKF) for precise tracking and prediction. The AEKF is an enhancement of the Extended Kalman Filter (EKF), designed to handle the non-linear dynamics of the vessel. It adapts to changes in the system's behavior in real-time, improving accuracy in uncertain conditions.

The algorithm implementation is based on the research paper **"Model-Based Fault Diagnosis Algorithms for Robotic Systems"** by Agus Hasan, Henrik Skov Midtiby, and Maryamsadat Tahavori. The paper discusses fault diagnosis in robotic systems, where the AEKF helps in maintaining accurate state estimation even when the system encounters unexpected changes.

## Project Structure

- **Frontend (React):**  
  The user interface is built with React, providing an interactive platform to visualize the vessel's movement. You can explore different simulation scenarios and see the effects in real-time.

- **Backend (Flask & Python):**  
  Flask serves as the API layer, connecting the frontend with the backend. The Python backend is responsible for the heavy lifting—implementing the AEKF and computing the vessel's trajectory.

A snapshot of the implemented web visualization is provided below:
![image](https://github.com/user-attachments/assets/4b0b3a46-d6b1-40db-8579-abadfb8d7d8a)


To run the project, build the frontend with npm and then start the flask server with flask --app .\app.py run (cd turning_vessel_model).
