from vessel_setup import *
# TABS FOR BOOK-KEEPING
xtab_FE = []
ttab_FE = []

while t < Ttot:
    x = A.dot(x) + dt*F(x) + dt*B.dot(u) # Forward Euler
    xtab_FE.append(x)    
    ttab_FE.append(t)
    t = t + dt 

# PLOTS
def plot_results():

    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Purple = '#9D2EC5'
    CB91_Violet = '#661D98'
    CB91_Amber = '#F5B14C'

    xtab_plot = np.array(xtab_FE)
    ttab_plot = np.array(ttab_FE)
    fig = plt.figure(figsize=(12, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(xtab_plot[:,0,:].flatten(), xtab_plot[:,1,:].flatten(), color = CB91_Blue)
    ax1.grid()
    ax1.set_title('Vessel\'s XY plot')
    ax1.set_xlabel('X')
    ax1.set_ylabel('X')

    ax2 = fig.add_subplot(1, 4, 3)
    ax2.plot(ttab_plot, xtab_plot[:,3,:].flatten(), label = 'u', color = CB91_Purple)
    ax2.plot(ttab_plot, xtab_plot[:,4,:].flatten(), label = 'v', color = CB91_Amber)
    ax2.plot(ttab_plot, xtab_plot[:,5,:].flatten(), label = 'r', color = CB91_Green)
    ax2.set_title('Vessel u,v and r rates')
    ax2.set_xlabel('Time [s]')
    ax2.legend()

    ax3 = fig.add_subplot(1, 4, 4)
    ax3.plot(ttab_plot, xtab_plot[:,2,:].flatten(),label = '$\psi$', color = CB91_Violet)
    ax3.set_title('Vessel\'s $\psi$')
    ax3.set_xlabel('Time [s]')
    ax3.set_ylabel('$\psi$')

    fig.tight_layout()
    fig.suptitle('Vessel Dynamics')
    plt.show()


if __name__ == '__main__':
    plot_results()
