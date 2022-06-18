import abc
from typing import Callable, List

from decouple import config

from models import Commit


class CommitSource(abc.ABC):
    """A simple abstract class for representing different commit sources generally."""

    @abc.abstractmethod
    def fetch(self, check_function: Callable) -> List[Commit]:
        """Fetch commits from the source."""
        pass


class Gitlab(CommitSource):
    """Serves as the commit source for GitLab."""

    API_KEY_CONSTANT: str = 'GITLAB_API_KEY'

    def __init__(self) -> None:
        self.__api_key: str = config(self.API_KEY_CONSTANT)

    def fetch(self, check_function: Callable) -> List[Commit]:
        pass
