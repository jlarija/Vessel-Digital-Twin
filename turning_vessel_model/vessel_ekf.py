'''NOT WORKING'''


import numpy as np
import sympy as sp

class Vessel:

    m11, m22, m23, m32, m33  = 25.8, 33.8, 6.2, 6.2, 2.76
    Xu, Xuu, Yv, Yvv, Yr, Nv, Nr, Nrr = -12, -2.1,-17, -4.5, -0.2, -0.5, -0.5,-0.1
    A = sp.eye(6)
    Btau = sp.Matrix([[1,0],[0,0],[0,1]])
    M = sp.Matrix([[m11, 0, 0],[0, m22, m23],[0, m32, m33]])
    M_inv = M.inv() # inverse of M
    B1 = sp.zeros(3,2)
    B2 = M_inv * Btau
    B = sp.Matrix(np.concatenate((B1,B2)))

    # new values from new paper 
    Qf = 0
    Cobs = 0 # this is the observation matrix, not the same C as below to calculate F
    Rf = 0
    llambda = 0 # forgetting factor 

    def __init__(self):
        self._x = sp.Matrix([[0], [0], [0], [0], [0], [0]]) # x,y,psi,u,v,r
        self.u = sp.Matrix([[1],[-1]], dtype=float) # input
        self.x_, self.y, self.psi, self.u, self.v, self.r = sp.symbols('x y psi u v r', real = True)
        self.x_jac = sp.Matrix([self.x_,self.y,self.psi,self.u,self.v,self.r])
        self._Pplus = 0
        self.Upsilon = 0
        self.Sk = 0
        self.thetak = 0

    def phi(self):
        return -self.B * sp.diag(*self.u) 
        
    def D(self):
        return sp.Matrix([[self.Xu+self.Xuu*self.u, 0, 0], 
            [0, self.Yv+self.Yvv*self.v, self.Yr],
            [0, self.Nv, self.Nr+self.Nrr*-self.r]])

    def C(self):
        c13 = -self.m22* self.v - ((self.m23+self.m32)/2) * self.r
        c23 = self.m11*self.u
        return sp.Matrix([[0,0,c13],
            [0,0, c23],
            [-c13,-c23,0]])

    def R(self):
        return sp.Matrix([[sp.cos((self.psi)), -sp.sin((self.psi)), 0],
                    [sp.sin((self.psi)), sp.cos((self.psi)), 0],
                    [0,0,1]])

    def F(self):
        eta = sp.Matrix([[self.u], 
                [self.v], 
                [self.r]])
        F1 = self.R() * eta
        F2 = -self.M_inv * ((self.C() - self.D()) * self.eta)
        sp.Matrix(np.concatenate((F1,F2)))
        return 
    
    def Fk(self):
        dfdx = self.F().jacobian(self.x_jac)
        return self.A + dfdx
    
    def Pminus(self):
        return self.Fk * self._Pplus * self.Fk + self.Qf # pplus has to be updated every iteration
    
    def Sigma(self):
        return self.Cobsv * self.Pminus * self.Cobsv.T + self.Rf
    
    def K(self):
        self.UpdatePplus((sp.eye(0) - self.K*self.Cobs)*self._Pplus) #update pplus
        return self.Pminus * self.Cobs.T*self.Sigma
        # recursive method to get kalman gain

    def Upsilon(self):
        return (sp.eye(0) - self.K * self.Cobs) * self.Fk*self.Upsilon + (sp.eye(0) - self.K * self.Cobs) * self.phi
    
    def Omega(self):
        return self.Cobs * self.Fk * self.Upsilon + self.Cobs * self.phi
    
    def Lambda(self):
        return (self.llambda * self.Sigma + self.Omega*self.Sk*self.Omega.T).inv()
    
    def theta(self):
        Tau = self.Sk * self.Omega.T * self.Lambda
        y_tilde = self.yk - self.Cobs * self.x_jac
        return self.thetak + Tau*y_tilde
    
    def Update(self, x):
        self._x = x

    def UpdatePplus(self, Pplus):
        self._Pplus = Pplus
    
    def UpdateUpsilon(self,Upsilon):
        return

    @property
    def x(self):
        return self._x
    
    @property
    def Pplus(self):
        return self.Pplus
    
