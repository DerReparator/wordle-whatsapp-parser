'''Parser for getting messages out of the WhatsApp Chat Backup ZIP file.
'''
from typing import Generator
from inputparser.MessageMetadata import Message
from inputparser.WhatsAppMessageParser import WhatsAppMessageParser
from inputparser.MessageParserBase import MessageParserBase
import os, shutil
from pathlib import Path
import zipfile
import tempfile

class WhatsAppMessageZipParser(MessageParserBase):
    CHAT_FILE_NAME = '_chat.txt'

    def __init__(self, filePath: str) -> None:
        super().__init__()
        if (os.path.isfile(filePath)):
            self.filePath = filePath
        else:
            raise FileNotFoundError(f'The WhatsApp .ZIP file "{filePath}" was not valid.')

    def __unzip_Chat_zip(self) -> str:
        '''Unzip the Chat *.zip and return the path to the chat *.txt'''
        unzipDestination: str = tempfile.mkdtemp(prefix='WordleParser_')
        with zipfile.ZipFile(self.filePath, 'r') as zip_file:
            print(f"I will unzip the WhatsApp ZIP {self.filePath} into {unzipDestination}")
            zip_file.extractall(unzipDestination)
        
        unzippedChatFile: str = os.path.join(unzipDestination, self.CHAT_FILE_NAME)
        if not os.path.isfile(unzippedChatFile):
            raise RuntimeError(f'Expected to find unzipped file "{unzippedChatFile}". But it was not there.')
        return unzippedChatFile

    def __remove_temp_folder(self, chatFileLocation: str):
        toBeRemoved: str = None
        if (os.path.isdir(chatFileLocation)):
            toBeRemoved = Path(chatFileLocation).absolute()
        elif (os.path.isfile(chatFileLocation)):
            toBeRemoved = Path(chatFileLocation).parent.absolute()
        if (toBeRemoved is not None):
            shutil.rmtree(toBeRemoved)
            print(f"Successfully removed temp folder {toBeRemoved}")

    def retrieve_snippets(self) -> Generator[Message, None, None]:
        chatTxtPath: str = self.__unzip_Chat_zip()
        
        parser = WhatsAppMessageParser(chatTxtPath)
        yield from parser.retrieve_snippets()

        self.__remove_temp_folder(chatTxtPath)
