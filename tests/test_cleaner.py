import pandas as pd
import pytest

from src.cleaner import clean_dataframe


def test_normalizes_age_values(input_age, expected_age):
    df = pd.DataFrame({"Age": [input_age]})

    result = clean_dataframe(df)

    assert result.loc[0, "Age"] == expected_age



def test_removes_extra_whitespace():
    df = pd.DataFrame({"Name": ["  Rahul   Sharma  "]})

    result = clean_dataframe(df)

    assert result.loc[0, "Name"] == "Rahul Sharma"


def test_normalizes_email():
    df = pd.DataFrame({"Email": ["RAHUL@GMAIL.COM"]})

    result = clean_dataframe(df)

    assert result.loc[0, "Email"] == "rahul@gmail.com"


def test_standardizes_name_and_city():
    df = pd.DataFrame({
        "Name": ["rahul sharma"],
        "City": ["new delhi"],
    })

    result = clean_dataframe(df)

    assert result.loc[0, "Name"] == "Rahul Sharma"
    assert result.loc[0, "City"] == "New Delhi"


def test_normalizes_indian_phone_formats():
    df = pd.DataFrame({
        "Phone": [
            "98765 43210",
            "+91-9876543210",
            "09876543210",
            "98765-43210",
        ]
    })

    result = clean_dataframe(df)

    assert result["Phone"].tolist() == [
        "9876543210",
        "9876543210",
        "9876543210",
        "9876543210",
    ]


def test_normalizes_numeric_age():
    df = pd.DataFrame({"Age": ["028", "21"]})

    result = clean_dataframe(df)

    assert result["Age"].tolist() == [28, 21]



def test_preserves_invalid_age():
    df = pd.DataFrame({"Age": ["twenty", "-5", "150"]})

    result = clean_dataframe(df)

    assert result.loc[0, "Age"] == "twenty"
    assert result.loc[1, "Age"] == "-5"
    assert result.loc[2, "Age"] == 150



def test_converts_blank_strings_to_missing_values():
    df = pd.DataFrame({
        "Name": ["   "],
        "Email": [""],
    })

    result = clean_dataframe(df)

    assert pd.isna(result.loc[0, "Name"])
    assert pd.isna(result.loc[0, "Email"])


def test_does_not_modify_original_dataframe():
    df = pd.DataFrame({"Name": ["  rahul sharma  "]})
    original = df.copy(deep=True)

    clean_dataframe(df)

    pd.testing.assert_frame_equal(df, original)

@pytest.mark.parametrize(
    "input_age, expected_age",
    [
        ("028", 28),
        ("ten", "ten"),
        ("twenty", "twenty"),
        ("-5", "-5"),
        ("149", 149),
        ("150", 150),
        ("45", 45),
        ("0", 0),
        ("120", 120),
        ("121", 121),
    ],
)
def test_normalizes_age_values(input_age, expected_age):
    df = pd.DataFrame({"Age": [input_age]})
    result = clean_dataframe(df)

    assert result.loc[0, "Age"] == expected_age