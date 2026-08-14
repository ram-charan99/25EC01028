import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# E12 - MOSFET ID-VDS Characteristics
# SPICE Level 1 and Level 3 style models
# ============================================================

# Physical constants
q = 1.602e-19
eps0 = 8.854e-14          # F/cm
eps_si = 11.7 * eps0
eps_ox = 3.9 * eps0
k = 1.381e-23
T = 300
kT_q = 8.617e-5 * T

# MOSFET parameters
tox = 10e-7               # 10 nm = 1e-6 cm
Na = 1e16                 # cm^-3
Qf_density = 1e12         # cm^-2
W = 4e-4                  # 4 um = 4e-4 cm
L = 0.18e-4               # 0.18 um = 1.8e-5 cm
mu_n = 400                # cm^2/Vs

# Material parameters
phi_m = 4.1               # Aluminium gate work function
chi_si = 4.05             # Silicon electron affinity
Eg = 1.12                 # eV
ni = 1e10                 # cm^-3

# ============================================================
# Calculate MOS parameters
# ============================================================

Cox = eps_ox / tox

phi_f = kT_q * np.log(Na / ni)

phi_s = chi_si + Eg / 2 + phi_f

phi_ms = phi_m - phi_s

Qf = q * Qf_density

Vfb = phi_ms - Qf / Cox

gamma = np.sqrt(2 * q * eps_si * Na) / Cox

Vt = Vfb + 2 * phi_f + gamma * np.sqrt(2 * phi_f)

# SPICE Level 1 transconductance parameter
KP = mu_n * Cox

print("E12 MOSFET Parameters")
print("----------------------")
print(f"Cox = {Cox:.4e} F/cm^2")
print(f"phi_F = {phi_f:.4f} V")
print(f"V_FB = {Vfb:.4f} V")
print(f"gamma = {gamma:.4f} V^0.5")
print(f"V_T = {Vt:.4f} V")
print(f"KP = {KP:.4e} A/V^2")
print()

# VDS range
vds = np.linspace(0, 4, 401)

# Gate voltages
vgs_values = [1, 2, 3]

# ============================================================
# SPICE LEVEL 1 MODEL
# ============================================================

def level1_current(vgs, vds):
    vov = vgs - Vt

    if vov <= 0:
        return 0.0

    beta = KP * W / L

    # Linear region
    if vds <= vov:
        return beta * (vov * vds - 0.5 * vds**2)

    # Saturation region
    return 0.5 * beta * vov**2


# ============================================================
# LEVEL 3 STYLE MODEL
# Includes:
#   - mobility degradation
#   - velocity saturation
#   - channel length modulation
# ============================================================

vsat = 1e7                 # cm/s
theta = 0.08               # mobility degradation parameter
lambda_3 = 0.02            # channel length modulation
kappa = 0.2                # velocity saturation effect


def level3_current(vgs, vds):
    vov = vgs - Vt

    if vov <= 0:
        return 0.0

    # Effective mobility reduction
    mu_eff = mu_n / (1 + theta * vov)

    beta = mu_eff * Cox * W / L

    # Velocity saturation voltage
    vdsat_velocity = (vsat * L) / mu_eff

    # Effective saturation voltage
    vdsat = min(vov, vdsat_velocity + kappa * vov)

    if vds <= vdsat:

        current = beta * (
            vov * vds
            - 0.5 * vds**2
        )

    else:

        current = 0.5 * beta * vdsat**2

        # Channel length modulation
        current *= (1 + lambda_3 * (vds - vdsat))

    return max(current, 0.0)


# ============================================================
# Generate curves
# ============================================================

level1_curves = {}
level3_curves = {}

for vgs in vgs_values:

    level1_curves[vgs] = np.array([
        level1_current(vgs, vd)
        for vd in vds
    ])

    level3_curves[vgs] = np.array([
        level3_current(vgs, vd)
        for vd in vds
    ])


# ============================================================
# Print maximum currents
# ============================================================

print("Maximum drain currents")
print("----------------------")

for vgs in vgs_values:

    id1 = level1_curves[vgs][-1]
    id3 = level3_curves[vgs][-1]

    print(
        f"VGS = {vgs} V : "
        f"Level 1 = {id1 * 1000:.3f} mA, "
        f"Level 3 = {id3 * 1000:.3f} mA"
    )


# ============================================================
# Plot SPICE Level 1
# ============================================================

plt.figure(figsize=(8, 6))

for vgs in vgs_values:
    plt.plot(
        vds,
        level1_curves[vgs] * 1000,
        label=f"VGS = {vgs} V"
    )

plt.xlabel("VDS (V)")
plt.ylabel("ID (mA)")
plt.title("MOSFET ID-VDS Characteristics - SPICE Level 1")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "e12_level1.png",
    dpi=350,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# Plot Level 3
# ============================================================

plt.figure(figsize=(8, 6))

for vgs in vgs_values:
    plt.plot(
        vds,
        level3_curves[vgs] * 1000,
        label=f"VGS = {vgs} V"
    )

plt.xlabel("VDS (V)")
plt.ylabel("ID (mA)")
plt.title("MOSFET ID-VDS Characteristics - Level 3")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "e12_level3.png",
    dpi=350,
    bbox_inches="tight"
)

plt.show()