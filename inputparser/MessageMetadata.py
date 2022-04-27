from dataclasses import dataclass
from datetime import date, time
from enum import Enum, unique

@unique
class WorldeGameSource(Enum):
    '''An Enum representing the source (which game) from where the Wordle Metadata was parsed.'''
    UNKNOWN = "Unknown"
    WOERDL = "Wördl"
    WORDLE = "Wordle"

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return self.value


@dataclass
class Message:
    '''Holds information about a parsed message'''
    datestamp: date
    timestamp: time
    player: str
    message: str
