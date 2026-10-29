"""Small dependency-free helpers for local dataset path configuration."""
import os
from pathlib import Path


def resolve_dataset_dir(cli_value: str | None = None) -> Path:
    """Resolve --data-dir, IMAGE_DATA_DIR, or the documented ./data/images default."""
    raw_path = cli_value or os.getenv("IMAGE_DATA_DIR") or "./data/images"
    return Path(raw_path).expanduser().resolve()
