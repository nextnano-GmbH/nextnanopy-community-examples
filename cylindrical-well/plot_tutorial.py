"""
nextnano++: 2.5.1
nextnanopy: 1.0.5
"""

from pathlib import Path
import numpy as np
import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
from nextnanopy.utils.plotting import NXT_BLUE, GREEN, NXT_BLUE_COLORMAP
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

use_nxt_style()
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"

folder_path = Path(r"c:\Users\Heorhii\Documents\nextnano\Output\2DQuantumCorral_nnp")
structure_file = folder_path / "Structure" / "materials.vtr"
states_file = folder_path / "bias_00000" / "Quantum" / "quantum_region" / "Gamma" / "probabilities_k00000.vtr"

STATES = [1, 2, 3, 4, 5, 6, 15, 20]


def plot_structure(ax, data_file):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    material_var = data_file.variables[0].value

    material_ids = np.unique(material_var).astype(int)
    n = len(material_ids)
    id_to_index = {mid: i for i, mid in enumerate(material_ids)}
    remapped = np.vectorize(id_to_index.get)(material_var.astype(int))

    cmap = ListedColormap([NXT_BLUE, "black", GREEN][:n])
    norm = BoundaryNorm(np.arange(n + 1) - 0.5, ncolors=n)

    ax.pcolormesh(x, y, remapped.T, cmap=cmap, norm=norm, shading="auto")
    ax.set_aspect("equal", adjustable="box")


def plot_structure_borders(ax, data_file, color="white", linewidth=1.0):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    material_var = data_file.variables[0].value

    material_ids = np.unique(material_var).astype(int)
    levels = (material_ids[:-1] + material_ids[1:]) / 2.0

    ax.contour(x, y, material_var.T, levels=levels,
               colors=color, linewidths=linewidth)


def plot_probabilities(ax, data_file, state_index):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    psi2 = data_file.variables[state_index - 1].value

    mesh = ax.pcolormesh(x, y, psi2.T, cmap=NXT_BLUE_COLORMAP, shading="auto")
    ax.set_aspect("equal", adjustable="box")
    return mesh


def plot_probabilities_surface(ax, data_file, state_index, z_aspect=0.5):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    psi2 = data_file.variables[state_index - 1].value

    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, psi2.T, cmap=NXT_BLUE_COLORMAP, edgecolor="none",
                           shade=False, antialiased=False,
                           rcount=psi2.shape[0], ccount=psi2.shape[1])
    ax.set_box_aspect((1, 1, z_aspect))
    ax.set_zticks([])
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.fill = True
        pane.set_facecolor("darkgray")
    return surf


data_file_structure = nn.DataFile(structure_file, product="nextnano++")
data_file_states = nn.DataFile(states_file, product="nextnano++")

# --- fig 1: structure ---
fig, ax = plt.subplots(figsize=(6, 6))
plot_structure(ax, data_file_structure)
ax.set_xlabel("x (nm)")
ax.set_ylabel("y (nm)")
ax.grid(False)

# --- fig 2: 4 rows x 4 cols ---
# rows 0-1: flat colormap (states split into two groups of 4)
# rows 2-3: 3D surface (same grouping)
N_COLS = 4
N_ROWS = 4
flat_states  = STATES[:4], STATES[4:]   # row 0, row 1
surf_states  = STATES[:4], STATES[4:]   # row 2, row 3

fig2 = plt.figure(figsize=(N_COLS * 3.5, N_ROWS * 4))
letters = iter("abcdefghijklmnop")
n_l_pairs = ["(1, 1)", "(1, 1)", "(1, -1)", "(1, 2)",
             "(1, -2)", "(2, 0)", "(1, 6)", "(3, 1)"]

for row in range(N_ROWS):
    is_surface = row >= 2
    group = (flat_states if not is_surface else surf_states)[row % 2]

    for col, state in enumerate(group):
        subplot_idx = row * N_COLS + col + 1
        letter = next(letters)

        is_left = col == 0
        is_bottom_flat = row == 1

        if is_surface:
            ax = fig2.add_subplot(N_ROWS, N_COLS, subplot_idx, projection="3d")
            plot_probabilities_surface(ax, data_file_states, state)
            ax.text2D(0.05, 0.95, letter, transform=ax.transAxes,
                      fontsize=14, fontweight="bold", va="bottom", ha="right")        
        else:
            ax = fig2.add_subplot(N_ROWS, N_COLS, subplot_idx)
            plot_probabilities(ax, data_file_states, state)
            plot_structure_borders(ax, data_file_structure)
            ax.grid(False)
            ax.text(0.05, 1.02, letter, transform=ax.transAxes,
                    fontsize=14, fontweight="bold", va="bottom", ha="right")
            ax.set_xlabel("x (nm)" if is_bottom_flat else "")
            ax.set_ylabel("y (nm)" if is_left else "")
            ax.tick_params(labelbottom=is_bottom_flat, labelleft=is_left)
            ax.set_title(f"State {state}, (n, l) = {n_l_pairs[STATES.index(state)]}", fontsize=12)

fig2.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.05, hspace=0.05, wspace=0.05)
# fig2.tight_layout()
fig.savefig("tutorial_quantum_corral_structure.png", dpi=300)
fig2.savefig("tutorial_quantum_corral_states.png", dpi=300)
# plt.show()
