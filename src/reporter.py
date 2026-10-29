
import json
from pathlib import Path

import pandas as pd


def save_report(
    issues_df: pd.DataFrame,
    output_path: str | Path,
    original_rows: int,
    cleaned_rows: int,
) -> None:
    """Save a JSON summary of data-quality issues."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    issue_counts = (
        issues_df["issue_type"].value_counts().to_dict()
        if not issues_df.empty
        else {}
    )

    report = {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "rows_removed": original_rows - cleaned_rows,
        "total_issues": len(issues_df),
        "issues_by_type": issue_counts,
        "issues": issues_df.astype(object)
        .where(pd.notna(issues_df), None)
        .to_dict(orient="records"),
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False, default=str)


def save_cleaned_data(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save the cleaned dataset as an Excel workbook."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(output_path, index=False)
