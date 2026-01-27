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

gain_TE = datafolder.go_to("bias_00000", "OpticsQuantum", "optics_region", "gain_spectrum_TEy_eV.dat")
gain_TM = datafolder.go_to("bias_00000", "OpticsQuantum", "optics_region", "gain_spectrum_TMx_eV.dat")


fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# plot gain
gain_TE_file = nn.DataFile(gain_TE, product="nextnano++")
gain_TM_file = nn.DataFile(gain_TM, product="nextnano++")

ax = axes[0]
ax.plot(gain_TE_file.coords[0].value, gain_TE_file.variables[0].value, label="TE")
ax.plot(gain_TM_file.coords[0].value, gain_TM_file.variables[0].value, label="TM")

ax.set_xlabel("Photon energy (eV)")
ax.set_ylabel("Gain (cm$^{-1}$)")
ax.set_xlim(5.05, 6.0)
ax.set_ylim(0, None)
ax.legend()

ax = axes[1]
# plot spontaneous emission

emission_TE_path = datafolder.go_to("bias_00000", "OpticsQuantum", "optics_region", "spont_emission_spectrum_power_TEy_eV.dat")
emission_TM_path = datafolder.go_to("bias_00000", "OpticsQuantum", "optics_region", "spont_emission_spectrum_power_TMx_eV.dat")

emission_TE_file = nn.DataFile(emission_TE_path, product="nextnano++")
emission_TM_file = nn.DataFile(emission_TM_path, product="nextnano++")

ax.plot(emission_TE_file.coords[0].value, emission_TE_file.variables[0].value, label="TE")
ax.plot(emission_TM_file.coords[0].value, emission_TM_file.variables[0].value, label="TM")

ax.set_xlabel("Photon energy (eV)")
ax.set_ylabel("Emission power (W eV $^{-1}$ cm$^{-3}$)")

ax.set_xlim(5.05, 6.0)
ax.set_ylim(0, None)


fig.savefig(r"t_UVC-LED_wz_III-N_1D_spectra.png", dpi=2048/16)
plt.show()




 