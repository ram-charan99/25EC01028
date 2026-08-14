import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the MOSFET ID-VDS data
df = pd.read_csv("MOSFET_ID_VDS.csv", header=None)

# Give the columns names
df.columns = ["VGS", "VDS", "ID"]

# Convert columns to numeric values
df["VGS"] = pd.to_numeric(df["VGS"], errors="coerce")
df["VDS"] = pd.to_numeric(df["VDS"], errors="coerce")
df["ID"] = pd.to_numeric(df["ID"], errors="coerce")

# Remove any non-numeric/header rows
df = df.dropna()

# Plot output conductance
plt.figure()

for vgs in sorted(df["VGS"].unique()):
    data = df[df["VGS"] == vgs]

    vds = data["VDS"].to_numpy()
    id_current = data["ID"].to_numpy()

    # gd = dID/dVDS
    gd = np.gradient(id_current, vds)

    plt.plot(vds, gd, marker="o", label=f"VGS = {vgs} V")

plt.xlabel("VDS (V)")
plt.ylabel("gd (mS)")
plt.title("MOSFET Output Conductance")
plt.legend()
plt.grid(True)

plt.savefig("e8_output_conductance.png", dpi=300, bbox_inches="tight")
plt.show()

# Highest VGS
highest_vgs = df["VGS"].max()
data = df[df["VGS"] == highest_vgs]

vds = data["VDS"].to_numpy()
id_current = data["ID"].to_numpy()

gd = np.gradient(id_current, vds)

# Last point
gd_sat = gd[-1]

if gd_sat != 0:
    ro = 1 / gd_sat

    print(f"Highest VGS = {highest_vgs} V")
    print(f"gd in saturation = {gd_sat:.6f} mS")
    print(f"1/gd in saturation = {ro:.6f} kOhm")
else:
    print("gd is zero.")