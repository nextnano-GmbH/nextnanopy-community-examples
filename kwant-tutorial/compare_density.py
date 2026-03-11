from pathlib import Path

import matplotlib.pyplot as plt
import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style

use_nxt_style()

path_classical = Path(r"C:\Users\Heorhii\Documents\nextnano\Output\3D_conductance_in_top_gated_2DEG_nnp(1)")
path_quantum = Path(r"C:\Users\Heorhii\Documents\nextnano\Output\3D_conductance_in_top_gated_2DEG_QM_exercise_nnp")


# plot density at bias -0.3V
def plot_density(ax, path, label):
    density_file = nn.DataFile(path / "bias_00080" / "density_electron_1d_section_line_x_center.dat", product="nextnano++")
    coord = density_file.coords[0].value
    density = density_file.variables[0].value
    ax.plot(coord, density, label=label)

fig, ax = plt.subplots(figsize=(8, 6))
plot_density(ax, path_classical, label="without quantization")
plot_density(ax, path_quantum, label="with quantization")

ax.set_xlabel("Position (nm)")
ax.set_ylabel("Electron density (10$^{18}$ cm$^{-3}$)")
ax.legend()
ax.set_xlim(95, 240)
ax.set_ylim(0, None)
fig.savefig("3D_conductance_in_top_gated_2DEG_density_profiles.png", dpi=2048/8)
plt.show()