import WordleStringParser
from WordleStringParser import WordleMetadata
import unittest

VALID_MESSAGE: str = '''[26.02.22, 23:30:51] foo bar: Wordle 252 5/6

🟨⬜⬜⬜⬜
🟨⬜⬜🟨⬜
🟨🟨⬜⬜⬜
🟨⬜🟨🟩⬜
🟩🟩🟩🟩🟩
'''

VALID_MESSAGE_DAYINDEX: int = 252
VALID_MESSAGE_STEPS: int = 5
VALID_MESSAGE_SOLUTION: str = '''🟨⬜⬜⬜⬜
🟨⬜⬜🟨⬜
🟨🟨⬜⬜⬜
🟨⬜🟨🟩⬜
🟩🟩🟩🟩🟩'''

VALID_MESSAGE_FAILED: str = '''[30.01.22, 10:42:56] bar foo: Wordle 225 X/6

⬛⬛⬛⬛⬛
⬛🟨⬛⬛🟨
⬛🟨🟨⬛⬛
⬛🟨⬛🟨⬛
🟨🟩🟨⬛⬛
⬛🟩🟩🟩🟩
'''

VALID_MESSAGE_FAILED_DAYINDEX: int = 225
VALID_MESSAGE_FAILED_STEPS: str = 'X'
VALID_MESSAGE_FAILED_SOLUTION: str = '''⬛⬛⬛⬛⬛
⬛🟨⬛⬛🟨
⬛🟨🟨⬛⬛
⬛🟨⬛🟨⬛
🟨🟩🟨⬛⬛
⬛🟩🟩🟩🟩'''


VALID_MESSAGE_WITH_TEXT_AFTERWARDS = '''
[09.02.22, 14:17:26] foo bar: so schlecht
wordle 235 X/6

⬛⬛⬛⬛⬛
⬛🟨⬛⬛⬛
⬛🟨🟨⬛⬛
⬛🟨🟨⬛⬛
🟨🟨🟨⬛🟨
🟩🟨🟨⬛⬛
asdfasfasdfasdfhhbzn
'''

class Test_ParseMessage_IsNone(unittest.TestCase):
    '''All cases where "None" should be returned.'''
    def test_ofEmpty(self):
        self.assertIsNone(WordleStringParser.parseMessage(""))

    # doesnt work because of type-hinting
    #def test_ofNone(self):
    #    self.assertIsNone(MessageParser.parseMessage(None))

class Test_ParseMessage_ParsesDayIndex(unittest.TestCase):
    def test_parseDayIdx(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE)
        self.assertIsNotNone(ret)
        parsedIdx: int = ret.day_index
        self.assertEqual(VALID_MESSAGE_DAYINDEX, parsedIdx)

class Test_ParseMessage_ParsesSolutionLength(unittest.TestCase):
    def test_parseSolutionLength(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE)
        self.assertIsNotNone(ret)
        parsedSolLen = ret.steps_to_solution
        self.assertEqual(VALID_MESSAGE_STEPS, parsedSolLen)

    def test_parseSolutionLengthOfFailed(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE_FAILED)
        self.assertIsNotNone(ret)
        parsedSolLen = ret.steps_to_solution
        self.assertEqual(VALID_MESSAGE_FAILED_STEPS, parsedSolLen)

class Test_ParseMessage_CorrectSolution(unittest.TestCase):
    def test_parseValidMessage(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE)
        self.assertIsNotNone(ret)
        parsedSolution: str = ret.solution
        self.assertEqual(VALID_MESSAGE_SOLUTION, parsedSolution)

    def test_parseValidMessageFailed(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE_FAILED)
        self.assertIsNotNone(ret)
        parsedSolution: str = ret.solution
        self.assertEqual(VALID_MESSAGE_FAILED_SOLUTION, parsedSolution)

class Test_ParseMessage_IsParsedSuccessfully(unittest.TestCase):
    '''Test input for successful parsing without focusing on any particular parsed value.'''
    def test_textAfterWordle(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE_WITH_TEXT_AFTERWARDS)
        self.assertIsNotNone(ret)

class Test_ParseMessage_InputNameIsInOutput(unittest.TestCase):
    name: str = "fooBar123"
    
    def test_inputNameInOutput(self):
        ret: WordleMetadata = WordleStringParser.parseMessage(VALID_MESSAGE, self.name)
        self.assertIsNotNone(ret)
        parsedName = ret.player
        self.assertEqual(self.name, parsedName)

if __name__=='__main__':
    unittest.main()
