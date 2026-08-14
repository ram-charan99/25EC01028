import numpy as np
import matplotlib.pyplot as plt

q = 1.602e-19
eps0 = 8.854e-14
eps_si = 11.7 * eps0
eps_ox = 3.9 * eps0

tox = 10e-7
NA = 1e16
QF = 1e12
W = 4e-4
L = 0.18e-4
mu_n = 400

Vt_thermal = 0.02585
ni = 1e10

Cox = eps_ox / tox

phi_F = Vt_thermal * np.log(NA / ni)

chi_si = 4.05
Eg = 1.12
phi_m = 4.1

phi_s = chi_si + Eg / 2 + phi_F
phi_ms = phi_m - phi_s

QF_C = q * QF

V_FB = phi_ms - QF_C / Cox

gamma = np.sqrt(2 * q * eps_si * NA) / Cox

Vth = V_FB + 2 * phi_F + gamma * np.sqrt(2 * phi_F)

KP = mu_n * Cox

theta = 0.1
lambda_ = 0.02

VDS = np.linspace(0, 4, 200)

VGS_values = [1, 2, 3]

plt.figure(figsize=(8, 6))

for VGS in VGS_values:

    Vov = VGS - Vth
    ID = np.zeros_like(VDS)

    if Vov > 0:

        Veff = Vov / (1 + theta * Vov)

        VDS_sat = Veff

        linear = VDS <= VDS_sat

        ID[linear] = (
            KP * (W / L)
            * (Veff * VDS[linear] - VDS[linear] ** 2 / 2)
        )

        saturation = VDS > VDS_sat

        ID_sat = (
            KP * (W / L)
            * Veff ** 2 / 2
        )

        ID[saturation] = (
            ID_sat
            * (1 + lambda_ * (VDS[saturation] - VDS_sat))
        )

    ID_mA = ID * 1000

    plt.plot(
        VDS,
        ID_mA,
        label=f"V_GS = {VGS} V"
    )

plt.xlabel("V_DS (V)")
plt.ylabel("I_D (mA)")
plt.title("MOSFET I_D-V_DS Characteristics - SPICE Level 3")
plt.legend()
plt.grid(True)

plt.savefig("E12B.png", dpi=350)

plt.show()