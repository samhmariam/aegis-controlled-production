from pathlib import Path

import pytest
from pydantic import ValidationError

from aegis.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_load_with_defaults() -> None:
    settings = get_settings()

    assert settings.environment == "local"
    assert settings.app_version == "0.1.0"
    assert settings.synthetic_data_dir == Path("data/synthetic")


def test_invalid_synthetic_data_dir_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AEGIS_SYNTHETIC_DATA_DIR", "data/does-not-exist")

    with pytest.raises(ValidationError, match="synthetic_data_dir"):
        get_settings()


def test_unknown_aegis_env_var_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    sensitive_value = "synthetic-sensitive-value"
    monkeypatch.setenv("AEGIS_UNEXPECTED", sensitive_value)

    with pytest.raises(ValidationError, match="Extra inputs are not permitted") as exc_info:
        get_settings()

    assert "AEGIS_UNEXPECTED" in str(exc_info.value)
    assert sensitive_value not in str(exc_info.value)
