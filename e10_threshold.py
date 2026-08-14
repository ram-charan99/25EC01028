import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load MOSFET VGS sweep data
df = pd.read_csv("./MOSFET_ID_VGS.csv")

# Get VGS and ID
vgs = pd.to_numeric(df["V_GS (V)"], errors="coerce")
id_current = pd.to_numeric(df["I_D (mA)"], errors="coerce")

# Remove invalid values
data = pd.DataFrame({
    "VGS": vgs,
    "ID": id_current
}).dropna()

# Keep positive drain current values
data = data[data["ID"] > 0]

vgs = data["VGS"].to_numpy()
id_current = data["ID"].to_numpy()

# Calculate square root of drain current
sqrt_id = np.sqrt(id_current)

# Select the approximately linear region near the upper part
mask = sqrt_id >= 0.3 * sqrt_id.max()

vgs_fit = vgs[mask]
sqrt_id_fit = sqrt_id[mask]

# Linear fit: sqrt(ID) = m*VGS + c
m, c = np.polyfit(vgs_fit, sqrt_id_fit, 1)

# Threshold voltage = x-intercept
vt = -c / m

print(f"Threshold voltage V_T = {vt:.4f} V")

# Plot
plt.figure()
plt.plot(vgs, sqrt_id, "o", label="Data")
plt.plot(
    vgs_fit,
    m * vgs_fit + c,
    label="Linear fit"
)

plt.axhline(0, linewidth=1)
plt.axvline(vt, linestyle="--", label=f"V_T = {vt:.3f} V")

plt.xlabel("V_GS (V)")
plt.ylabel("sqrt(I_D) (sqrt(mA))")
plt.title("MOSFET Threshold Voltage Extraction")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("e10_threshold.png", dpi=300)
plt.show()