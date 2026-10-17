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

        for row_number, row in enumerate(reader, start=2):
            issue = ""

            if len(row) < expected_columns:
                issue = (
                    f"Missing {expected_columns - len(row)} field(s)"
                )

                row = row + [""] * (expected_columns - len(row))

            elif len(row) > expected_columns:
                extra_fields = row[expected_columns:]

                issue = (
                    f"Extra {len(extra_fields)} field(s)"
                )

                row = row[:expected_columns] + [
                    ", ".join(extra_fields)
                ]

            else:
                row = row + [""]

            rows.append(row + [issue])

    columns = headers + ["_extra_data", "_row_issue"]

    return pd.DataFrame(rows, columns=columns)