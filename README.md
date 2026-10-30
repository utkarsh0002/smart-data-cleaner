# Smart Data Cleaner

A Python tool for cleaning, validating, and reporting issues in customer data from CSV and Excel files.

## Features

- Load customer data from CSV, XLSX, and XLS files.
- Normalize whitespace, names, email addresses, phone numbers, and numeric ages.
- Detect missing values and invalid email addresses, phone numbers, and ages.
- Identify potential duplicate records.
- Detect malformed CSV rows, including missing or extra fields.
- Export cleaned data to Excel.
- Generate a JSON report summarizing data quality issues.
- Run automated tests using pytest.

## Tech Stack

- Python
- Pandas
- OpenPyXL
- Pytest

## Project Structure

```text
smart-data-cleaner/
|-- input/
|   `-- customers.csv
|-- output/
|   |-- cleaned_customers.xlsx
|   `-- cleaning_report.json
|-- src/
|   |-- __init__.py
|   |-- cleaner.py
|   |-- loader.py
|   |-- main.py
|   |-- reporter.py
|   `-- validator.py
|-- tests/
|-- requirements.txt
`-- README.md
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/utkarsh0002/smart-data-cleaner.git
   cd smart-data-cleaner
   ```

2. Create and activate a virtual environment.

   **Windows PowerShell:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

Place your input file at `input/customers.csv`, then run:

```bash
python src/main.py
```

The program processes the data and generates:

- `output/cleaned_customers.xlsx` - cleaned customer data.
- `output/cleaning_report.json` - a report of detected data quality issues.

## Run Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The project currently includes 47 automated tests covering data loading, cleaning, validation, and reporting.

## Notes

- The input CSV is expected to contain the customer columns used by the application: `Name`, `Email`, `Phone`, `City`, and `Age`.
- Invalid records are flagged for review rather than automatically deleted.
- Duplicate records are reported as potential duplicates; they are not automatically removed.

## Author

Utkarsh Vats

GitHub: https://github.com/utkarsh0002