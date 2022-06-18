from dataclasses import dataclass
from datetime import datetime


@dataclass
class Commit:
    """Describes a specific commit event in time."""
    id: str
    project_id: int
    source: str
    iteration: int
    timestamp: datetime
    seen_timestamp: datetime

    def __str__(self) -> str:
        return '{name}({params})'.format(
                name=type(self).__name__,
                params=', '.join(f'{k}={v}' for k,v in self.__dict__.items())
        )
