
import re

import pandas as pd


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a report of data-quality issues without deleting rows."""

    issues = []

    def add_issue(record_number, column, issue_type, value, message):
        issues.append({
            "record_number": record_number,
            "column": column,
            "issue_type": issue_type,
            "value": value,
            "message": message,
        })

    required_columns = ["Name", "Email", "Phone", "City", "Age"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Required column is missing: {column}")

    for index, row in df.iterrows():
        record_number = index + 1

        # Report malformed CSV records.

        row_issue = row.get("_row_issue")
        extra_data = row.get("_extra_data")


        if (
            pd.notna(row_issue)
            and str(row_issue).strip()
            and row_issue != "Recovered embedded CSV record"
        ):
            issue_text = str(row_issue).strip()

            if issue_text.startswith("Extra"):
                message = (
                    f"CSV record contains {issue_text.lower()}. "
                    "Review the extra fields."
                )
            elif issue_text.startswith("Missing"):
                message = (
                    f"CSV record has {issue_text.lower()}. "
                    "Check the missing fields."
                )
            else:
                message = "CSV record has an incorrect number of fields."

            add_issue(
                record_number,
                "_row_issue",
                "malformed_row",
                row_issue,
                message,
            )


        # Check required fields.
        for column in required_columns:
            value = row[column]

            if pd.isna(value) or not str(value).strip():
                add_issue(
                    record_number, column, "missing_value",
                    value, f"{column} is missing."
                )

        # Validate email format.
        email = row["Email"]

        if pd.notna(email) and str(email).strip():
            email = str(email).strip()

            if not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+", email
            ):
                add_issue(
                    record_number, "Email", "invalid_email",
                    email, "Email format appears invalid."
                )

        # Validate Indian phone numbers: 10 digits, optionally prefixed by 91.
        phone = row["Phone"]

        if pd.notna(phone) and str(phone).strip():
            digits = re.sub(r"\D", "", str(phone))

            valid_phone = (
                len(digits) == 10
                or (len(digits) == 12 and digits.startswith("91"))
            )

            if not valid_phone:
                add_issue(
                    record_number, "Phone", "invalid_phone",
                    phone, "Expected 10 digits or 91 followed by 10 digits."
                )

        # Validate age.
        age = row["Age"]

        if pd.notna(age) and str(age).strip():
            try:
                numeric_age = float(age)

                if not numeric_age.is_integer() or not 0 <= numeric_age <= 120:
                    raise ValueError

            except (ValueError, TypeError):
                add_issue(
                    record_number, "Age", "invalid_age",
                    age, "Age must be a whole number between 0 and 120."
                )

    # Flag exact duplicate customer details after basic normalization.
    normalized = df.copy()

    for column in ("Name", "Email", "Phone", "City"):
        normalized[column] = normalized[column].map(
            lambda value: (
                str(value).strip().casefold()
                if pd.notna(value)
                else ""
            )
        )

    duplicate_mask = normalized.duplicated(
        subset=["Name", "Email", "Phone", "City", "Age"],
        keep=False,
    )

    for index in df.index[duplicate_mask]:
        add_issue(
            index + 1, "record", "duplicate_candidate",
            None, "Record matches another record after basic normalization."
        )

    return pd.DataFrame(
        issues,
        columns=[
            "record_number",
            "column",
            "issue_type",
            "value",
            "message",
        ],
    )
