import numpy as np
from matplotlib import pyplot as plt

# DATA
m11 = 25.8
m22 = 33.8
m23 = 6.2
m32 = 6.2
m33 = 2.76
Xu = -12
Xuu = -2.1
Yv = -17
Yvv = -4.5
Yr = -0.2
Nv = -0.5
Nr = -0.5
Nrr = -0.1

# CONSTANT MATRICES
A = np.eye(6)

Btau = np.array([[1,0],
      [0,0],
      [0,1]])

M = np.array([[m11, 0, 0],
    [0, m22, m23],
    [0, m32, m33]])

M_inv = np.linalg.inv(M) # inverse of M
B1 = np.zeros((3,2))
B2 = M_inv.dot(Btau)
B = np.concatenate((B1,B2))

# FUNCTIONS FOR NON-CONSTANT MATRICES
def D(x):
    d = np.array([[Xu+Xuu*np.abs(float(x[3])), 0, 0], 
     [0, Yv+Yvv*np.abs(float(x[4])), Yr],
     [0, Nv, Nr+Nrr*np.abs(float(x[5]))]])
    return d

def C(x):
    c13 = -m22* x[4] - ((m23+m32)/2) * x[5]
    c23 = m11*x[3]
    c= np.array([[0,0,c13],
        [0,0, c23],
        [-c13,-c23,0]],  dtype=float)
    return c

def R(x):
    r = np.array([[np.cos(float(x[2])), -np.sin(float(x[2])), 0],
                [np.sin(float(x[2])), np.cos(float(x[2])), 0],
                [0,0,1]],  dtype=float)
    return r

def F(x):
    v = np.array([[float(x[3])], 
                 [float(x[4])], 
                 [float(x[5])]],  dtype=float)
    F1 = R(x).dot(v)
    F2 = -M_inv.dot((C(x) - D(x)).dot(v))
    f = np.concatenate((F1,F2))
    return f

# INITIALISE
x = np.array([[0], [0], [0], [0], [0], [0]]) # x,y,psi,u,v,r
dt = 0.1
Ttot = 20
u = np.array([[1],[-1]], dtype=float)

t = 0 #s