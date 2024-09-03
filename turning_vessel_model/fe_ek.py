'''In this code, we have 6 states, 2 inputs, and 6 outputs. The outputs were chosen in accordance with the paper 
'Flatness-based MPC for underactuated surface vessels in confined areas' as y = [x,y,psi]'''

from vessel import Vessel
from matplotlib import pyplot as plt
import numpy as np
from numpy.linalg import inv
from numpy.random import randn

def predict(t_tot, ti, dt, u_input):

    timestamp = []
    x_state = []
    x_hat = []
    theta_array = []
    theta_hat = []

    vs = Vessel(u_input)
    vs_exact = Vessel(u_input)
    # Sk = 0.1*np.eye(2) # depends on number of inputs (inputsxinputs)
    Sk = 0.1*np.eye(2)
    Pplus = np.eye(6) # covariance matrix, states x states 
    Upsilon = np.zeros((6,2)) # 6 rows and 2 columns, states x inputs
    theta = np.array([0,0]) # fault in any of the control inputs so same shape as inputs
    thetahat = np.array([0,0])
    llambda = 0.995
    Cobvs = np.eye(6)
    Qf = 0.01*np.eye(6) # shape proportional to number of states
    Rf =  0.04*np.eye(6) # shape proportional to number of outputs
    a = 0.999 # random factor that they do not explain

    i = 0

    while ti < t_tot:

        phi = vs.phi()

        if(i == 100):
            u_input = np.array([u_input[0], min(u_input[1] + 0.01, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 600):
            theta = np.array([0.001,0.12])
        if(i == 1000):
            u_input = np.array([u_input[0], min(u_input[1] + 0.1, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 2000):
            theta = np.array([0,0.025])
        if(i == 2500):
            u_input = np.array([u_input[0], min(u_input[1] - 0.2, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 3000):
            u_input = np.array([u_input[0], min(u_input[1] - 0.05, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 3200):
            u_input = np.array([2.0, min(u_input[1] - 0.25, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 3600):
            theta = np.array([0.005, 0.075])
        if(i == 3800):
            u_input = np.array([-1.0, min(u_input[1] - 0.4, 0.2)], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
        if(i == 4000):
            u_input = np.array([1, -0.02], dtype=float)
            vs_exact.updateInput(u_input)
            vs.updateInput(u_input)
            theta = np.array([0,0])

        vs_exact.Update(vs_exact.A @ vs_exact.X + dt*vs_exact.F(vs_exact.X) + dt*vs_exact.B @ vs_exact.u_input + vs_exact.phi() @ theta) # calcualtes x

        y = Cobvs.dot(vs_exact.X)

        Fk = vs.Fk(dt)

        Pminus = Fk @ Pplus @ Fk.T + Qf
        Sigma = Cobvs @ Pminus @ Cobvs.T + Rf
        K = Pminus @ Cobvs.T @ inv(Sigma)
        Pplus = (np.eye(6) - (K @ Cobvs)) @ Pminus

        ytilde =  y - (Cobvs @ vs.X)

        Qf = a * Qf + (1 - a) * (K * (ytilde @ ytilde.T) * K.T)

        Rf = a*Rf + (1-a) * (ytilde @ ytilde.T + Cobvs @ Pminus @ Cobvs.T)

        # Compute fault estimation gains
        Upsilon =  (np.eye(6) - K @ Cobvs) @ Fk @ Upsilon + (np.eye(6) - K @ Cobvs) @ phi
        Omega = Cobvs @ Fk @ Upsilon + Cobvs @ phi

        Lambda = inv(llambda * Sigma + Omega.dot(Sk).dot(Omega.T))

        Tau = Sk @ Omega.T @ Lambda
        Sk = (1 / llambda) * Sk - (1 / llambda) * Sk @ Omega.T.dot(Lambda).dot(Omega) @ Sk

        thetahat = thetahat + Tau.dot(ytilde)
        vs.Update(vs.A @ vs.X + dt*vs.F(vs_exact.X) + vs.B @ vs.u_input + phi @ thetahat + K @ ytilde + Upsilon @ Tau @ ytilde) # calcualtes x_hat

        timestamp.append(ti)
        x_state.append(vs_exact.X)
        x_hat.append(vs.X)
        theta_array.append(theta)
        theta_hat.append(thetahat)

        i += 1

        ti += dt 

    return np.array(timestamp).round(2), np.array(x_state), np.array(x_hat), np.array(theta_array), np.array(theta_hat)


def plot_results():

    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Purple = '#9D2EC5'
    CB91_Amber = '#F5B14C'

    xtab_plot0 = np.array([i[0] for i in x_state])
    xtab_plot1 = np.array([i[1] for i in x_state])
    xtab_plot2 = np.array([i[2] for i in x_state])
    xtab_plot3 = np.array([i[3] for i in x_state])
    xtab_plot4 = np.array([i[4] for i in x_state])
    xtab_plot5 = np.array([i[5] for i in x_state])
    xhatt_plot0 = np.array([i[0] for i in x_hat])
    xhatt_plot1 = np.array([i[1] for i in x_hat])
    xhatt_plot2 = np.array([i[2] for i in x_hat])
    xhatt_plot3 = np.array([i[3] for i in x_hat])
    xhatt_plot4 = np.array([i[4] for i in x_hat])
    xhatt_plot5 = np.array([i[5] for i in x_hat])
    ttab_plot = timestamp
    

    fig = plt.figure(figsize=(12, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(xtab_plot0.flatten(), xtab_plot1.flatten(), label = 'x', color = CB91_Blue)
    ax1.plot(xhatt_plot0.flatten(), xhatt_plot1.flatten(), label = 'x_hat', color = 'black', linestyle = 'dotted')
    ax1.grid()
    ax1.legend()
    ax1.set_title('Vessel\'s XY plot')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    ax2 = fig.add_subplot(1, 4, 3)
    ax2.plot(ttab_plot, xtab_plot3.flatten(), label = 'u', color = CB91_Purple)
    ax2.plot(ttab_plot, xtab_plot4.flatten(), label = 'v', color = CB91_Amber)
    ax2.plot(ttab_plot, xtab_plot5.flatten(), label = 'r', color = CB91_Green)
    ax2.plot(ttab_plot, xhatt_plot3.flatten(), label = 'u KE', color = CB91_Purple,  linestyle = 'dotted')
    ax2.plot(ttab_plot, xhatt_plot4.flatten(), label = 'v KE', color = CB91_Amber,  linestyle = 'dotted')
    ax2.plot(ttab_plot, xhatt_plot5.flatten(), label = 'r KE', color = CB91_Green,  linestyle = 'dotted')
    ax2.set_title('Vessel u,v and r rates')
    ax2.set_xlabel('Time [s]')
    ax2.legend()

    ax3 = fig.add_subplot(1, 4, 4)
    ax3.plot(ttab_plot, xtab_plot2.flatten(),label = '$\psi$', color = CB91_Amber)
    ax3.plot(ttab_plot, xhatt_plot2.flatten(),label = '$\psi KE$', color = CB91_Amber,  linestyle = 'dotted')
    ax3.set_title('Vessel\'s $\psi$')
    ax3.set_xlabel('Time [s]')
    ax3.legend()
    ax3.set_ylabel('$\psi$')

    fig.tight_layout()
    fig.suptitle('Vessel Dynamics')
    plt.show()

def theta_plots():

    fig2, axs = plt.subplots(2,1)
    ttab_plot = timestamp
    theta_plot0 = np.array([i[0] for i in theta_array])
    thetahat_plot0 = np.array([i[0] for i in thetahat])
    theta_plot1 = np.array([i[1] for i in theta_array])
    thetahat_plot1 = np.array([i[1] for i in thetahat])

    axs[0].plot(ttab_plot, theta_plot0.flatten(),label = '$\Theta_1$', color = 'black')
    axs[0].plot(ttab_plot, thetahat_plot0.flatten(),label = '$\Theta_1$ hat', color = 'red')
    axs[0].set_title('$\Theta$')
    axs[0].set_xlabel('Time [s]')
    axs[0].legend()
    axs[0].set_ylabel('$\Theta$')
    
    axs[1].plot(ttab_plot, theta_plot1.flatten(),label = '$\Theta_2$', color = 'black')
    axs[1].plot(ttab_plot, thetahat_plot1.flatten(),label = '$\Theta_2$ hat', color = 'red')
    axs[1].set_title('$\Theta$')
    axs[1].set_xlabel('Time [s]')
    axs[1].legend()
    axs[1].set_ylabel('$\Theta$')

    plt.subplots_adjust(hspace=0.5)

    plt.show()


if __name__ == '__main__':
    timestamp, x_state, x_hat, theta_array, thetahat = predict(
        t_tot=40, 
        ti=0,
        dt=0.01,
        u_input=np.array([1, 0], dtype=float))
    plot_results()
    # theta_plots()
