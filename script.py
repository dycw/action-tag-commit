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
from subprocess import CalledProcessError, check_call, check_output

from click import command
from typed_settings import click_options, option, settings
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config
from utilities.version import parse_version

_LOGGER = getLogger(__name__)


@settings
class Settings:
    dry_run: bool = option(default=False, help="Dry run the CLI")


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@click_options(Settings, "app", show_envvars_in_help=True)
def main(settings: Settings, /) -> None:
    if settings.dry_run:
        _LOGGER.info("Dry run; exiting...")
        return
    cmds = ["bump-my-version", "show", "current_version"]
    _LOGGER.info("Running '%s'...", " ".join(cmds))
    version = parse_version(check_output(cmds, text=True).rstrip("\n"))
    _tag(str(version))
    _tag(f"{version.major}.{version.minor}")
    _tag(str(version.major))
    _tag("latest")
    _LOGGER.info("Finished")


def _tag(version: str, /) -> None:
    _delete_tag(version)
    _add_tag(version)


def _delete_tag(version: str, /) -> None:
    cmds1 = ["git", "tag", "--delete", version]
    _LOGGER.info("Running '%s'...", " ".join(cmds1))
    with suppress(CalledProcessError):
        _ = check_call(cmds1)
    cmds2 = ["git", "push", "--delete", "origin", version]
    _LOGGER.info("Running '%s'...", " ".join(cmds2))
    with suppress(CalledProcessError):
        _ = check_call(cmds2)


def _add_tag(version: str, /) -> None:
    cmds1 = ["git", "tag", "-a", version, "HEAD", "-m", version]
    _LOGGER.info("Running '%s'...", " ".join(cmds1))
    _ = check_call(cmds1)
    cmds2 = ["git", "push", "--tags", "--force", "--set-upstream", "origin"]
    _LOGGER.info("Running '%s'...", " ".join(cmds2))
    _ = check_call(cmds2)


if __name__ == "__main__":
    basic_config(obj=__name__)
    main()
