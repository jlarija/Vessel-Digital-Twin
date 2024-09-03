import numpy as np
from numpy.linalg import inv

# time horizon
tf = 20
dt = 0.01
t = np.arange(dt, tf + dt, dt)

# system description
A = np.eye(6)
B_t = np.array([[1, 0], [0, 0], [0, 1]])
M = np.array([[25.8, 0, 0], [0, 33.8, 6.2], [0, 6.2, 2.76]])
B = dt * np.concatenate(([np.zeros((3, 2)), np.linalg.inv(M) @ B_t]))
C = np.eye(6)

# noise
QF = 0.01 * np.eye(6)
RF = 0.04 * np.eye(6)

# Initialization
x = np.array([0, 0, 0, 0, 0, 0])
xbar = np.array([0, 0, 0, 0, 0, 0])
xhat = np.array([0, 0, 0, 0, 0, 0])
theta = np.array([0, 0])
thetabar = np.array([0, 0])
thetahat = np.array([0, 0])
temp = np.zeros(6)
Pplus = np.eye(6)

# Parameter
m22 = 5
m23 = 1.2
m32 = 1.2
m11 = 3
Xu = -1
Xuu = -2
Yv = -1
Yvv = -1
Yr = -0.2
Nv = -0.5
Nr = -0.5
Nrr = -0.1

u = np.array([2, 0.1])
at = 0
Psi = -B @ np.diag(u)
S = 0.1*np.eye(2)
UpsilonPlus = np.zeros_like(B)
lambda_val = 0.995
a = 0.999

# For plotting
uArray = []
xArray = []
xhatArray = []
thetaArray = []
thetahatArray = []

def R(xi):
    return np.array([[np.cos(float(xi[2])), -np.sin(float(xi[2])), 0],
                [np.sin(float(xi[2])), np.cos(float(xi[2])), 0],
                [0,0,1]],  dtype=float)

def F(xi, Cv, Dv):
    v = np.array([float(xi[3]), 
                float(xi[4]), 
                float(xi[5])],  dtype=float)
    F1 =  R(xi).dot(v)
    F2 = -inv(M).dot((Cv + Dv).dot(v))
    return np.concatenate((F1,F2))

# Simulation
for i in range(int(tf / dt)):
    Psi = -B @ np.diag(u)

    if(i == 100):
        u = np.array([1, 0.1], dtype=float)
    if(i == 600):
        theta = np.array([0.001,0.12])
    if(i == 1000):
        u = np.array([1, 0.15], dtype=float)
    if(i == 2000):
        theta = np.array([0,0.025])
    if(i == 2500):
        u = np.array([1, 0.2], dtype=float)
    if(i == 3000):
        u = np.array([1, 0.001], dtype=float)

    if(i == 3200):
        u = np.array([1, -0.05], dtype=float)
    if(i == 3600):
        theta = np.array([0.005,0.075])
    if(i == 3800):
        u = np.array([1, -0.005], dtype=float)
    if(i == 4000):
        u = np.array([1, -0.2], dtype=float)
        theta = np.array([0,0])

    # if i > 500:
    #     u = np.array([4, 0.2])

    # if i > 1000:
    #     theta = np.array([0, 0.25])

    # if i > 1200:
    #     u = np.array([1, -0.1])

    # if i > 1500:
    #     theta = np.array([0, 0.141])

    uArray.append(u)
    xArray.append(x)
    xhatArray.append(xhat)
    thetaArray.append(theta)
    thetahatArray.append(thetahat)

    c13 = -m22 * x[4] - ((m23 + m32) / 2) * x[5]
    c23 = m11 * x[3]
    Cv = np.array([[0, 0, c13], [0, 0, c23], [-c13, -c23, 0]])
    Dv = -np.array([[Xu + Xuu * abs(x[3]), 0, 0], [0, Yv + Yvv * abs(x[4]), Yr], [0, Nv, Nr + Nrr * abs(x[5])]])

    x = A @ x + dt*F(x, Cv, Dv) + dt*B @ u + Psi @ theta + QF @ np.random.randn(6)
    y = C @ x + RF @ np.random.randn(6)

    # Adaptive Extended Kalman filter
    FX = A + dt * np.array([
            [0, 0, -x[3]*np.sin(x[2]) - x[4]*np.cos(x[2]), np.cos(x[2]), -np.sin(x[2]), 0], 
            [0, 0, x[3]*np.cos(x[2]) - x[4]*np.sin(x[2]), np.sin(x[2]), np.cos(x[2]), 0], 
            [0, 0, 0, 0, 0, 1], 
            [0, 0, 0, -0.162790697674419*x[3] - 0.465116279069767, 1.31007751937984*x[5], 0.48062015503876*x[5] + 1.31007751937984*x[4]], 
            [0, 0, 0, -0.597432905484248*x[5] + 0.904317386231039*x[4], 0.904317386231039*x[3] - 0.452887981330222*x[4] - 0.798935239206535, 0.022607934655776*x[5] - 0.597432905484248*x[3] + 0.0464556592765461], 
            [0, 0, 0, -0.904317386231039*x[5] - 4.92998833138856*x[4], -4.92998833138856*x[3] + 1.01735705950992*x[4] + 1.61355017502917, -0.123249708284714*x[5] - 0.904317386231039*x[3] - 0.285516336056009]])
    
    Pmin = FX @ Pplus @ FX.T + QF
    Sigma = C @ Pmin @ C.T + RF
    KF = Pmin @ C.T @ np.linalg.inv(Sigma)
    Pplus = (np.eye(np.linalg.matrix_rank(A)) - KF @ C) @ Pmin
    
    ytilde = y - C @ xhat
    a1 = a * QF
    a2 = (1 - a)
    a3 = ytilde @ ytilde.T
    QF = a * QF + (1 - a) * (KF * (ytilde @ ytilde.T) * KF.T)
    RF = a * RF + (1 - a) * (ytilde @ ytilde.T + C @ Pmin @ C.T)
    
    Upsilon = (np.eye(np.linalg.matrix_rank(A)) - KF @ C) @ FX @ UpsilonPlus + (np.eye(np.linalg.matrix_rank(A)) - KF @ C) @ Psi
    Omega = C @ FX @ UpsilonPlus + C @ Psi
    whatamI = Omega.T @ Omega
    Lambda = np.linalg.inv(lambda_val * Sigma + Omega @ S @ Omega.T)
    Gamma = S @ Omega.T @ Lambda
    S = (1 / lambda_val) * S - (1 / lambda_val) * S @ Omega.T @ Lambda @ Omega @ S
    UpsilonPlus = Upsilon
    
    thetahat = thetahat + Gamma @ (y - C @ xhat)
    xhat = (
        A @ xhat
        + dt * F(xhat, Cv, Dv)
        + B @ u + Psi @ thetahat + KF @ (y - C @ xhat) + Upsilon @ Gamma @ (y - C @ xhat)
    )

