"""
nextnanopy: 1.0.3
nextnano++: 2.4.27 
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt

use_nxt_style()


sweep_folder = r"c:\Users\Heorhii\Documents\nextnano\OutputNnpy\InterbandTunneling_Duboz2019_nnp_1_sweep__BIAS0"

# check sweep_infodict.json for the exact folders and biases
bias1 = 0.2 # V
bias2 = 0.7 # V
bias1_folder = "InterbandTunneling_Duboz2019_nnp_2"
bias2_folder = "InterbandTunneling_Duboz2019_nnp_7"

def plot_bandedges(ax, sweep_folder, bias_folder):
    data_folder = nn.DataFolder(sweep_folder)
    data_file_path = data_folder.go_to(bias_folder, 'bias_00000', "bandedges.dat")
    data_file = nn.DataFile(data_file_path, product="nextnano++")
    coord = data_file.coords[0].value
    
    hh = data_file.variables["HH"].value
    gamma = data_file.variables["Gamma"].value
    
    hole_fermi_level = data_file.variables["hole_Fermi_level"].value
    el_fermi_level = data_file.variables["electron_Fermi_level"].value

    ax.plot(coord, hh, label="HH")
    ax.plot(coord, gamma, label="Gamma")
    ax.plot(coord, el_fermi_level, linestyle='--', label="Electron Fermi Level")
    ax.plot(coord, hole_fermi_level, linestyle='--', label="Hole Fermi Level")
    ax.set_xlabel("Position (nm)")
    ax.set_ylabel("Energy (eV)")
    ax.legend()


fig, axes = plt.subplots(1, 2, figsize=(16, 6))
plot_bandedges(axes[0], sweep_folder, bias1_folder)

plot_bandedges(axes[1], sweep_folder, bias2_folder)
plt.savefig("1D_interband_tunneling_in_nitride_junction_bandedges.png", dpi=2048/8)

plt.show()

