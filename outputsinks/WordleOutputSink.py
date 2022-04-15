from abc import ABC, abstractmethod
from typing import List
from WordleStringParser import WordleMetadata

class WordleOutput(ABC):
    '''Base class for all users of parsed Wordle metadata.'''
    @abstractmethod
    def output_results(self, playedWordles: List[WordleMetadata]) -> None:
        pass