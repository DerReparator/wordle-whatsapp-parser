from dataclasses import dataclass
from datetime import date, time

@dataclass
class Message:
    '''Holds information about a parsed message'''
    datestamp: date
    timestamp: time
    player: str
    message: str
