import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv, jn_zeros
from nextnanopy.utils.plotting import use_nxt_style

use_nxt_style()

x = np.linspace(0, 10, 500)

J0 = jv(0, x)
J1 = jv(1, x)
J2 = jv(2, x)

plt.figure(figsize=(8, 6), dpi=1024/8)

plt.plot(x, J0, label=r"$\ell=0$")
plt.plot(x, J1, label=r"$\ell=1$")
plt.plot(x, J2, label=r"$\ell=2$")

# horizontal line at y = 0 for better visibility of zeros
plt.axhline(0, color='black', linestyle='--', linewidth=1.0)

ax = plt.gca()
plt.xlim(0, 10)

n_zeros = 3
# shifts for better placement of labels, keyed by (ell, zero_index)
x_shifts = {
    (0, 1): 0.1,
    (1, 1): 0.05,
    (2, 1): 0.05,
    (0, 2): -0.05,
    (1, 2): -0.05,
    (2, 2): -0.25,
    (0, 3): 0.25,

}
for ell, color in zip([0, 1, 2], ['C0', 'C1', 'C2']):
    zeros = jn_zeros(ell, n_zeros)
    
    for i, z in enumerate(zeros, start=1):
        if z > 10:  # stay within plotting range
            continue
        
        # value is ~0, but we use a small vertical offset
        ax.text(z + x_shifts.get((ell, i), 0), 0.05, rf"$J_{{{ell}{i}}}$", color=color,
                ha='center')

# plt.title("Bessel functions of the first kind")
plt.xlabel(r"$x$")
plt.ylabel(r"$J_\ell(x)$")

plt.legend()

plt.savefig("tutorial_quantum_corral-bessel-functions.png", dpi=1024/8)

plt.tight_layout()
plt.show()

