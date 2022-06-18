"""
Manages all behavior related to reading and writing commits to the internal database.
"""

import logging
import sqlite3
from typing import Optional

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

    def check_exists(self, id: str) -> bool:
        """Returns true if the commit in question exists."""
        return False
