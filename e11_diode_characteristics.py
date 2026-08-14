import pandas as pd
import matplotlib.pyplot as plt

# Load diode I-V temperature data
df = pd.read_csv("./Diode_IV_Temperature.csv")

# Display column names
print("Columns:", list(df.columns))

# Plot each temperature curve
plt.figure()

# The first column is voltage
voltage = df.iloc[:, 0]

# Remaining columns are currents at different temperatures
for column in df.columns[1:]:
    plt.plot(voltage, df[column], label=column)

plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.title("Diode I-V Characteristics at Different Temperatures")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save at 350 dpi
plt.savefig("e11_diode_characteristics.png", dpi=350)

plt.show()