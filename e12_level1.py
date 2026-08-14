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

beta = mu_n * Cox * (W / L)

print("Cox =", Cox, "F/cm^2")
print("V_FB =", V_FB, "V")
print("Vth =", Vth, "V")
print("Beta =", beta, "A/V^2")

VDS = np.linspace(0, 4, 200)

VGS_values = [1, 2, 3]

plt.figure(figsize=(8, 6))

for VGS in VGS_values:

    Vov = VGS - Vth
    ID = np.zeros_like(VDS)

    if Vov > 0:

        linear = VDS <= Vov

        ID[linear] = beta * (
            Vov * VDS[linear]
            - (VDS[linear] ** 2) / 2
        )

        saturation = VDS > Vov

        ID[saturation] = (
            beta / 2
        ) * Vov ** 2

    ID_mA = ID * 1000

    plt.plot(
        VDS,
        ID_mA,
        label=f"V_GS = {VGS} V"
    )

plt.xlabel("V_DS (V)")
plt.ylabel("I_D (mA)")
plt.title("MOSFET I_D-V_DS Characteristics - SPICE Level 1")
plt.legend()
plt.grid(True)

plt.savefig("E12_SPICE_Level1.png", dpi=350)

plt.show()