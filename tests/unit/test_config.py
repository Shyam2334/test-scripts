"""Unit tests for configuration management."""
import os
import pytest
from app.config import Settings


def test_default_settings():
    """Test default settings values."""
    settings = Settings()
    assert settings.app_name == "Health Check Microservice"
    assert settings.app_version == "0.1.0"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_settings_from_env(monkeypatch):
    """Test settings from environment variables."""
    monkeypatch.setenv("APP_NAME", "Test App")
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("HOST", "localhost")
    monkeypatch.setenv("PORT", "9000")
    
    settings = Settings()
    assert settings.app_name == "Test App"
    assert settings.app_version == "2.0.0"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"
    assert settings.host == "localhost"
    assert settings.port == 9000