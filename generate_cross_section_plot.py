import matplotlib.pyplot as plt
import numpy as np
import math

def generate_cross_section_stress():
    # Oval parameters (mm)
    b = 3.66  # height (vertical)
    a = 2.92  # width (radial)
    
    # Grid for the oval cross-section
    y = np.linspace(-b/2, b/2, 200)
    x = np.linspace(-a/2, a/2, 200)
    X, Y = np.meshgrid(x, y)
    
    # Mask for points inside the ellipse (x^2/(a/2)^2 + y^2/(b/2)^2 <= 1)
    mask = (X**2 / (a/2)**2 + Y**2 / (b/2)**2) <= 1
    
    # Parameters for stress at 10mm (F = 250N)
    F = 250.0
    D_mean = 14.92
    T = F * (D_mean / 2) # Torque
    
    # Nominal shear stress at the surface (approximate for ellipse)
    # tau = T * r / J
    # For an ellipse, max stress is at the ends of the minor axis? 
    # Actually for torsion of ellipse, max stress is at the ends of the minor axis (shortest radius from center to surface)
    # tau_max = 2 * T / (pi * (a/2) * (b/2)^2)
    tau_peak = 558.5 # From previous verified calculation (corrected)
    
    # Simplified stress distribution for torsion in elliptical cross section
    # tau(x, y) = proportional to distance from center, but scaled for ellipse
    # Real distribution: tau_zx = -2Ty / (pi * a * b^3 / 64 * (a^2+b^2)) ... complicated.
    # We'll use a representative gradient where stress is 0 at center and max at boundary
    # Stress concentration factor k is higher on the inner radius (let's say left side is inner)
    
    # Distance normalized to boundary
    R_norm = np.sqrt(X**2 / (a/2)**2 + Y**2 / (b/2)**2)
    
    # Linear gradient for visualization
    Tau = tau_peak * R_norm
    
    # Apply curvature effect (Wahl-like factor across the width)
    # Inner radius of coil is to the left (negative X)
    # Stress is higher on the inside
    k_curvature = 1.0 + 0.15 * (-X / (a/2)) # 1.15 at X = -a/2, 0.85 at X = a/2
    Tau = Tau * k_curvature
    
    # Mask outside points
    Tau[~mask] = np.nan
    vM = Tau * math.sqrt(3)
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Shear Stress
    im1 = ax1.imshow(Tau, extent=[-a/2, a/2, -b/2, b/2], origin='lower', cmap='jet')
    ax1.set_title(r'Shear Stress Distribution $\tau$ [MPa]')
    ax1.set_xlabel('Width (radial) [mm]')
    ax1.set_ylabel('Height (vertical) [mm]')
    plt.colorbar(im1, ax=ax1, label='MPa')
    
    # Von Mises Stress
    im2 = ax2.imshow(vM, extent=[-a/2, a/2, -b/2, b/2], origin='lower', cmap='magma')
    ax2.set_title(r'Von Mises Stress Distribution $\sigma_{vM}$ [MPa]')
    ax2.set_xlabel('Width (radial) [mm]')
    ax2.set_ylabel('Height (vertical) [mm]')
    plt.colorbar(im2, ax=ax2, label='MPa')
    
    plt.tight_layout()
    plt.savefig('stress_cross_section.png', dpi=150)
    print("Cross-section stress plot saved: stress_cross_section.png")

if __name__ == "__main__":
    generate_cross_section_stress()
