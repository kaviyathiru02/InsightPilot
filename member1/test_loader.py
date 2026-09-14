from data_loader import load_data

df = load_data("data/sample_sales.csv")

print(df.head())
print()
print("Shape:", df.shape)