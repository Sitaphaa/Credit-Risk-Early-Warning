from dataclasses import replace
from pathlib import Path

import pytest

from credit_risk_ews.config import read_project_config
from credit_risk_ews.fixtures import load_fixture, validate_fixture

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_configuration_is_readable() -> None:
    config = read_project_config(PROJECT_ROOT)
    assert config.horizon_months == 6
    assert config.severe_delinquency_status == 3
    assert config.review_capacity_fraction == 0.05
    assert config.synthetic_fixture.is_file()


def test_fixture_has_five_distinct_loans() -> None:
    config = read_project_config(PROJECT_ROOT)
    records = load_fixture(config.synthetic_fixture)
    assert len({r.loan_id for r in records}) == 5


def test_missing_month_is_not_fabricated() -> None:
    records = load_fixture(read_project_config(PROJECT_ROOT).synthetic_fixture)
    months = {r.reporting_month for r in records if r.loan_id == "L003"}
    assert "2025-02" not in months
    assert months == {"2025-01", "2025-03", "2025-04"}


def test_prepaid_loan_is_present() -> None:
    records = load_fixture(read_project_config(PROJECT_ROOT).synthetic_fixture)
    assert any(r.loan_status == "prepaid" for r in records)


def test_duplicate_loan_month_is_rejected() -> None:
    records = load_fixture(read_project_config(PROJECT_ROOT).synthetic_fixture)
    with pytest.raises(ValueError, match="Duplicated"):
        validate_fixture([*records, records[0]])


def test_negative_balance_is_rejected() -> None:
    records = load_fixture(read_project_config(PROJECT_ROOT).synthetic_fixture)
    with pytest.raises(ValueError, match="Negative"):
        validate_fixture([replace(records[0], current_balance=-10), *records[1:]])


def test_invalid_status_is_rejected() -> None:
    records = load_fixture(read_project_config(PROJECT_ROOT).synthetic_fixture)
    with pytest.raises(ValueError, match="Invalid delinquency"):
        validate_fixture([replace(records[0], delinquency_status=-1), *records[1:]])
