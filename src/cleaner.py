
import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean common formatting issues without deleting records."""
    cleaned = df.copy()

    # Clean whitespace in all text columns.
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: (
                " ".join(value.split())
                if isinstance(value, str)
                else value
            )
        )

    # Normalize email addresses.
    if "Email" in cleaned.columns:
        cleaned["Email"] = cleaned["Email"].map(
            lambda value: value.lower()
            if isinstance(value, str)
            else value
        )

    # Standardize names and city names.
    for column in ("Name", "City"):
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].map(
                lambda value: value.title()
                if isinstance(value, str)
                else value
            )

    # Treat empty or whitespace-only strings as missing values.
    cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)

    return cleaned
