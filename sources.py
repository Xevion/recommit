import abc
import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

import requests
from dateutil import parser
from decouple import config

from models import Commit


class CommitSource(abc.ABC):
    """A simple abstract class for representing different commit sources generally."""

    def __init__(self) -> None:
        self.session = requests.Session()

    @abc.abstractmethod
    def fetch(self, check_function: Callable) -> List[Commit]:
        """Fetch commits from the source."""
        pass

    @property
    @abc.abstractmethod
    def source_type(self) -> str:
        """Specifies the source type for storage in a database."""
        pass

    @property
    def name(self) -> str:
        """Returns the name of this class."""
        return type(self).__name__

    def getLogger(self, name: Optional[str] = None) -> logging.Logger:
        """Returns a new instance of a Logger"""
        logger = logging.getLogger(name or self.name.lower())
        logger.setLevel(logging.INFO)
        return logger


class Gitlab(CommitSource):
    """Serves as the commit source for GitLab."""

    USERNAME_CONSTANT: str = 'GITLAB_USERNAME'
    API_KEY_CONSTANT: str = 'GITLAB_API_KEY'

    def __init__(self) -> None:
        super().__init__()

        self.logger: logging.Logger = self.getLogger()
        self.__api_key: str = config(self.API_KEY_CONSTANT)
        self.__username: str = config(self.USERNAME_CONSTANT)

    def fetch(self, check_seen_function: Callable) -> List[Commit]:
        """Automatically fetch all commits from the database."""

        page: int = 1
        continue_fetching: bool = True
        results: List[Commit] = []

        self.logger.info('Beginning fetching process for GitLab source.')

        while continue_fetching:
            continue_fetching = False

            # Check all events in the list
            for event in self.events(page=page, per_page=50):
                if not check_seen_function(event['id']):
                    continue_fetching = True

                    results.append(Commit(
                            id=event['id'],
                            name='Private Contribution',
                            timestamp=parser.isoparse(event['created_at'])
                    ))

            page += 1

        return results

    def events(self, action: Optional[str] = None, target_type: Optional[str] = None, before: Optional[date] = None,
               after: Optional[date] = None, sort: Optional[str] = None, page: Optional[int] = None,
               per_page: Optional[int] = None) -> List[Any]:
        """Fetches events from GitLab's API given parameters"""

        params = {'action': action, 'target_type': target_type, 'sort': sort, 'page': page, 'per_page': per_page}
        if before: params['before'] = before.isoformat()
        if after: params['after'] = after.isoformat()

        params = {k: v for k, v in params.items() if v is not None}
        request = requests.Request('GET', self.url, params=params, headers=self.headers)
        prepped = self.session.prepare_request(request)
        response = self.session.send(prepped)

        return response.json()

    @property
    def source_type(self) -> str:
        """Provides the source type for this class in the database."""
        return 'gitlab'

    @property
    def url(self) -> str:
        """Returns the request URL from which events will be sourced."""
        return f"https://gitlab.com/api/v4/users/{self.__username}/events"

    @property
    def headers(self) -> Dict[str, str]:
        """Returns the required headers for authoring API requests."""
        return {
            'PRIVATE-TOKEN': self.__api_key
        }
