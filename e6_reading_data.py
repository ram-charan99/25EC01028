import pandas as pd

df = pd.read_csv("MOSFET_ID_VDS.csv")

print("Columns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nDescription:")
print(df.describe())