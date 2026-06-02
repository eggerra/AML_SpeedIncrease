import numpy as np
import matplotlib.pyplot as plt

# Operating point: 10mm lift, 250N force
lifts = np.linspace(0, 10, 20)
forces = 19 * lifts + 0.6 * (lifts**2)

# Geometric parameters for stress calculation (at highest stress location - top coils)
D_mean = 14.92
a = 2.92 # minor axis
b = 3.66 # major axis
k = 1.15 # Wahl concentration factor

# Formulas (in comments for reference, used for calculation)
# Tau_nom = (16 * F * D_mean) / (pi * a * b^2)
# Tau_max = k * Tau_nom
# VonMises = sqrt(3) * Tau_max

tau_max_list = []
vM_list = []

for F in forces:
    tau_nom = (16 * F * D_mean) / (np.pi * a * b**2)
    tau_max = k * tau_nom
    vM = np.sqrt(3) * tau_max
    tau_max_list.append(tau_max)
    vM_list.append(vM)

plt.figure(figsize=(10, 6))
plt.plot(lifts, tau_max_list, 'r-', linewidth=2, label=r'Max Shear Stress $\tau_{max}$')
plt.plot(lifts, vM_list, 'b--', linewidth=2, label=r'Von Mises Stress $\sigma_{vM}$')

# Highlighting the max point (10mm)
plt.scatter([10], [tau_max_list[-1]], color='red')
plt.scatter([10], [vM_list[-1]], color='blue')
plt.annotate(f'{tau_max_list[-1]:.1f} MPa', (10, tau_max_list[-1]), textcoords="offset points", xytext=(-10,10), ha='center', color='red')
plt.annotate(f'{vM_list[-1]:.1f} MPa', (10, vM_list[-1]), textcoords="offset points", xytext=(-10,10), ha='center', color='blue')

plt.title('Stress Distribution over Valve Lift (Operating Range)', fontsize=14)
plt.xlabel('Valve Lift [mm]', fontsize=12)
plt.ylabel('Stress [MPa]', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)

# Save the plot
plt.savefig('stress_plot.png', dpi=300, bbox_inches='tight')
print("Stress plot saved as stress_plot.png")
