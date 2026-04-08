"""
nextnano++: 2.6.17 
nextnanopy: 1.0.5
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt


use_nxt_style()


single_band_paths  = [
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_calculation_1(1)",
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_calculation_2(1)",
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_calculation_3(1)",
]

kp8_paths = [
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_kp8_1_calculation_1(1)",
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_kp8_1_calculation_2(1)",
    r"c:\Users\Heorhii\Documents\nextnano\Output\zb_III-V_GaAs_excitonic-absorption_1D_kp8_1_calculation_3(1)",
]


def plot_absorption(ax, paths):
    labels = ["single particle", "excitonic (Colummb enhancement only)", "excitonic (Colummb enhancement + exciton peaks)"]
    for path, label in zip(paths, labels):
        data_folder = nn.DataFolder(path)
        data_file_path = data_folder.find("absorption_coeff_spectrum_y_eV.dat", deep=True)
        if not data_file_path:
            raise FileNotFoundError(f"absorption file not found in {path}")
        data_file_path = data_file_path[0]  # get the first match
        data_file = nn.DataFile(data_file_path, product="nextnano++")
        energy = data_file.coords[0].value
        absorption = data_file.variables[0].value
        print(f"Plotting {label} from {data_file_path}")
        ax.plot(energy, absorption, label=label)


fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
ax = axes[0]
ax.set_ylim(0, 32000)
ax.set_xlim(1.33, 1.75)
plot_absorption(ax, single_band_paths)
ax.legend()
ax.set_xlabel("Photon energy (eV)")
ax.set_ylabel(r"Absorption coefficient (cm$^{-1}$)")
# was -0.125
ax.text(0.03, 0.94, "a", transform=ax.transAxes, fontsize=18, fontweight="bold", va="bottom", ha="right")

ax = axes[1]
ax.set_ylim(0, 33000)
ax.set_xlim(1.33, 1.75)
plot_absorption(ax, kp8_paths)
ax.legend()
ax.set_xlabel("Photon energy (eV)")
# ax.set_ylabel(r"Absorption coefficient (cm$^{-1}$)")
ax.text(0.03, 0.94, "b", transform=ax.transAxes, fontsize=18, fontweight="bold", va="bottom", ha="right") 
fig.tight_layout()
fig.savefig(r"1D_exciton_in_infinite_quantum_well_absorption.png", dpi=2048/8)


plt.show()
    
