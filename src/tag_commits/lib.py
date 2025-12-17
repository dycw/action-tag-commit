from __future__ import annotations

from contextlib import suppress
from logging import getLogger
from subprocess import CalledProcessError, check_output
from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.version import parse_version

from tag_commits.settings import SETTINGS

if TYPE_CHECKING:
    from utilities.version import Version


_LOGGER = getLogger(__name__)


def main(
    *,
    user_name: str = SETTINGS.user_name,
    user_email: str = SETTINGS.user_email,
    major_minor: bool = SETTINGS.major_minor,
    major: bool = SETTINGS.major,
    latest: bool = SETTINGS.latest,
) -> None:
    _ = _log_run("git", "config", "--global", "user.name", user_name)
    _ = _log_run("git", "config", "--global", "user.email", user_email)
    version = _get_version()
    _tag(str(version))
    if major_minor:
        _tag(f"{version.major}.{version.minor}")
    if major:
        _tag(str(version.major))
    if latest:
        _tag("latest")


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
