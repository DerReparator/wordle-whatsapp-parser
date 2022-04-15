'''Parser for getting messages out of the WhatsApp Chat Backup ZIP file.
'''
from typing import Generator
import MessageParserBase

class WhatsAppMessageZipParser(MessageParserBase):
    
    def retrieve_snippets(self) -> Generator[str, None, None]:
        pass