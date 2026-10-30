
import re
import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize common formatting issues without deleting records."""
    cleaned = df.copy()

    # 1. Remove extra whitespace from text fields.
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: " ".join(value.split())
            if isinstance(value, str)
            else value
        )

    # 2. Normalize email addresses.
    if "Email" in cleaned.columns:
        cleaned["Email"] = cleaned["Email"].map(
            lambda value: value.lower()
            if isinstance(value, str)
            else value
        )

    # 3. Standardize names and cities.
    for column in ("Name", "City"):
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].map(
                lambda value: value.title()
                if isinstance(value, str)
                else value
            )

    # 4. Normalize common Indian phone number formats.
    if "Phone" in cleaned.columns:
        cleaned["Phone"] = cleaned["Phone"].map(_normalize_phone)

    # 5. Convert numeric-looking ages such as "028" to 28.
    if "Age" in cleaned.columns:
        cleaned["Age"] = cleaned["Age"].map(_normalize_age)

    # 6. Convert blank strings and whitespace-only values to missing values.
    cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)

    return cleaned


def _normalize_phone(value):
    if pd.isna(value):
        return value

    original = str(value).strip()
    digits = re.sub(r"\D", "", original)

    if len(digits) == 10:
        return digits

    if len(digits) == 11 and digits.startswith("0"):
        return digits[1:]

    if len(digits) == 12 and digits.startswith("91"):
        return digits[2:]

    # Preserve unexpected formats for the validator to flag.
    return original


def _normalize_age(value):
    if pd.isna(value):
        return value

    original = str(value).strip()

    if re.fullmatch(r"\d+", original):
        return int(original)

    # Leave invalid values such as "twenty" for validation.
    return original
