"""
nextnano++: 2.5.1
nextnanopy: 1.0.5
"""

from pathlib import Path
import numpy as np
import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
from nextnanopy.utils.plotting import NXT_BLUE, GREEN, NXT_BLUE_COLORMAP, DANDELION
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

use_nxt_style()

folder_path = Path(r"c:\Users\Heorhii\Documents\nextnano\Output\2DQuantumCorral_nnp")
structure_file = folder_path / "Structure" / "materials.vtr"
states_file = folder_path / "bias_00000" / "Quantum" / "quantum_region" / "Gamma" / "probabilities_k00000.vtr"


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


def plot_structure_borders_3d(ax, data_file, color="white", linewidth=1.0):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    material_var = data_file.variables[0].value

    material_ids = np.unique(material_var).astype(int)
    levels = (material_ids[:-1] + material_ids[1:]) / 2.0

    zlim = ax.get_zlim()
    ax.contour(x, y, material_var.T, levels=levels,
               colors=[color], linewidths=linewidth, zdir="z", offset=0)
    ax.set_zlim(zlim)
    ax.grid(False)


def plot_probabilities(ax, data_file, state_index, vmin, vmax):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    psi2 = data_file.variables[state_index - 1].value

    mesh = ax.pcolormesh(x, y, psi2.T, cmap=NXT_BLUE_COLORMAP, shading="auto",
                         vmin=vmin, vmax=vmax)
    ax.set_aspect("equal", adjustable="box")
    return mesh


def plot_probabilities_surface(ax, data_file, state_index, vmin, vmax, z_aspect=0.5):
    x = data_file.coords[0].value
    y = data_file.coords[1].value
    psi2 = data_file.variables[state_index - 1].value

    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, psi2.T, cmap=NXT_BLUE_COLORMAP, edgecolor="none",
                           vmin=vmin, vmax=vmax)
    ax.set_box_aspect((1, 1, z_aspect))
    ax.set_xlabel("x (nm)")
    ax.set_ylabel("y (nm)")
    ax.set_zticks([])
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_facecolor((0.3, 0.3, 0.3, 1.0))
    return surf


data_file_structure = nn.DataFile(structure_file, product="nextnano++")
data_file_states = nn.DataFile(states_file, product="nextnano++")

psi2_all = np.stack([data_file_states.variables[i].value for i in range(9)])
vmin, vmax = psi2_all.min(), psi2_all.max()

fig, ax = plt.subplots(figsize=(6, 6))
plot_structure(ax, data_file_structure)
ax.set_xlabel("x (nm)")
ax.set_ylabel("y (nm)")
ax.grid(False)

for i in range(1, 10):
    fig = plt.figure(figsize=(12, 6))
    ax_flat = fig.add_subplot(1, 2, 1)
    ax_surf = fig.add_subplot(1, 2, 2, projection="3d")

    mesh = plot_probabilities(ax_flat, data_file_states, state_index=i, vmin=vmin, vmax=vmax)
    plot_structure_borders(ax_flat, data_file_structure)
    ax_flat.set_xlabel("x (nm)")
    ax_flat.set_ylabel("y (nm)")
    ax_flat.grid(False)

    plot_probabilities_surface(ax_surf, data_file_states, state_index=i, vmin=vmin, vmax=vmax)
    plot_structure_borders_3d(ax_surf, data_file_structure, linewidth=2.0)
    fig.colorbar(mesh, ax=[ax_flat, ax_surf], label=r"$|\Psi|^2$")

plt.show()
