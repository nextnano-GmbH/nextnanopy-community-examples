"""
nextnanopy: 1.0.3
nextnano++: 2.3.9
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style, NXT_BLUE, WILD_STRAWBERRY
import matplotlib.pyplot as plt
import numpy as np

use_nxt_style()
path_sphere = r"c:\Users\Heorhii\Documents\nextnano\Output\QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_elipsoid_0"
path_ellips = r"c:\Users\Heorhii\Documents\nextnano\Output\QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_elipsoid_1"


dfolder_sphere = nn.DataFolder(path_sphere)
dfolder_ellips = nn.DataFolder(path_ellips)

plt.figure(figsize=(8,6))
# plot energies
for dfolder, label in zip([dfolder_sphere, dfolder_ellips], ['Spherical QD', 'Ellipsoidal QD']):
    energies_path = dfolder.go_to("bias_00000", "quantum", "quantum_region", "Gamma", "energy_spectrum_k00000.dat")
    data_file = nn.DataFile(energies_path, product="nextnano++")
    energies = data_file.variables["Energy"].value
    plt.plot(energies, marker='o', label=label)
plt.xticks(np.arange(0, 21, 2))  # Force x-ticks to integers
plt.xlim(0, 20)
plt.xlabel("State index")
plt.ylabel("Energy (eV)")
plt.legend()


plt.savefig("tu_QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_energies.png", dpi=1024/8)
plt.savefig("tu_QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_energies.svg")


# plot absorptions
plt.figure(figsize=(8,6))
for dfolder, label in zip([dfolder_sphere, dfolder_ellips], ['Spherical QD', 'Ellipsoidal QD']):
    absorption_path = dfolder.find("absorption", deep=True)[0]
    data_file = nn.DataFile(absorption_path, product="nextnano++")
    coord = data_file.coords[0].value
    absorption = data_file.variables[0].value
    plt.plot(coord, absorption, label=label)

plt.xlim(1.5, 3.0)
plt.ylim(0, 4050)
plt.legend()

plt.savefig("tu_QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_abs.png", dpi=1024/8)
plt.savefig("tu_QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_abs.svg")

plt.show()
