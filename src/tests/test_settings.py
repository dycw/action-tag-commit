from __future__ import annotations

from typed_settings import EnvLoader, load_settings
from utilities.os import temp_environ

from tag_commit.settings import Settings


class TestSettings:
    def test_empty_strs(self) -> None:
        with temp_environ(TOKEN=""):
            settings = load_settings(Settings, [EnvLoader("")])
        assert settings.token is None
