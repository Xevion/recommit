import logging
from logging.handlers import TimedRotatingFileHandler
from typing import List

from rich.logging import RichHandler

from database import Database
from models import Commit
from sources import CommitSource, Gitlab

logging.basicConfig(level=logging.WARNING, format='%(message)s', datefmt="[%X]", handlers=[
    RichHandler(),
    TimedRotatingFileHandler(filename='recommit-log', backupCount=25)
])

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sources = [Gitlab()]


def main() -> None:
    """The main method for this application. When executed, it will use all available sources and create commits to act as contributions."""
    logger.info('Starting recommit.')

    sources: List[CommitSource] = [Gitlab()]
    commits: List[Commit] = []
    db = Database()

    logger.debug(f'{len(sources)} sources available.')
    logger.info('Ready.')

    for source in sources:
        new_commits: List[Commit] = source.fetch(db.check_exists)
        commits.extend(new_commits)

        logger.debug(f'{len(new_commits)} new commits from {source.name.upper()}.')

    logger.info(f'{len(commits)} commits found.')

    # TODO: Fetch all commits from the available sources
    # TODO: Check that the commit has been written
    # TODO: Write commits into the git log
    # TODO: Push to GitHub

    logger.info('Shutting down.')


if __name__ == '__main__':
    main()
