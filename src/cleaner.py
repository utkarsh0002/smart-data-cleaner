import re

import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a customer DataFrame using safe, deterministic transformations.

    Invalid or ambiguous values are preserved so that validator.py
    can identify and report them later.
    """

    df = df.copy()

    df = clean_names(df)
    df = clean_emails(df)
    df = clean_phones(df)
    df = clean_cities(df)
    df = clean_ages(df)

    return df


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    if "Name" not in df.columns:
        return df

    df["Name"] = (
        df["Name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    return df


def clean_emails(df: pd.DataFrame) -> pd.DataFrame:
    if "Email" not in df.columns:
        return df

    df["Email"] = (
        df["Email"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "", regex=False)
    )

    return df


def clean_phones(df: pd.DataFrame) -> pd.DataFrame:
    if "Phone" not in df.columns:
        return df

    def normalize_phone(value):
        if pd.isna(value):
            return ""

        value = str(value).strip()

        if not value:
            return ""

        # Keep only digits.
        digits = re.sub(r"\D", "", value)

        # Convert common Indian formats to 10 digits.
        if digits.startswith("91") and len(digits) == 12:
            digits = digits[2:]

        if len(digits) == 11 and digits.startswith("0"):
            digits = digits[1:]

        if len(digits) == 10:
            return digits

        # Leave unusual values untouched for validator.py.
        return value

    df["Phone"] = df["Phone"].apply(normalize_phone)

    return df


def clean_cities(df: pd.DataFrame) -> pd.DataFrame:
    if "City" not in df.columns:
        return df

    df["City"] = (
        df["City"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    return df


def clean_ages(df: pd.DataFrame) -> pd.DataFrame:
    if "Age" not in df.columns:
        return df

    def normalize_age(value):
        if pd.isna(value):
            return ""

        value = str(value).strip()

        if not value:
            return ""

        # Only convert values that are actually numeric.
        if value.isdigit():
            return int(value)

        # Leave things like "twenty" untouched.
        return value

    df["Age"] = df["Age"].apply(normalize_age)

    return df