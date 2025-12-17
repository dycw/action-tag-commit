from __future__ import annotations

from typed_settings import option, settings


@settings
class Settings:
    token: str = option(default="token", help="GitHub token")
    user_name: str = option(default="github-actions-bot", help="'git' user name")
    user_email: str = option(default="noreply@github.com", help="'git' user email")
    major_minor: bool = option(default=False, help="Add the 'major.minor' tag")
    major: bool = option(default=False, help="Add the 'major' tag")
    latest: bool = option(default=False, help="Add the 'latest' tag")
    dry_run: bool = option(default=False, help="Dry run the CLI")


SETTINGS = Settings()


__all__ = ["SETTINGS", "Settings"]
