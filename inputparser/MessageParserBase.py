'''Base class for all parsers that provide World message string snippets.
'''

from typing import Generator
from abc import ABC, abstractmethod

class MessageParserBase(ABC):

    @abstractmethod
    def retrieve_snippets(self) -> Generator[str, None, None]:
        pass
