from dataclasses import dataclass
from datetime import datetime


@dataclass
class Commit:
    """Describes a specific commit event in time."""

    # A unique identifier for this commit. Not necessarily the commit hash.
    id: int
    # A name, description etc. for this commit. Not required to be based on the original comit message.
    name: str
    # A timestamp
    timestamp: datetime
