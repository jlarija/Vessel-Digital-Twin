import matplotlib.pyplot as plt
import numpy as np

from kf import KF

plt.ion()
plt.figure()

kf = KF(0.0, 1.0, 0.1)

real_x = 0.0
meas_variance = 0.1 ** 2
real_v = 0.9

DT = 0.1
NUM_STEPS = 1000
MEAS_STEPS = 20

mus = []
covs = []

for step in range(NUM_STEPS):
    covs.append(kf.cov)
    mus.append(kf.mean)

    real_x = real_x+DT * real_v

    kf.predict(DT)
    if(step != 0 and step % MEAS_STEPS == 0):
        kf.update(real_x + np.random.randn() * np.sqrt(meas_variance), meas_variance)


plt.subplot(2,1,1)
plt.title('Position')
plt.plot([mu[0] for mu in mus], 'r')
plt.plot([mu[0] - 2*np.sqrt(covs[0,0]) for mu, covs in zip(mus, covs)], 'r--')
plt.plot([mu[0] + 2*np.sqrt(covs[0,0]) for mu, covs in zip(mus, covs)], 'r--')

plt.subplot(2,1,2)
plt.title('Velocity')
plt.plot([mu[1] for mu in mus], 'r')
plt.plot([mu[1] - 2*np.sqrt(covs[1,1]) for mu, covs in zip(mus, covs)], 'r--')
plt.plot([mu[1] + 2*np.sqrt(covs[1,1]) for mu, covs in zip(mus, covs)], 'r--')

plt.show()
# plt.ginput(1)