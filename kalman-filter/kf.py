import numpy as np

class KF:
    def __init__(self, initial_x, initial_v, variance):
        self.x = np.array([initial_x, initial_v])
        self.variance = variance

        self.P = np.eye(2)

    def predict(self, dt):
        F = np.array([[1,dt],[0,1]])
        Q = np.array([0.0001, dt]).reshape((2,1))

        self.x = F.dot(self.x)
        self.P = F.dot(self.P).dot(F.T) + Q.dot(Q.T) * self.variance

    def update(self, meas_value, meas_variance):
        Z = np.array([meas_value])
        R = np.array([meas_variance])
        C = np.array([1,0]).reshape(1,2)

        y = Z - C.dot(self.x)
        s = C.dot(self.P).dot(C.T) + R
        k = self.P.dot(C.T).dot(np.linalg.inv(s))

        self.x = self.x + k.dot(y)
        self.P = (np.eye(2) - k.dot(C)).dot(self.P)

    @property
    def cov(self):
        return self.P
    
    @property
    def mean(self):
        return self.x

    @property
    def pos(self):
        return self.x[0]
    
    @property
    def vel(self):
        return self.x[1]