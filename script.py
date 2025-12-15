#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "click",
#   "dycw-utilities",
#   "pytest-xdist",
#   "typed-settings[attrs, click]",
# ]
# ///
from __future__ import annotations

from contextlib import suppress
from logging import getLogger
from subprocess import CalledProcessError, check_output
from typing import TYPE_CHECKING

from click import command
from typed_settings import click_options, option, settings
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config
from utilities.version import parse_version

if TYPE_CHECKING:
    from utilities.version import Version

_LOGGER = getLogger(__name__)


@settings
class Settings:
    user_name: str = "github-actions-bot"
    user_email: str = "noreply@github.com"
    dry_run: bool = option(default=False, help="Dry run the CLI")


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@click_options(Settings, "app", show_envvars_in_help=True)
def main(settings: Settings, /) -> None:
    if settings.dry_run:
        _LOGGER.info("Dry run; exiting...")
        return
    _config(settings.user_name, settings.user_email)
    version = _get_version()
    _tag(str(version))
    _tag(f"{version.major}.{version.minor}")
    _tag(str(version.major))
    _tag("latest")
    _LOGGER.info("Finished")


def _config(name: str, email: str, /) -> None:
    _ = _log_run("git", "config", "--global", "user.name", name)
    _ = _log_run("git", "config", "--global", "user.email", email)


def _get_version() -> Version:
    return parse_version(_log_run("bump-my-version", "show", "current_version"))


def _tag(version: str, /) -> None:
    _delete_tag(version)
    _add_tag(version)


def _delete_tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        _ = _log_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        _ = _log_run("git", "push", "--delete", "origin", version)


def _add_tag(version: str, /) -> None:
    _ = _log_run("git", "tag", "-a", version, "HEAD", "-m", version)
    _ = _log_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


def _log_run(*cmds: str) -> str:
    _LOGGER.info("Running '%s'...", " ".join(cmds))
    return check_output(cmds, text=True)


if __name__ == "__main__":
    basic_config(obj=__name__)
    main()
