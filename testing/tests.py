# add tests for stepFrameConditions.py
import unittest
from util.preprocess import checkIfNoTextAfterCharacter, checkIfNoTextBeforeCharacter, checkIfValidCharacters
from util.errors import InputError

class TestStepFrameConditions(unittest.TestCase):
    def test_checkIfNoTextAfterCharacter(self):
        self.assertTrue(checkIfNoTextAfterCharacter("test#", "#"))
        self.assertFalse(checkIfNoTextAfterCharacter("test#text", "#"))
        self.assertTrue(checkIfNoTextAfterCharacter("test", "#"))

    def test_checkIfNoTextBeforeCharacter(self):
        self.assertTrue(checkIfNoTextBeforeCharacter("#test", "#"))
        self.assertFalse(checkIfNoTextBeforeCharacter("text#test", "#"))
        self.assertTrue(checkIfNoTextBeforeCharacter("test", "#"))

    def test_checkIfValidCharacters(self):
        valid_rule = "a#b@c->d<->e"
        invalid_rule = "a#b@c->d<->e$"

        self.assertTrue(checkIfValidCharacters(valid_rule))
        with self.assertRaises(InputError):
            checkIfValidCharacters(invalid_rule)


if __name__ == '__main__':
    unittest.main()
