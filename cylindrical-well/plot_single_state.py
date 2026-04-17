"""
nextnano++: 2.5.1
nextnanopy: 1.0.5
"""

import numpy as np
import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style, NXT_BLUE_COLORMAP
import matplotlib.pyplot as plt

use_nxt_style()

# --- parameters ---
STATE_INDEX = 1

# adjust folder path as needed
folder_path = r"c:\Users\Heorhii\Documents\nextnano\Output\2DQuantumCorral_nnp"
states_file = folder_path + r"\bias_00000\Quantum\quantum_region\Gamma\probabilities_k00000.vtr"

# --- load data ---
data_file = nn.DataFile(states_file, product="nextnano++")

x = data_file.coords[0].value
y = data_file.coords[1].value
psi2 = data_file.variables[STATE_INDEX - 1].value

# --- flat colormap ---
fig, ax = plt.subplots(figsize=(6, 6))
mesh = ax.pcolormesh(x, y, psi2.T, cmap=NXT_BLUE_COLORMAP, shading="auto")
plt.colorbar(mesh, ax=ax, label=r"$|\Psi|^2$")
ax.set_aspect("equal")
ax.set_xlabel("x (nm)")
ax.set_ylabel("y (nm)")
ax.grid(False)

# --- 3D surface ---
fig = plt.figure(figsize=(6, 6))
ax3d = fig.add_subplot(111, projection="3d")
X, Y = np.meshgrid(x, y)
surf = ax3d.plot_surface(X, Y, psi2.T, cmap=NXT_BLUE_COLORMAP, edgecolor="none", shade=False,
                         antialiased=False, rcount=psi2.shape[0], ccount=psi2.shape[1])
plt.colorbar(surf, ax=ax3d, label=r"$|\Psi|^2$")
ax3d.set_box_aspect((1, 1, 0.5))
ax3d.set_xlabel("x (nm)")
ax3d.set_ylabel("y (nm)")
ax3d.set_zticks([])

plt.show()
