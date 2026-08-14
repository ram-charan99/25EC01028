import pandas as pd
import numpy as np

# Load MOSFET VGS sweep data
df = pd.read_csv("./MOSFET_ID_VGS.csv")

# Display column names
print("Columns:", list(df.columns))

# Convert required columns to numeric
vgs = pd.to_numeric(df["V_GS (V)"], errors="coerce")
id_current = pd.to_numeric(df["I_D (mA)"], errors="coerce")

# Remove invalid/header rows if any
data = pd.DataFrame({
    "VGS": vgs,
    "ID": id_current
}).dropna()

vgs = data["VGS"].to_numpy()
id_current = data["ID"].to_numpy()

# Calculate transconductance
gm = np.gradient(id_current, vgs)

# Find maximum transconductance
max_index = np.argmax(gm)

print(f"Highest VGS = {vgs.max():.1f} V")
print(f"Maximum gm = {gm[max_index]:.6f} mS")
print(f"1/gm = {1000 / gm[max_index]:.6f} kOhm")