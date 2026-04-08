"""
nextnano++: 2.6.17 
nextnanopy: 1.0.5
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt


use_nxt_style()


single_band_path = r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_calculation_1(1)"

kp8_path = r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_kp8_1_calculation_1(1)"


def plot_bandedges(ax, path):
    data_folder = nn.DataFolder(path)
    data_file_path = data_folder.find("bandedges.dat", deep=True)
    if not data_file_path:
        raise FileNotFoundError(f"bandedges file not found in {path}")
    data_file_path = data_file_path[0]  # get the first match
    data_file = nn.DataFile(data_file_path, product="nextnano++")
    coord = data_file.coords[0].value
    
    hh = data_file.variables["HH"].value
    gamma = data_file.variables["Gamma"].value
    

    ax.plot(coord, hh, ls="--", label="HH")
    ax.plot(coord, gamma, ls="--",label="Gamma")
    ax.legend()

def plot_states_single_band(ax, path, number_of_states_per_band=4):
    data_folder = nn.DataFolder(path)
    data_file_paths = data_folder.find("probabilities_shift_k00000.dat", deep=True)
    if not data_file_paths:
        raise FileNotFoundError(f"states file not found in {path}")
    for df_path in data_file_paths:
        data_file = nn.DataFile(df_path, product="nextnano++")
        position = data_file.coords[0].value
        for i in range(1, number_of_states_per_band+1):
            psi_squared = data_file.variables[f"Psi^2_{i}"].value
            ax.plot(position, psi_squared, lw=1, color="black")

def plot_states_kp8(ax, path, min_index=10, max_index=20):
    data_folder = nn.DataFolder(path)
    data_file_path = data_folder.find("probabilities_shift_k00000.dat", deep=True)
    if not data_file_path:
        raise FileNotFoundError(f"states file not found in {path}")
    data_file_path = data_file_path[0]  # get the first match
    data_file = nn.DataFile(data_file_path, product="nextnano++")
    energy = data_file.coords[0].value
    for i in range(min_index, max_index+1):
        psi_squared = data_file.variables[f"Psi^2_{i}"].value
        ax.plot(energy, psi_squared, lw=1, color="black")


fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

ax = axes[0]
plot_bandedges(ax, single_band_path)
plot_states_single_band(ax, single_band_path)
# -0.1, 1.02 to mark outside of the plot area
ax.text(0.03, 0.94, "a", transform=ax.transAxes, fontsize=18, fontweight="bold", va="bottom", ha="right")
ax.set_xlim(0, 10)
ax.set_ylim(-0.784, 2.2)
ax.set_xlabel("Position (nm)")
ax.set_ylabel("Energy (eV)")
ax = axes[1]
plot_bandedges(ax, kp8_path)
plot_states_kp8(ax, kp8_path, min_index=64, max_index=80)
ax.text(0.03, 0.94, "b", transform=ax.transAxes, fontsize=18, fontweight="bold", va="bottom", ha="right")
ax.set_xlim(0, 10)
ax.set_xlabel("Position (nm)")
# ax.set_ylabel("Energy (eV)")
fig.tight_layout()
fig.savefig(r"1D_exciton_in_infinite_quantum_well_states.png", dpi=2048/8)
plt.show()