from pathlib import Path
from loader import load_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "input" / "customers.csv"

df = load_file(str(INPUT_FILE))

print(df)
print()

print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")