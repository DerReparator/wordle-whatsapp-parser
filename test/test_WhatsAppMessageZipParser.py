from inputparser.WhatsAppMessageZipParser import WhatsAppMessageZipParser
import unittest
import os

FILE_WITH_2_MESSAGES: str = os.path.abspath('test/_chat_2Messages.zip')

class Test_RetrieveSnippets_FindsAllMessages(unittest.TestCase):
    def test_RetrieveSnippets_4Messages(self):
        parser = WhatsAppMessageZipParser(FILE_WITH_2_MESSAGES)
        self.assertEqual(2, len(list(parser.retrieve_snippets())))

class Test_RetrieveSnippets_CorrectContent(unittest.TestCase):
    def test_RetrieveSnippets_CorrectMessageContent(self):
        parser = WhatsAppMessageZipParser(FILE_WITH_2_MESSAGES)
        expected_res = ['''baz bar: Kennst des
 TELNR ?''', 'bar foo: Nö']
        self.assertEqual(expected_res, list(parser.retrieve_snippets()))

if __name__=='__main__':
    unittest.main()
