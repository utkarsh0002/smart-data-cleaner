from loader import load_file


df = load_file("input/customers.csv")

print(df)
print()
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")