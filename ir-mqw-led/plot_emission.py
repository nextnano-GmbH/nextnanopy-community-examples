"""
nextnanopy: 1.0.5
nextnano++: nextnano++ 2.5.1 
"""

import nextnanopy as nn
import numpy as np
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FuncFormatter

from pathlib import Path

use_nxt_style()


def sci_fmt(x, pos):
    if x == 0:
        return '0'
    exp = int(np.floor(np.log10(abs(x))))
    coef = x / 10**exp
    return r'${:.1f} \cdot 10^{{{}}}$'.format(coef, exp)
                                               
classical_folder_path = Path(r"c:\Users\Heorhii\Documents\nextnano\Output\LaserDiode_InGaAs_1D_cl_nnp")
quantum_folder_path = Path(r"c:\Users\Heorhii\Documents\nextnano\Output\LaserDiode_InGaAs_1D_qm_nnp")

# plot at 0.8 bias
classical_file = classical_folder_path / "bias_00008" / "OpticsSemiClassical" / "spont_emission_spectrum_photons_eV.dat"
quantum_file = quantum_folder_path / "bias_00008" / "OpticsSemiClassical" / "spont_emission_spectrum_photons_eV.dat"

def plot_emission_spectrum(ax, file, label):
    data = nn.DataFile(file, product="nextnano++")
    energy = data.coords[0].value
    spectrum = data.variables[0].value*1e12
    ax.plot(energy, spectrum, label=label)


fig, ax = plt.subplots(figsize=(8, 6))

ax.set_xlim(0.37, 1.4)
ax.set_ylim(0, 2.3e23)
ax.yaxis.set_major_formatter(FuncFormatter(sci_fmt))

plot_emission_spectrum(ax, classical_file, label="classical")
plot_emission_spectrum(ax, quantum_file, label="quantum")
ax.set_xlabel("Photon energy (eV)")
ax.set_ylabel(r"Emission $(\mathrm{photons\ s^{-1}\ cm^{-2}\ eV^{-1}})$")
ax.legend()

plt.tight_layout()

fig.savefig("tutorials_laser_diode-laserdiode_emission.png", dpi=2048/8)
plt.show()



