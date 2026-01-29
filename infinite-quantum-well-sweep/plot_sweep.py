"""
nextnanopy: 1.0.3
nextnano++: 2.4.27 
"""

from pathlib import Path
import json

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style, WILD_STRAWBERRY, GREEN
import matplotlib.pyplot as plt
import numpy as np

use_nxt_style()

this_dir = Path(__file__).parent.resolve()
input_file_path = this_dir / "1D_IntersubbandAbsorption_InfiniteWell_GaAs_Chuang_sg.nnp"

run_sweep = False
sweep_var =  "QuantumWellWidth" # 
if run_sweep:
    sweep_values = np.linspace(7.5, 20, 100) # nm

    sweep = nn.Sweep({sweep_var: sweep_values}, input_file_path)

    sweep.save_sweep(integer_only_in_name=True)
    sweep.execute_sweep(delete_input_files=True, show_log=False)
    sweep_infodict = sweep.sweep_output_infodict
else:
    sweep_folder_loc = r"c:\Users\Heorhii\Documents\nextnano\OutputNnpy\1D_IntersubbandAbsorption_InfiniteWell_GaAs_Chuang_sg_sweep__QuantumWellWidth4"
    sweep_infodict_path = Path(sweep_folder_loc) / 'sweep_infodict.json'
    with open(sweep_infodict_path, 'r') as json_file:
        sweep_infodict = json.load(json_file)
    

fig, ax = plt.subplots(figsize=(8, 6))

energy = []
well_widths = []

for folder, vars in sweep_infodict.items():
    well_width = vars[sweep_var]
    data_folder = nn.DataFolder(folder)

    data_file_path = data_folder.go_to('bias_00000', 'Quantum', "quantum_region", "Gamma", 'energy_spectrum_k00000.dat')
    data_file = nn.DataFile(data_file_path, product="nextnano++")
    energy_array = data_file.variables[0].value # scale for better plotting
    ground_state_energy = energy_array[0]  # First energy level
    first_excited_state_energy = energy_array[1]  # Second energy level
    transition_energy = first_excited_state_energy - ground_state_energy

    energy.append(transition_energy)
    well_widths.append(well_width)

ax.plot(well_widths, energy, label="Energy")
y_min = 0
xmax = max(well_widths)
xmin = min(well_widths)

x_intersect = 12.80762256
y_intersect = np.interp(x_intersect, well_widths, energy)
ax.vlines(x_intersect, ymin=0, ymax=y_intersect, color=WILD_STRAWBERRY, linestyle='--')
ax.plot(x_intersect, y_intersect, 'o', color=WILD_STRAWBERRY, label="Optimal point")

x_start = 10.0
ax.vlines(x_start, ymin=0, ymax=np.interp(x_start, well_widths, energy), color='black', linestyle='--')
ax.plot(x_start, np.interp(x_start, well_widths, energy), 'o', color='black', label="Initial point")

target_energy = 0.1 # eV
ax.hlines(target_energy, xmin, xmax, colors=GREEN, linestyles='--', label="Target energy")

ax.set_xlim(xmin, xmax)
ax.set_ylim(y_min, max(energy)*1.1)

ax.set_xlabel("Quantum Well Width (nm)")
ax.set_ylabel("Transition Energy (eV)")
ax.legend()


fig.savefig(this_dir / "tut_1D_infinite_well_optimization_sweep.png", dpi=1024/8)
plt.show()