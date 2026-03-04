"""
nextnanopy: 1.0.3
nextnano++: 2.4.27 
"""

import nextnanopy as nn
from nextnanopy.utils.plotting import use_nxt_style
import matplotlib.pyplot as plt

use_nxt_style()

file_single_band = r"c:\Users\Heorhii\Documents\nextnano\OutputNnpy\InterbandTunneling_Duboz2019_nnp_1_sweep__BIAS3\TunnelCurrent_vs_bias_SingleBand.dat"
file_6band = r"c:\Users\Heorhii\Documents\nextnano\OutputNnpy\InterbandTunneling_Duboz2019_nnp_1_sweep__BIAS0\TunnelCurrent_vs_bias_KP6.dat"


single_band_data = nn.DataFile(file_single_band, product="nextnano++")
data_6band = nn.DataFile(file_6band, product="nextnano++")
print(single_band_data)

coord  = single_band_data.coords[0].value
current = single_band_data.variables[0].value

current_6band = data_6band.variables[0].value

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(coord, current, 'o-', label="Single Band")
ax.plot(coord, current_6band, 'o-', label="6-band k.p")
ax.set_xlabel("Bias (V)")
ax.set_ylabel("Current (A/cm$^2$)")
ax.set_title("Interband Tunneling Current vs Bias")
ax.set_yscale('log')
ax.set_ylim([1e-4, 1e0])
ax.legend()


plt.savefig("tutorials_interband_tunneling_in_nitride_junction-TunnelCurrent_vs_bias.png", dpi=2048/8)
plt.show()