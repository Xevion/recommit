import abc
from datetime import date, datetime
from pprint import pprint
from typing import Any, Callable, Dict, List, Optional

import requests
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
        return logging.getLogger(name or self.name.lower())


class Gitlab(CommitSource):
    """Serves as the commit source for GitLab."""

    USERNAME_CONSTANT: str = 'GITLAB_USERNAME'
    API_KEY_CONSTANT: str = 'GITLAB_API_KEY'

    def __init__(self) -> None:
        super().__init__()

        self.logger: logging.Logger = self.getLogger()
        self.__api_key: str = config(self.API_KEY_CONSTANT)
        self.__username: str = config(self.USERNAME_CONSTANT)

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

    def fetch(self, check_function: Callable) -> List[Commit]:
        self.events(page=3)

        return []

    def events(self, action: Optional[str] = None, target_type: Optional[str] = None, before: Optional[date] = None,
               after: Optional[date] = None, sort: Optional[str] = None, page: Optional[int] = None,
               per_page: Optional[int] = None) -> List[Any]:
        """Fetches events from GitLab's API given parameters"""

        params = {'action': action, 'target_type': target_type, 'sort': sort, 'page': page, 'per_page': per_page}
        if before: params['before'] = before.strftime('%Y-%m-%d')
        if after: params['after'] = after.strftime('%Y-%m-%d')

        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(self.url, params=params, headers=self.headers)

        pprint(params)

        pprint(response.json())

        return response.json()
