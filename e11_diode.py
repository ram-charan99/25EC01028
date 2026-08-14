import pandas as pd
import matplotlib.pyplot as plt

# Load diode data
df = pd.read_csv("Diode_IV_Temperature.csv")

# Display data information
print("Columns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nDescription:")
print(df.describe())

# Create the figure
plt.figure(figsize=(9, 6))

# Plot I-V curve for each temperature
for temperature, group in df.groupby("T (C)"):
    plt.plot(
        group["V (V)"],
        group["I (mA)"],
        marker="o",
        linewidth=1.5,
        label=f"{temperature} °C"
    )

# Fully labelled graph
plt.xlabel("Voltage, V (V)")
plt.ylabel("Current, I (mA)")
plt.title("Diode I–V Characteristics at Different Ambient Temperatures")

# Legend and grid
plt.legend(title="Ambient Temperature")
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Save PNG at 350 dpi
plt.savefig(
    "Diode_IV_Temperature.png",
    dpi=350,
    bbox_inches="tight"
)

# Display graph
plt.show()