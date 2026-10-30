
from pathlib import Path
import csv

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if extension == ".csv":
        return _load_csv(path)

    return pd.read_excel(path)


def _load_csv(path: Path) -> pd.DataFrame:
    rows = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty.")

        expected_columns = len(headers)

        if expected_columns == 0:
            raise ValueError("CSV header contains no columns.")

        for row_number, row in enumerate(reader, start=2):
            extra_data = ""
            issue = ""

            # Recover a complete CSV record accidentally stored
            # inside a single field, but only when the column count
            # matches the header exactly.
            if len(row) == 1 and expected_columns > 1:
                try:
                    recovered = next(csv.reader([row[0]]))
                except csv.Error:
                    recovered = row

                if len(recovered) == expected_columns:
                    row = recovered
                    issue = "Recovered embedded CSV record"

            if len(row) < expected_columns:
                missing_count = expected_columns - len(row)
                row.extend([""] * missing_count)

                if not issue:
                    issue = f"Missing {missing_count} field(s)"

            elif len(row) > expected_columns:
                extra_fields = row[expected_columns:]
                extra_data = ", ".join(extra_fields)
                row = row[:expected_columns]

                issue = f"Extra {len(extra_fields)} field(s)"

            rows.append(row + [extra_data, issue])

    columns = headers + ["_extra_data", "_row_issue"]

    return pd.DataFrame(rows, columns=columns)
