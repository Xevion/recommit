import difflib
import logging
import os.path
from logging.handlers import TimedRotatingFileHandler
from typing import List, Optional

import git
import pytz
from decouple import config

from database import Database
from models import Commit
from sources import CommitSource, Gitlab

CURRENT_DIR: str = os.path.dirname(os.path.abspath(__name__))
LOGS_DIR: str = os.path.join(CURRENT_DIR, 'logs')
if not os.path.exists(LOGS_DIR): os.makedirs(LOGS_DIR)

logging.basicConfig(level=logging.WARNING,
                    format='[%(asctime)s] [%(levelname)s] [%(threadName)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        TimedRotatingFileHandler(filename=os.path.join(LOGS_DIR, 'recommit.log'), backupCount=25)
                    ])

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sources = [Gitlab()]


def main() -> None:
    """The main method for this application. When executed, it will use all available sources and create commits to act as contributions."""
    logger.info('Starting recommit.')

    source_instances: List[CommitSource] = [Gitlab()]
    # source_instances.clear()
    commits: List[Commit] = []
    db = Database()

    logger.debug(f'{len(source_instances)} sources available.')
    logger.info('Ready.')

    for source in source_instances:
        new_commits: List[Commit] = source.fetch(db.check_exists)
        commits.extend(new_commits)

        logger.debug(f'{len(new_commits)} new commits from {source.name.upper()}.')

    logger.info(f'All done fetching. {len(commits)} commits found.')

    repository_path = config("REPOSITORY_PATH")
    repository_path = os.path.abspath(repository_path)
    if not os.path.exists(repository_path):
        logger.error('Unable to locate repository.')

    repo = git.Repo(repository_path)

    timezone_configuration: Optional[str] = None
    try:
        timezone_configuration = config('TIMEZONE', default=None)
        timezone = pytz.timezone(timezone_configuration or 'UTC')
    except pytz.UnknownTimeZoneError as e:
        logger.error('Failed to find the timezone specified.', exc_info=e)
        closest = difflib.get_close_matches(timezone_configuration, pytz.common_timezones, n=10, cutoff=0.15)
        logger.info('Did you mean any of these valid timezones? ' + str(closest))
        return

    logger.debug('Processing new commits...')

    successful: int = 0
    for commit in commits:
        commit_date_string = commit.timestamp.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S %z")

        try:
            logger.debug('Updating metafile with latest commit id.')
            meta_filepath = os.path.join(repository_path, 'meta')
            with open(meta_filepath, 'w') as meta_file:
                meta_file.write(str(commit.id))

            logger.debug('Constructing new Git commit.')
            repo.index.add(meta_filepath)
            repo_commit: git.Commit = repo.index.commit(str(commit.id), commit_date=commit_date_string, author_date=commit_date_string)

            logger.debug('Adding new commit to database.')
            db.add_commit(commit, commit_hash=repo_commit.hexsha)

            successful += 1
        except Exception as e:
            logger.error(f'Failed while inserting new commit ({commit.id}) into database.', commit, exc_info=e)
            continue

        logger.debug(f'Processed {commit.id} as {repo_commit.hexsha}')
        break

    logger.info(f'Finished processing commits ({successful}/{len(commits)}).')
    logger.info('Pushing to origin...')
    origin = repo.remote(name='origin')
    origin.push()
    logger.info('Done.')

    logger.info('Shutting down.')


if __name__ == '__main__':
    main()
