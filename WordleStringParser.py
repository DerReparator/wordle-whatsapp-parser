'''
This module holds the parsing functionality for
parsing Wordle metadata from strings.
'''
from dataclasses import dataclass
from tokenize import group
from typing import Dict, Optional, Union
import re

PLAYER_UNKNOWN: str = "unknown"

REGEX_GROUP_DAYIDX = "dayIdx"
REGEX_GROUP_SOLLEN = "solutionLength"
REGEX_GROUP_SOL = "solution"

REGEX_WORDLE_MSG = re.compile(f'.*?Wordle (?P<{REGEX_GROUP_DAYIDX}>\d+) (?P<{REGEX_GROUP_SOLLEN}>[1-6X])/6\n+?(?P<{REGEX_GROUP_SOL}>(^[🟨⬜⬛🟩]{{5}}\n){{1,6}})', re.M | re.I | re.DOTALL)

@dataclass
class WordleMetadata:
    '''Holds information about the wordle metadata of one played day.'''
    day_index: int
    steps_to_solution: Union[int, str]
    player: str
    solution: str
    streak: Optional[int] = None

    def is_failed_attempt(self) -> bool:
        return self.steps_to_solution == 'X'

def parseMessage(msg: str, playerName:str = PLAYER_UNKNOWN) -> Optional[WordleMetadata]:
    day_index = None
    steps_to_solution = None
    solution = None

    match = REGEX_WORDLE_MSG.match(msg)

    if match is None:
        print("Aborting because no match was found.")
        return None

    matchedGroups: Dict[str, str] = match.groupdict()
    for groupName in matchedGroups:
        print("Found group:", groupName, matchedGroups[groupName])
        if REGEX_GROUP_DAYIDX == groupName:
            day_index = int(matchedGroups[REGEX_GROUP_DAYIDX])
        elif REGEX_GROUP_SOLLEN == groupName:
            try: # the steps were one of the digits 1 through 6
                steps_to_solution = int(matchedGroups[REGEX_GROUP_SOLLEN])
            except ValueError: # the steps were 'X' for an failed attempt
                steps_to_solution = matchedGroups[REGEX_GROUP_SOLLEN]
        elif REGEX_GROUP_SOL == groupName:
            solution = matchedGroups[REGEX_GROUP_SOL].strip()
    
    print("Day Idx:", day_index, "Steps to Solution:", steps_to_solution)
    # Check if ALL values are NOT None anymore
    if not any(map(lambda x: x is None, (day_index, steps_to_solution, solution))):
        return WordleMetadata(
            day_index=day_index,
            steps_to_solution=steps_to_solution,
            player=playerName,
            solution=solution,
        )
    else:
        return None