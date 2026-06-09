import pandas as pd

df = pd.read_csv("DataCoSupplyChainDatasetRefined_First_5000.csv")

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

for col in df.columns:
    print(col)