'''
This module holds the parsing functionality for
parsing Wordle metadata from strings.
'''
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import re

from inputparser.MessageMetadata import Message, WorldeGameSource
from inputparser.MessageParserBase import MessageParserBase

PLAYER_UNKNOWN: str = "unknown"

REGEX_GROUP_DAYIDX = "dayIdx"
REGEX_GROUP_SOLLEN = "solutionLength"
REGEX_GROUP_SOL = "solution"
REGEX_GROUP_STREAK = "streak"

REGEX_WORDLE_MSG = re.compile(f'.*?Wordle (?P<{REGEX_GROUP_DAYIDX}>\d+) (?P<{REGEX_GROUP_SOLLEN}>[1-6X])/6\n+?(?P<{REGEX_GROUP_SOL}>(^[🟨⬜⬛🟩]{{5}}\n){{1,6}})', re.M | re.I | re.DOTALL)
REGEX_WOERDL_MSG = re.compile(f'.*?Wördl (?P<{REGEX_GROUP_DAYIDX}>\d+) (?P<{REGEX_GROUP_SOLLEN}>[1-6X])/6 🔥(?P<{REGEX_GROUP_STREAK}>\d+)\n+?(?P<{REGEX_GROUP_SOL}>(^[🟨⬜⬛🟩]{{5}}\n){{1,6}})', re.M | re.I | re.DOTALL)

@dataclass
class WordleMetadata:
    '''Holds information about the wordle metadata of one played day.'''
    day_index: int
    steps_to_solution: Union[int, str]
    player: str
    solution: str
    streak: Optional[int] = None
    wordleGame: WorldeGameSource = WorldeGameSource.UNKNOWN


    def is_failed_attempt(self) -> bool:
        return self.steps_to_solution == 'X'

def parseFromSource(source: MessageParserBase) -> List[Optional[WordleMetadata]]:
    ret: List[WordleMetadata] = []
    for msg in source.retrieve_snippets():
        if msg is None:
            continue
        wordle = parseMessage(msg.message, msg.player)
        if wordle is not None:
            ret.append(wordle)
    return ret

def parseMessage(msg: str, playerName:str = PLAYER_UNKNOWN) -> Optional[WordleMetadata]:
    if not (parsedWordle := parseWordle(msg, playerName)) is None:
        return parsedWordle
    if not (parsedWoerdl := parseWoerdl(msg, playerName)) is None:
        return parsedWoerdl
    return None

def parseWordle(msg: str, playerName:str = PLAYER_UNKNOWN) -> Optional[WordleMetadata]:
    '''Parse for a "Wordle" (english) result.'''
    day_index = None
    steps_to_solution = None
    solution = None

    match = REGEX_WORDLE_MSG.match(msg)

    if match is None:
        return None

    matchedGroups: Dict[str, str] = match.groupdict()
    for groupName in matchedGroups:
        if REGEX_GROUP_DAYIDX == groupName:
            day_index = int(matchedGroups[REGEX_GROUP_DAYIDX])
        elif REGEX_GROUP_SOLLEN == groupName:
            try: # the steps were one of the digits 1 through 6
                steps_to_solution = int(matchedGroups[REGEX_GROUP_SOLLEN])
            except ValueError: # the steps were 'X' for an failed attempt
                steps_to_solution = matchedGroups[REGEX_GROUP_SOLLEN]
        elif REGEX_GROUP_SOL == groupName:
            solution = matchedGroups[REGEX_GROUP_SOL].strip()
    
    # Check if ALL values are NOT None anymore
    if not any(map(lambda x: x is None, (day_index, steps_to_solution, solution))):
        parsedWordle: WordleMetadata = WordleMetadata(
            day_index=day_index,
            steps_to_solution=steps_to_solution,
            player=playerName,
            solution=solution,
        )
        parsedWordle.wordleGame = WorldeGameSource.WORDLE
        return parsedWordle
    else:
        return None

def parseWoerdl(msg: str, playerName:str = PLAYER_UNKNOWN) -> Optional[WordleMetadata]:
    '''Parse for a "Woerdl" (german) result.'''
    day_index = None
    steps_to_solution = None
    solution = None
    streak = None

    match = REGEX_WOERDL_MSG.match(msg)

    if match is None:
        return None

    matchedGroups: Dict[str, str] = match.groupdict()
    for groupName in matchedGroups:
        if REGEX_GROUP_DAYIDX == groupName:
            day_index = int(matchedGroups[REGEX_GROUP_DAYIDX])
        elif REGEX_GROUP_SOLLEN == groupName:
            try: # the steps were one of the digits 1 through 6
                steps_to_solution = int(matchedGroups[REGEX_GROUP_SOLLEN])
            except ValueError: # the steps were 'X' for an failed attempt
                steps_to_solution = matchedGroups[REGEX_GROUP_SOLLEN]
        elif REGEX_GROUP_SOL == groupName:
            solution = matchedGroups[REGEX_GROUP_SOL].strip()
        elif REGEX_GROUP_STREAK == groupName:
            streak = int(matchedGroups[REGEX_GROUP_STREAK])
    
    # Check if ALL values are NOT None anymore
    if not any(map(lambda x: x is None, (day_index, steps_to_solution, solution, streak))):
        parsedWordle: WordleMetadata =  WordleMetadata(
            day_index=day_index,
            steps_to_solution=steps_to_solution,
            player=playerName,
            solution=solution,
            streak=streak
        )
        parsedWordle.wordleGame = WorldeGameSource.WOERDL
        return parsedWordle
    else:
        return None