"""
nextnanopy: 1.0.3
nextnano++: 2.3.9
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style, NXT_BLUE, WILD_STRAWBERRY, GREEN, GREEN, NXT_BLUE_COLORMAP, NXT_STRAWBERRY_COLORMAP, DANDELION
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


use_nxt_style()

path = r"c:\Users\Heorhii\Documents\nextnano\Output\UVC-LED_wz_III-N_1D"
datafolder = nn.DataFolder(path)
bandedges_path = datafolder.go_to("bias_00000", "bandedges.dat")

# plot bandedges

bandedges = nn.DataFile(bandedges_path, product="nextnano++")
coord = bandedges.coords[0].value
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

ax = axes[0, 0]
var_names = ["Gamma", "HH", "LH", "SO", "electron_Fermi_level", "hole_Fermi_level"]
labels = ["CB", "HH", "LH", "SO", "E$_F$ (el)", "E$_F$ (hl)"]
colors = [WILD_STRAWBERRY, NXT_BLUE, "black", DANDELION, NXT_BLUE, GREEN]
styles = ["-", "-", "-", "-", "--", "--"]
widths = [2, 2, 2, 2, 1, 1]

axins = inset_axes(ax, width="30%", height="30%", loc='lower left', bbox_to_anchor=(0.6, 0.2, 1, 1),  # (x, y, width, height) in axes fraction
    bbox_transform=ax.transAxes, borderpad=0)

x1, x2 = 490, 530  # x-limits for zoom
y1, y2 = -6.5, -5.5      # y-limits for zoom
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.tick_params(labelsize=10)

for var_name, label, color, style, width in zip(var_names, labels, colors, styles, widths):
    var = bandedges.get_variable(var_name)
    ax.plot(coord, var.value, label=label, color=color, linestyle=style, linewidth=width)
    axins.plot(coord, var.value, label=label, color=color, linestyle=style, linewidth=1)
ax.set_xlabel("Coordinate (nm)")
ax.set_ylabel("Energy (eV)")
ax.set_xlim(470, 580)
ax.legend()

# recombination

recombination_path = datafolder.go_to("bias_00000", "recombination.dat")

var_names = ["Auger", "SRH", "radiative"]
labels = ["Auger", "SRH", "Radiative"]

recombination = nn.DataFile(recombination_path, product="nextnano++")

ax = axes[1, 0]
for var_name, label in zip(var_names, labels):
    var = recombination.get_variable(var_name)
    ax.plot(coord, var.value*1e18, label=label)

ax.set_xlabel("Coordinate (nm)")
ax.set_ylabel(r"Recombination rate (cm$^{-3}$s$^{-1}$)")
ax.set_yscale("log")
ax.set_xlim(490, 530)
ax.legend()

# electron density
density_electron_path = datafolder.go_to("bias_00000", "electron_density_vs_energy.fld")
density_electron = nn.DataFile(density_electron_path, product="nextnano++")

ax = axes[0, 1]
# plot density
x = density_electron.coords['x'].value
y = density_electron.coords['y'].value
density = density_electron.variables[0].value
ax.set_xlim(480, 530)
ax.set_ylim(-0.73, 0.15)
# CB and fermi level
ax.plot(bandedges.coords[0].value, bandedges.get_variable("Gamma").value, color="white", linestyle="-", label="CB edge")
ax.plot(bandedges.coords[0].value, bandedges.get_variable("electron_Fermi_level").value, color="white", linestyle="--", label="Electron Fermi level")
pcm = ax.pcolormesh(x, y, density.T, shading='auto', cmap=NXT_STRAWBERRY_COLORMAP)
cbar = fig.colorbar(pcm, ax=ax, label='Electron Density ($10^{18}$ cm$^{-3}$ eV$^{-1}$)')
ax.set_xlabel('Position (nm)')
ax.set_ylabel('Energy (eV)')

# hole density

density_hole_path = datafolder.go_to("bias_00000", "hole_density_vs_energy.fld")
density_hole = nn.DataFile(density_hole_path, product="nextnano++")

ax = axes[1, 1]
# plot density

x = density_hole.coords['x'].value
y = density_hole.coords['y'].value
density = density_hole.variables[0].value

ax.set_xlim(480, 530)
ax.set_ylim(-6.33, -5.7)
# VB and fermi level
ax.plot(bandedges.coords[0].value, bandedges.get_variable("SO").value, color="white", linestyle="-", label="VB edge")
ax.plot(bandedges.coords[0].value, bandedges.get_variable("hole_Fermi_level").value, color="white", linestyle="--", label="Hole Fermi level")
pcm = ax.pcolormesh(x, y, density.T, shading='auto', cmap=NXT_BLUE_COLORMAP)
cbar = fig.colorbar(pcm, ax=ax, label='Hole Density ($10^{18}$ cm$^{-3}$ eV$^{-1}$)')
ax.set_xlabel('Position (nm)')
ax.set_ylabel('Energy (eV)')


fig.savefig("t_UVC-LED_wz_III-N_1D_profiles.png", dpi=4098/16)





plt.show()




 