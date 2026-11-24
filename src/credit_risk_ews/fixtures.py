import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class LoanMonth:
    loan_id: str
    reporting_month: str
    delinquency_status: int | None
    current_balance: float
    loan_status: str


def load_fixture(path: Path) -> list[LoanMonth]:
    """Read a CSV fixture and validate its basic structural contract."""
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        expected = {
            "loan_id",
            "reporting_month",
            "delinquency_status",
            "current_balance",
            "loan_status",
        }
        if set(reader.fieldnames or []) != expected:
            raise ValueError(f"Expected columns: {sorted(expected)}")
        records: list[LoanMonth] = []
        for row in reader:
            records.append(
                LoanMonth(
                    loan_id=row["loan_id"].strip(),
                    reporting_month=row["reporting_month"].strip(),
                    delinquency_status=(
                        int(row["delinquency_status"])
                        if row["delinquency_status"].strip()
                        else None
                    ),
                    current_balance=float(row["current_balance"]),
                    loan_status=row["loan_status"].strip(),
                )
            )
    validate_fixture(records)
    return records


def validate_fixture(records: list[LoanMonth]) -> None:
    """Check uniqueness, valid month/status and basic nonnegative balances."""
    unique_keys: set[tuple[str, str]] = set()
    for record in records:
        if not record.loan_id:
            raise ValueError("Empty loan_id")
        try:
            parsed = datetime.strptime(record.reporting_month, "%Y-%m")
        except ValueError as error:
            raise ValueError("Invalid reporting_month") from error
        if parsed.strftime("%Y-%m") != record.reporting_month:
            raise ValueError("Invalid reporting_month")
        if record.current_balance < 0:
            raise ValueError("Negative current_balance")
        if record.loan_status not in {"active", "prepaid"}:
            raise ValueError("Unknown loan_status")
        if record.loan_status == "active" and record.delinquency_status is None:
            raise ValueError("Active loan has missing delinquency_status")
        if record.delinquency_status is not None and record.delinquency_status < 0:
            raise ValueError("Invalid delinquency_status")
        key = (record.loan_id, record.reporting_month)
        if key in unique_keys:
            raise ValueError("Duplicated loan-month key")
        unique_keys.add(key)
