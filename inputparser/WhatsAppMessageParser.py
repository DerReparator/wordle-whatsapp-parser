from tokenize import group
from typing import Dict, Generator
from typing import List
import os, re

from datetime import datetime, date, time

from inputparser.MessageParserBase import MessageParserBase
from inputparser.MessageMetadata import Message

class WhatsAppMessageParser(MessageParserBase):
    '''Parser for getting messages out of a WhatsApp Chat Backup TXT file.'''
    
    REGEX_GROUP_DATE: str = "dateStamp"
    REGEX_GROUP_TIME: str = "timeStamp"
    REGEX_GROUP_NAME: str = "name"
    REGEX_GROUP_MSG: str = "msg"

    REGEX_MSG_INFO = re.compile(f'^\[(?P<{REGEX_GROUP_DATE}>\d\d\.\d\d\.\d\d), (?P<{REGEX_GROUP_TIME}>\d\d:\d\d:\d\d)\] (?P<{REGEX_GROUP_NAME}>.+?): (?P<{REGEX_GROUP_MSG}>.+)')

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

    def parse_message_info(self, newMsgLine: str) -> Message:
        '''Parse the necessary metadata from the message.'''
        match = self.REGEX_MSG_INFO.match(newMsgLine)

        if match is None:
            return Message(message=newMsgLine)

        dateStamp: date = None
        timeStamp: time = None
        name = None
        msg = None

        matchedGroups: Dict[str, str] = match.groupdict()
        for groupName in matchedGroups:
            if self.REGEX_GROUP_DATE == groupName:
                dateStampStr: str = matchedGroups[self.REGEX_GROUP_DATE]
                dateStamp = datetime.strptime(dateStampStr, '%d.%m.%y').date()
            elif self.REGEX_GROUP_TIME == groupName:
                timeStampStr: str = matchedGroups[self.REGEX_GROUP_TIME]
                timeStamp = datetime.strptime(timeStampStr, '%H:%M:%S').time()
            elif self.REGEX_GROUP_NAME == groupName:
                name = matchedGroups[self.REGEX_GROUP_NAME]
            elif self.REGEX_GROUP_MSG == groupName:
                msg = matchedGroups[self.REGEX_GROUP_MSG]

        # Check if ALL values are NOT None anymore
        if not any(map(lambda x: x is None, (dateStamp, timeStamp, name, msg))):
            return Message(
                datestamp=dateStamp,
                timestamp=timeStamp,
                player=name,
                message=msg
            )
        else:
            return Message(message=newMsgLine)
        
    def build_message(self, metaObj: Message, messageText: List[str]) -> Message:
        if metaObj is None:
            print("Internal error: message building needs non-null meta object. Skipping...")
            return None
        metaObj.message = ''.join(messageText).strip()
        return metaObj

    def retrieve_snippets(self) -> Generator[Message, None, None]:
        '''This method parses lines for the messages and their meta-information.'''
        if self.filePath is None:
            raise FileNotFoundError("Cannot retrieve snippets. File Path is None")
        
        with open(self.filePath, 'r', encoding="utf-8") as f:
            messageText: List[str] = []
            metaObj: Message = None
            for line in f:
                if self.is_new_message(line):
                    if len(messageText) > 0:    # skip the yield if the first line starts
                        yield self.build_message(metaObj, messageText)   # yield the old, finished message
                    metaObj = self.parse_message_info(line) # Parse the msg's metainfo from the first line
                    messageText = [line[self.LENGTH_OF_PREAMBLE:]]
                else:
                    messageText.append(line)
            yield self.build_message(metaObj, messageText)   # yield the last message at EOF
