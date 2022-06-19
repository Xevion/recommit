"""
Manages all behavior related to reading and writing commits to the internal database.
"""

import logging
import sqlite3
from typing import Optional

from models import Commit

logger = logging.getLogger(__name__)


class Database:
    """
    Operates and handles reading/writing to the local commit database.
    """

    def __init__(self) -> None:
        logger.debug('Initializing...')
        self.__is_closed: bool = True  # Becomes false after this statement.
        self.conn: Optional[sqlite3.Connection] = None
        self.open()
        self.construct()

    def construct(self) -> None:
        """Automatically initializes the database with the required table(s)."""

        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS commits (
                            Id text primary key not null,
                            Source text not null,
                            CommitHash text not null,
                            CommitTimestamp text not null,
                            SeenTimestamp text not null,
                            Iteration integer not null,
                            ProjectId integer not null);""")

        self.conn.commit()

    def open(self) -> None:
        """Opens a connection to the database file."""
        if self.__is_closed:
            logger.debug('Opening new database connection.')
            self.conn = sqlite3.connect('commits.db')
            self.__is_closed = False

    def close(self) -> None:
        """Closes the currently active database connection."""
        if self.__is_closed:
            logger.warning('Attempted to close while database connection is already closed...')
        else:
            logger.debug('Closing database connection.')
            self.conn.close()
            self.conn = None
            self.__is_closed = True

    def add_commit(self, commit: Commit, commit_hash: str) -> None:
        """Inserts a commit into the database"""

        cur = self.conn.cursor()
        cur.execute("""INSERT INTO commits (Id, Source, ProjectId, CommitHash, Iteration, CommitTimestamp, SeenTimestamp) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (commit.id, commit.source, commit.project_id, commit_hash, commit.iteration,
                     commit.timestamp.isoformat(), commit.seen_timestamp.isoformat()))
        self.conn.commit()

    def check_exists(self, id: str, source: Optional[str] = None) -> bool:
        """Returns true if the commit in question exists."""

        cur = self.conn.cursor()

        if source is None:
            results = list(cur.execute("""SELECT Id FROM commits WHERE Id = ? LIMIT 1;""", (id,)))
        else:
            results = list(cur.execute("""SELECT Id FROM commits WHERE Id = ? AND Source = ?""", (id, source)))
        if len(results) == 1: return True
        return False
