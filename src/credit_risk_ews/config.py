import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    horizon_months: int
    severe_delinquency_status: int
    review_capacity_fraction: float
    synthetic_fixture: Path


def read_project_config(project_root: Path) -> ProjectConfig:
    """Load and validate local configuration using relative paths."""
    root = Path(project_root).resolve()
    config_file = root / "configs" / "project.toml"

    with config_file.open("rb") as stream:
        data = tomllib.load(stream)

    scoring = data["scoring"]

    settings = ProjectConfig(
        horizon_months=int(scoring["horizon_months"]),
        severe_delinquency_status=int(scoring["severe_delinquency_status"]),
        review_capacity_fraction=float(scoring["review_capacity_fraction"]),
        synthetic_fixture=(root / data["paths"]["synthetic_fixture"]).resolve(),
    )

    if settings.horizon_months <= 0:
        raise ValueError("horizon_months must be positive")

    if not 0 < settings.review_capacity_fraction <= 1:
        raise ValueError("review_capacity_fraction must be in (0, 1]")

    if settings.severe_delinquency_status < 1:
        raise ValueError("severe_delinquency_status must be >= 1")
    return settings
