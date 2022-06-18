import logging
from logging.handlers import TimedRotatingFileHandler
from typing import List

from rich.logging import RichHandler

from database import Database
from models import Commit
from sources import Gitlab

logging.basicConfig(level=logging.WARNING, handlers=[
    RichHandler(),
    TimedRotatingFileHandler(filename='recommit-log', backupCount=25)
])

logger = logging.getLogger(__name__)
sources = [Gitlab()]


def main() -> None:
    """The main method for this application. When executed, it will use all available sources and create commits to act as contributions."""
    logger.info('Starting recommit.')

    commits: List[Commit] = []
    db = Database()

    # TODO: Fetch all commits from the available sources
    # TODO: Check that the commit has been written
    # TODO: Write commits into the git log
    # TODO: Push to GitHub

    logger.info('Shutting down.')


if __name__ == '__main__':
    main()
