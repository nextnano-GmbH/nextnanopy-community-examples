import nextnanopy as nn
import matplotlib.pyplot as plt
from nextnanopy.utils.plotting import use_nxt_style, WILD_STRAWBERRY, NXT_BLUE
import numpy as np

use_nxt_style()


path_single_band = r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_InGaAs-AlGaAs_2DEG_occupation_1D_use_8_band_model_0"
path_8kp = r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_InGaAs-AlGaAs_2DEG_occupation_1D_use_8_band_model_1"

# limits for plotting
XMIN = 0 # nm
XMAX = 52 # nm
SI_DOPING_START = 17 # nm
SI_DOPING_END = 20 # nm

def plot_densities(ax, path, number_of_states=4, state_factor=1, model="Gamma"):
    data_folder = nn.DataFolder(path)
    bandedges_path = data_folder.go_to('bias_00000', 'bandedges.dat')
    bandedges_file = nn.DataFile(bandedges_path, product="nextnano++")
    coord = bandedges_file.coords[0].value
    gamma_bandedge = bandedges_file.variables["Gamma"].value
    ax.plot(coord, gamma_bandedge, label="conduction band edge", ls='--', lw=1, alpha=0.4, color=WILD_STRAWBERRY)

    data_file_path = data_folder.go_to('bias_00000', 'Quantum', "2DEG", model, 'density_subbands.dat')
    data_file = nn.DataFile(data_file_path, product="nextnano++")
    coord = data_file.coords[0].value

    for state_index in range(number_of_states):
        subband_density = data_file.variables[state_index*state_factor].value
        subband_density = np.abs(subband_density) # plot always positive density
        ax.plot(coord, subband_density, color=NXT_BLUE)
    ax.set_xlim(XMIN, XMAX)
    ax.set_xlabel("Position (nm)")
    ax.set_ylabel("Subband Density (10$^{18}$ cm$^{-3}$)")


def plot_doping(ax):
    ax.axvspan(SI_DOPING_START, SI_DOPING_END, color='gray', alpha=0.4, label="Si doping")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

plot_densities(ax[0], path_single_band)
plot_densities(ax[1], path_8kp, number_of_states=8, model="kp8")
# plot_doping(ax[0])
# plot_doping(ax[1])
# ax[0].legend()
# ax[1].legend()

fig.savefig("zb_III-V_InGaAs-AlGaAs_2DEG_occupation_1D_subband_densities.png", dpi=2048/12)

plt.show()




