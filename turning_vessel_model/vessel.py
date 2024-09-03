import numpy as np
from numpy.linalg import inv
import random
random.seed(10)
class Vessel:

    m11, m22, m23, m32, m33  = 25.8, 33.8, 6.2, 6.2, 2.76
    Xu, Xuu, Yv, Yvv, Yr, Nv, Nr, Nrr = -12, -2.1,-17, -4.5, -0.2, -0.5, -0.5,-0.1
    A = np.eye(6)
    Btau = np.array([[1,0],[0,0],[0,1]])
    M = np.array([[m11, 0, 0],[0, m22, m23],[0, m32, m33]])
    M_inv = inv(M) # inverse of M 
    B1 = np.zeros((3,2))
    B2 = M_inv @ Btau
    B = np.array(np.concatenate((B1,B2)))

    def __init__(self, u_input):
        self._x = np.zeros(6)
        self.x, self.y, self.psi, self.u, self.v, self.r = self._x[0],self._x[1],self._x[2],self._x[3],self._x[4],self._x[5]
        self.u_input = u_input # input
           
    def D(self, xi):
        return -np.array([[self.Xu+self.Xuu*np.abs(float(xi[3])), 0, 0], 
            [0, self.Yv+self.Yvv*np.abs(float(xi[4])), self.Yr],
            [0, self.Nv, self.Nr+self.Nrr*np.abs(float(xi[5]))]])
        # return -np.array([[self.Xu+self.Xuu*np.abs(float(self._x[3])), 0, 0], 
        #     [0, self.Yv+self.Yvv*np.abs(float(self._x[4])), self.Yr],
        #     [0, self.Nv, self.Nr+self.Nrr*np.abs(float(self._x[5]))]])


    def C(self):
        c13 = -self.m22* self._x[4] - ((self.m23+self.m32)/2) * self._x[5]
        c23 = self.m11*self._x[3]
        return np.array([[0,0,float(c13)],
            [0,0, float(c23)],
            [-float(c13),-float(c23),0]],  dtype=float)

    def R(self):
        return np.array([
            [np.cos(float(self._x[2])), -np.sin(float(self._x[2])), 0],
            [np.sin(float(self._x[2])), np.cos(float(self._x[2])), 0],
            [0,0,1]],  dtype=float)

    def F(self, xi):
        v = np.array([float(self._x[3]), float(self._x[4]), float(self._x[5])],  dtype=float)
        F1 = self.R().dot(v)
        F2 = -self.M_inv.dot((self.C() + self.D(xi)).dot(v))
        return np.concatenate((F1,F2))
       
    def phi(self):
        return -self.B @ np.diag(self.u_input.T) 
    
    def Fk(self, dt):
        dfdx_num = np.array([
            [0, 0, -self.u*np.sin(self.psi) - self.v*np.cos(self.psi), np.cos(self.psi), -np.sin(self.psi), 0], 
            [0, 0, self.u*np.cos(self.psi) - self.v*np.sin(self.psi), np.sin(self.psi), np.cos(self.psi), 0], 
            [0, 0, 0, 0, 0, 1], 
            [0, 0, 0, -0.162790697674419*self.u - 0.465116279069767, 1.31007751937984*self.r, 0.48062015503876*self.r + 1.31007751937984*self.v], 
            [0, 0, 0, -0.597432905484248*self.r + 0.904317386231039*self.v, 0.904317386231039*self.u - 0.452887981330222*self.v - 0.798935239206535, 0.022607934655776*self.r - 0.597432905484248*self.u + 0.0464556592765461], 
            [0, 0, 0, -0.904317386231039*self.r - 4.92998833138856*self.v, -4.92998833138856*self.u + 1.01735705950992*self.v + 1.61355017502917, -0.123249708284714*self.r - 0.904317386231039*self.u - 0.285516336056009]])
        
        return self.A + dt*dfdx_num

    def ytilde(self, y): 
        return y - (self.Cobvs @ self._x)

    def Update(self, x):
        self._x = x
        self.x, self.y, self.psi, self.u, self.v, self.r = self._x[0],self._x[1], self._x[2], self._x[3], self._x[4], self._x[5]

    def updateInput(self, u):
        self.u_input = u

    @property
    def X(self):
        return self._x
    
