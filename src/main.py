
from pathlib import Path

from loader import load_file
from cleaner import clean_dataframe
from validator import validate_dataframe

from reporter import save_report, save_cleaned_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "input" / "customers.csv"

df = load_file(str(INPUT_FILE))
cleaned_df = clean_dataframe(df)
issues_df = validate_dataframe(cleaned_df)

OUTPUT_DIR = PROJECT_ROOT / "output"

save_cleaned_data(
    cleaned_df,
    OUTPUT_DIR / "cleaned_customers.xlsx",
)

save_report(
    issues_df,
    OUTPUT_DIR / "cleaning_report.json",
    original_rows=len(df),
    cleaned_rows=len(cleaned_df),
)

print(f"\nCleaned file saved to: {OUTPUT_DIR / 'cleaned_customers.xlsx'}")
print(f"Report saved to: {OUTPUT_DIR / 'cleaning_report.json'}")

print("CLEANED DATA")
print(cleaned_df.head(10).to_string(index=False))

print("\nVALIDATION ISSUES")
if issues_df.empty:
    print("No issues found.")
else:
    print(issues_df.to_string(index=False))

print(f"\nOriginal rows: {len(df)}")
print(f"Cleaned rows: {len(cleaned_df)}")
print(f"Total issues found: {len(issues_df)}")
