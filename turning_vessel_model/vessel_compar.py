from vessel_FE import ttab_FE, xtab_FE
from vessel_RK import ttab_RK, xtab_RK
from vessel_setup import *

def plot_compar():

    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Purple = '#9D2EC5'
    CB91_Violet = '#661D98'
    CB91_Amber = '#F5B14C'

    xtab_RK1 = np.array(xtab_RK)
    ttab_RK1 = np.array(ttab_RK)
    xtab_FE1= np.array(xtab_FE)
    ttab_FE1 = np.array(ttab_FE)

    fig = plt.figure(figsize=(12, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(xtab_FE1[:,0,:].flatten(), xtab_FE1[:,1,:].flatten(), color = CB91_Blue, label='fe')
    ax1.plot(xtab_RK1[:,0,:].flatten(), xtab_RK1[:,1,:].flatten(), color = 'b', label='rk')
    ax1.grid()
    ax1.set_title('Vessel\'s XY plot')
    ax1.set_xlabel('X')
    ax1.set_ylabel('X')

    ax2 = fig.add_subplot(1, 4, 3)
    ax2.plot(ttab_FE1, xtab_FE1[:,3,:].flatten(), label = 'u_FE', color = '#880808')
    ax2.plot(ttab_FE1, xtab_FE1[:,4,:].flatten(), label = 'v_FE', color = '#EE4B2B')
    ax2.plot(ttab_FE1, xtab_FE1[:,5,:].flatten(), label = 'r_FE', color = '#DE3163')

    ax2.plot(ttab_RK1, xtab_RK1[:,3,:].flatten(), label = 'u_RK', color = '#00FFFF')
    ax2.plot(ttab_RK1, xtab_RK1[:,4,:].flatten(), label = 'v_RK', color = '#89CFF0')
    ax2.plot(ttab_RK1, xtab_RK1[:,5,:].flatten(), label = 'r_RK', color = '#088F8F')
    
    ax2.set_title('Vessel u,v and r rates')
    ax2.set_xlabel('Time [s]')
    ax2.legend()

    ax3 = fig.add_subplot(1, 4, 4)
    ax3.plot(ttab_FE1, xtab_FE1[:,2,:].flatten(),label = '$\psi$', color = '#00A36C')
    ax3.plot(ttab_RK1, xtab_RK1[:,2,:].flatten(),label = '$\psi$', color = 'orange')
    ax3.set_title('Vessel\'s $\psi$')
    ax3.set_xlabel('Time [s]')
    ax3.set_ylabel('$\psi$')

    fig.tight_layout()
    fig.suptitle('Vessel Dynamics')
    plt.show()

plot_compar()