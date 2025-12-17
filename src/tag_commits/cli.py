from __future__ import annotations

from click import command
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config

from tag_commits.lib import tag_commits
from tag_commits.logging import LOGGER
from tag_commits.settings import Settings


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@click_options(Settings, "app", show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    if settings.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    tag_commits(
        user_name=settings.user_name,
        user_email=settings.user_email,
        major_minor=settings.major_minor,
        major=settings.major,
        latest=settings.latest,
    )


if __name__ == "__main__":
    basic_config(obj=LOGGER)
    _main()