import matplotlib.pyplot as plt

# Figure 1 - Subplot 1
xArray0 = np.array([i[0] for i in xArray])
xArray1 =  np.array([i[1] for i in xArray])
xArray3 =  np.array([i[3] for i in xArray])
xhatArray0 =  np.array([i[0] for i in xhatArray])
xhatArray1 =  np.array([i[1] for i in xhatArray])
xhatArray3 =  np.array([i[3] for i in xhatArray])
thetaArray0 =  np.array([i[0] for i in thetaArray])
thetaArray1 =  np.array([i[1] for i in thetaArray])
thetahatArray0 =  np.array([i[0] for i in thetaArray])
thetahatArray1 =  np.array([i[1] for i in thetaArray])
uArray0 = np.array([i[0] for i in uArray])
uArray1 = np.array([i[1] for i in uArray])

plt.figure(1)
plt.subplot(2, 2, 1)
plt.plot(xArray0, xArray1, 'k', linewidth=3)
# plt.hold(True)
plt.plot(xhatArray0, xhatArray1, 'r:', linewidth=3)
plt.grid(True, which='both')
plt.ylabel('y (m)', fontsize=36)
plt.xlabel('x (m)', fontsize=36)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(['true', 'estimated'], fontsize=18)

# Figure 1 - Subplot 2
plt.subplot(2, 2, 2)
plt.plot(t, xArray0 - xhatArray0, 'k', linewidth=3)
plt.grid(True, which='both')
plt.ylabel('error x', fontsize=36)
plt.xlabel('t (s)', fontsize=18)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.axvline(x=10, linestyle=':', color='b', linewidth=3)
plt.axvline(x=15, linestyle=':', color='b', linewidth=3)
plt.text(12, 1.5, 'fault', fontsize=18)

# Figure 1 - Subplot 3
plt.subplot(2, 2, 4)
plt.plot(t, xArray3 - xhatArray3, 'k', linewidth=3)
plt.grid(True, which='both')
plt.ylabel('error y', fontsize=36)
plt.xlabel('t (s)', fontsize=36)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.axvline(x=10, linestyle=':', color='b', linewidth=3)
plt.axvline(x=15, linestyle=':', color='b', linewidth=3)
plt.text(12, 1.5, 'fault', fontsize=18)

# Figure 2
plt.figure(2)
plt.plot(t, uArray0, ':b', linewidth=3)
# plt.hold(True)
plt.plot(t, uArray1, ':r', linewidth=3)
plt.grid(True, which='both')
plt.ylabel('u', fontsize=36)
plt.xlabel('t (s)', fontsize=36)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(['a', 'r'], fontsize=18)

# Figure 3 - Subplot 1
plt.figure(3)
plt.subplot(2, 1, 1)
plt.plot(t, thetaArray0, 'k', linewidth=3)
# plt.hold(True)
plt.plot(t, thetahatArray0, 'r:', linewidth=3)
plt.ylabel('θ₁', fontsize=18)
plt.xlabel('t (s)', fontsize=18)
plt.grid(True, which='both')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim([-0.05, 0.35])

# Figure 3 - Subplot 2
plt.subplot(2, 1, 2)
plt.plot(t, thetaArray1, 'k', linewidth=3)
# plt.hold(True)
plt.plot(t, thetahatArray1, 'r:', linewidth=3)
plt.legend(['true θ', 'estimated θ'], fontsize=18)
plt.ylabel('θ₂', fontsize=18)
plt.xlabel('t (s)', fontsize=18)
plt.grid(True, which='both')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim([-0.05, 0.3])

# Show all the plots
plt.show()