from inputparser.WhatsAppMessageParser import WhatsAppMessageParser
import unittest
import os

FILE_WITH_FEW_MESSAGES: str = os.path.abspath('test/_chat_4Messages.txt')
FILE_WITH_SINGLE_MESSAGE: str = os.path.abspath('test/_chat_1_Message.txt')
FILE_WITH_SINGLE_MESSAGE_MULTILINE: str = os.path.abspath('test/_chat_1_Message_Multiline.txt')
FILE_WITH_2_MESSAGES: str = os.path.abspath('test/_chat_2Messages.txt')

class Test_RetrieveSnippets_FindsAllMessages(unittest.TestCase):
    def test_RetrieveSnippets_4Messages(self):
        parser = WhatsAppMessageParser(FILE_WITH_FEW_MESSAGES)
        self.assertEqual(4, len(list(parser.retrieve_snippets())))

class Test_RetrieveSnippets_CorrectContent(unittest.TestCase):
    def test_RetrieveSnippets_CorrectMessageContent(self):
        parser = WhatsAppMessageParser(FILE_WITH_SINGLE_MESSAGE)
        expected_res = ['baz bar: Kennst des TELNR ?']
        self.assertEqual(expected_res, list(parser.retrieve_snippets()))

    def test_RetrieveSnippets_CorrectMessageContent_Multiline(self):
        parser = WhatsAppMessageParser(FILE_WITH_SINGLE_MESSAGE_MULTILINE)
        expected_res = ['''baz bar: Schon mal eins ohne Gelb gesehen? 😂

Wordle 223 6/6

⬛🟩🟩⬛⬛
⬛🟩🟩⬛🟩
⬛⬛⬛⬛⬛
🟩⬛⬛⬛⬛
🟩🟩🟩⬛🟩
🟩🟩🟩🟩🟩''']
        self.assertEqual(expected_res, list(parser.retrieve_snippets()))

    def test_RetrieveSnippets_CorrectMessageContent_2Messages(self):
        parser = WhatsAppMessageParser(FILE_WITH_2_MESSAGES)
        expected_res = ['''baz bar: Kennst des
 TELNR ?''', 'bar foo: Nö']
        self.assertEqual(expected_res, list(parser.retrieve_snippets()))

if __name__=='__main__':
    unittest.main()