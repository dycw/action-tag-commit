from __future__ import annotations

from click import command
from rich.pretty import pretty_repr
from typed_settings import EnvLoader, click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config

from tag_commit import __version__
from tag_commit.lib import tag_commit
from tag_commit.logging import LOGGER
from tag_commit.settings import Settings


@command(**CONTEXT_SETTINGS)
@click_options(Settings, [EnvLoader("")], show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running version %s with settings:
%s""",
        __version__,
        pretty_repr(settings),
    )
    if settings.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    tag_commit(
        user_name=settings.user_name,
        user_email=settings.user_email,
        major_minor=settings.major_minor,
        major=settings.major,
        latest=settings.latest,
    )


if __name__ == "__main__":
    _main()
