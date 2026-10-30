
import pandas as pd
import pytest

from src.loader import load_file


def test_loads_valid_csv(tmp_path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "Name,Email\nRahul,rahul@gmail.com\n",
        encoding="utf-8",
    )

    result = load_file(str(file_path))

    assert list(result.columns) == [
        "Name", "Email", "_extra_data", "_row_issue"
    ]
    assert result.loc[0, "Name"] == "Rahul"
    assert result.loc[0, "Email"] == "rahul@gmail.com"


def test_missing_file_raises_error(tmp_path):
    file_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_file(str(file_path))


def test_unsupported_extension_raises_error(tmp_path):
    file_path = tmp_path / "customers.txt"
    file_path.write_text("sample", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_file(str(file_path))


def test_empty_csv_raises_error(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV file is empty"):
        load_file(str(file_path))


def test_missing_fields_are_padded(tmp_path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "Name,Email,Age\nRahul,rahul@gmail.com\n",
        encoding="utf-8",
    )

    result = load_file(str(file_path))

    assert result.loc[0, "Age"] == ""
    assert result.loc[0, "_row_issue"] == "Missing 1 field(s)"


def test_extra_fields_are_preserved(tmp_path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "Name,Email\nRahul,rahul@gmail.com,EXTRA\n",
        encoding="utf-8",
    )

    result = load_file(str(file_path))

    assert result.loc[0, "Name"] == "Rahul"
    assert result.loc[0, "Email"] == "rahul@gmail.com"
    assert result.loc[0, "_extra_data"] == "EXTRA"
    assert result.loc[0, "_row_issue"] == "Extra 1 field(s)"


def test_recovers_embedded_csv_record(tmp_path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "Name,Email,Phone,City,Age\n"
        '"Anjali Sharma,anjali@gmail.com,9876500013,Delhi,26"\n',
        encoding="utf-8",
    )

    result = load_file(str(file_path))

    assert result.loc[0, "Name"] == "Anjali Sharma"
    assert result.loc[0, "Email"] == "anjali@gmail.com"
    assert result.loc[0, "Phone"] == "9876500013"
    assert result.loc[0, "City"] == "Delhi"
    assert result.loc[0, "Age"] == "26"
    assert result.loc[0, "_row_issue"] == "Recovered embedded CSV record"
