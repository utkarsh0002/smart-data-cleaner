
import pandas as pd
import pytest

from src.validator import validate_dataframe


def make_valid_record(**overrides):
    """Create a valid customer record for testing."""
    record = {
        "Name": "Rahul Sharma",
        "Email": "rahul@gmail.com",
        "Phone": "9876543210",
        "City": "Delhi",
        "Age": 21,
    }
    record.update(overrides)
    return record


def test_valid_record_has_no_issues():
    df = pd.DataFrame([make_valid_record()])

    issues = validate_dataframe(df)

    assert issues.empty


@pytest.mark.parametrize(
    "age",
    ["ten", -5, 149, 121, 150, 20.5],
)
def test_invalid_ages_are_flagged(age):
    df = pd.DataFrame([make_valid_record(Age=age)])

    issues = validate_dataframe(df)

    age_issues = issues[
        (issues["column"] == "Age")
        & (issues["issue_type"] == "invalid_age")
    ]

    assert len(age_issues) == 1


@pytest.mark.parametrize(
    "email",
    [
        "priya @gmail.com",
        "pooja@gmail",
        "ravi@@gmail.com",
        "nishagmail.com",
        "arjun@gmail",
    ],
)
def test_invalid_emails_are_flagged(email):
    df = pd.DataFrame([make_valid_record(Email=email)])

    issues = validate_dataframe(df)

    email_issues = issues[
        (issues["column"] == "Email")
        & (issues["issue_type"] == "invalid_email")
    ]

    assert len(email_issues) == 1


def test_missing_required_value_is_flagged():
    df = pd.DataFrame([
        make_valid_record(Name=pd.NA)
    ])

    issues = validate_dataframe(df)

    assert (
        (issues["column"] == "Name")
        & (issues["issue_type"] == "missing_value")
    ).any()


def test_invalid_phone_is_flagged():
    df = pd.DataFrame([
        make_valid_record(Phone="12345")
    ])

    issues = validate_dataframe(df)

    assert (
        (issues["column"] == "Phone")
        & (issues["issue_type"] == "invalid_phone")
    ).any()


def test_duplicate_records_are_flagged():
    record = make_valid_record()
    df = pd.DataFrame([record, record.copy()])

    issues = validate_dataframe(df)

    duplicates = issues[
        issues["issue_type"] == "duplicate_candidate"
    ]

    assert len(duplicates) == 2
    assert set(duplicates["record_number"]) == {1, 2}


def test_recovered_csv_record_is_not_malformed():
    df = pd.DataFrame([
        make_valid_record(
            _row_issue="Recovered embedded CSV record"
        )
    ])

    issues = validate_dataframe(df)

    assert not (issues["issue_type"] == "malformed_row").any()


@pytest.mark.parametrize(
    "row_issue, expected_message",
    [
        (
            "Extra 1 field(s)",
            "Review the extra fields.",
        ),
        (
            "Missing 1 field(s)",
            "Check the missing fields.",
        ),
    ],
)
def test_malformed_row_message(row_issue, expected_message):
    df = pd.DataFrame([
        make_valid_record(_row_issue=row_issue)
    ])

    issues = validate_dataframe(df)

    malformed = issues[
        issues["issue_type"] == "malformed_row"
    ]

    assert len(malformed) == 1
    assert expected_message in malformed.iloc[0]["message"]


def test_missing_required_column_raises_error():
    df = pd.DataFrame([
        {
            "Name": "Rahul Sharma",
            "Email": "rahul@gmail.com",
            "Phone": "9876543210",
            "City": "Delhi",
        }
    ])

    with pytest.raises(
        ValueError,
        match="Required column is missing: Age",
    ):
        validate_dataframe(df)
