import pandas as pd
import matplotlib.pyplot as plt

# Load the MOSFET ID-VDS data
df = pd.read_csv("MOSFET_ID_VDS.csv")

# Rename columns
df.columns = ["VGS", "VDS", "ID"]

# Plot ID-VDS curves for different VGS values
plt.figure()

for vgs in sorted(df["VGS"].unique()):
    data = df[df["VGS"] == vgs]
    plt.plot(data["VDS"], data["ID"], marker="o", label=f"VGS = {vgs} V")

plt.xlabel("VDS (V)")
plt.ylabel("ID (mA)")
plt.title("MOSFET Output Characteristics")
plt.legend()
plt.grid(True)

plt.savefig("e7_output_characteristics.png", dpi=300, bbox_inches="tight")
plt.show()