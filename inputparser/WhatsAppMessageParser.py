from typing import Generator
from typing import List
import os

from inputparser.MessageParserBase import MessageParserBase

class WhatsAppMessageParser(MessageParserBase):
    '''Parser for getting messages out of a WhatsApp Chat Backup TXT file.'''
    
    LENGTH_OF_PREAMBLE = 21
    '''The length of the "[<date>, <time>] " pre-amble of each new message.'''

    def __init__(self, filePath: str) -> None:
        super().__init__()
        if (os.path.isfile(filePath)):
            self.filePath = filePath
        else:
            raise FileNotFoundError(f'The WhatsApp .TXT file "{filePath}" was not valid.')

    def is_new_message(self, line: str) -> bool:
        '''Determine whether a line is the first line of a new message.'''
        return len(line) > self.LENGTH_OF_PREAMBLE\
        and line[0] == '['\
        and line[self.LENGTH_OF_PREAMBLE-2] == ']'

    def build_message(self, messageArr: List[str]) -> str:
        return ''.join(messageArr).strip()

    def retrieve_snippets(self) -> Generator[str, None, None]:
        if self.filePath is None:
            raise FileNotFoundError("Cannot retrieve snippets. File Path is None")
        
        with open(self.filePath, 'r', encoding="utf-8") as f:
            message: List[str] = []
            for line in f:
                if self.is_new_message(line):
                    if len(message) > 0:    # skip the yield if the first line starts
                        yield self.build_message(message)   # yield the old, finished message
                    message = [line[self.LENGTH_OF_PREAMBLE:]]
                else:
                    message.append(line)
            yield self.build_message(message)   # yield the last message at EOF
