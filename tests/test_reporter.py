
import json

import pandas as pd

from src.reporter import save_cleaned_data, save_report


def test_saves_cleaned_data_to_excel(tmp_path):
    df = pd.DataFrame({
        "Name": ["Rahul Sharma"],
        "Age": [21],
    })
    output_path = tmp_path / "nested" / "cleaned.xlsx"

    save_cleaned_data(df, output_path)

    assert output_path.exists()

    saved_df = pd.read_excel(output_path)

    pd.testing.assert_frame_equal(saved_df, df)


def test_saves_json_report_with_issue_counts(tmp_path):
    issues = pd.DataFrame([
        {
            "record_number": 1,
            "column": "Email",
            "issue_type": "invalid_email",
            "value": "bad-email",
            "message": "Email format appears invalid.",
        },
        {
            "record_number": 2,
            "column": "Age",
            "issue_type": "invalid_age",
            "value": "150",
            "message": "Age must be a whole number between 0 and 120.",
        },
    ])

    output_path = tmp_path / "nested" / "report.json"

    save_report(
        issues,
        output_path,
        original_rows=10,
        cleaned_rows=10,
    )

    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["original_rows"] == 10
    assert report["cleaned_rows"] == 10
    assert report["rows_removed"] == 0
    assert report["total_issues"] == 2
    assert report["issues_by_type"] == {
        "invalid_email": 1,
        "invalid_age": 1,
    }
    assert len(report["issues"]) == 2


def test_saves_empty_issue_report(tmp_path):
    issues = pd.DataFrame(
        columns=[
            "record_number",
            "column",
            "issue_type",
            "value",
            "message",
        ]
    )

    output_path = tmp_path / "empty_report.json"

    save_report(
        issues,
        output_path,
        original_rows=5,
        cleaned_rows=5,
    )

    with output_path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_issues"] == 0
    assert report["issues_by_type"] == {}
    assert report["issues"] == []
