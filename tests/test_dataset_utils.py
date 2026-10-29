import os
from pathlib import Path

from app.scripts.dataset_utils import resolve_dataset_dir


def test_cli_path_takes_precedence_over_environment(monkeypatch, tmp_path):
    env_path = tmp_path / "from-env"
    cli_path = tmp_path / "from-cli"
    monkeypatch.setenv("IMAGE_DATA_DIR", str(env_path))

    assert resolve_dataset_dir(str(cli_path)) == cli_path.resolve()


def test_environment_path_is_used_when_cli_path_is_absent(monkeypatch, tmp_path):
    data_path = tmp_path / "images"
    monkeypatch.setenv("IMAGE_DATA_DIR", str(data_path))

    assert resolve_dataset_dir() == data_path.resolve()


def test_default_path_is_data_images_when_not_configured(monkeypatch):
    monkeypatch.delenv("IMAGE_DATA_DIR", raising=False)

    assert resolve_dataset_dir() == Path("./data/images").resolve()
