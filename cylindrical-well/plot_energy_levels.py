import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt

use_nxt_style()


folder_path = r"c:\Users\Heorhii\Documents\nextnano\Output\2DQuantumCorral_nnp"
states_file = folder_path + r"\bias_00000\Quantum\quantum_region\Gamma\energy_spectrum_k00000.dat"

data_file = nn.DataFile(states_file, product="nextnano++")

energies = data_file.variables[0].value
index = data_file.coords[0].value

plt.figure(figsize=(8, 6), dpi=1024/8)

plt.plot(index, energies, marker="o")

plt.xlabel("State index")
plt.ylabel("Energy (eV)")

plt.ylim(0, None)

plt.tight_layout()

plt.savefig("tutorial_quantum_corral-energies.png", dpi=1024/8)

plt.show()
