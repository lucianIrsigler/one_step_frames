import unittest
from util.preprocess import checkIfNoTextAfterCharacter, checkIfNoTextBeforeCharacter, checkIfValidCharacters
from util.errors import InputError
import util.formula as formula_util

class UtilTesting(unittest.TestCase):
    # Preprocessing Tests
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

    # Formula tests
    def test_checkIfFree(self):
        self.assertTrue(formula_util.checkIfFree("x"))
        self.assertFalse(formula_util.checkIfFree("#x"))
        self.assertFalse(formula_util.checkIfFree("@x"))
    
    def test_initAtomicFormula(self):
        self.assertEqual(formula_util.initAtomicFormula("x"), "i(x)")
        self.assertEqual(formula_util.initAtomicFormula("#x"), "#x")
        self.assertEqual(formula_util.initAtomicFormula("@x"), "@x")

    """def test_initSubformula(self):
        self.assertEqual(formula_util.initSubformula("x"), "i(x)")
        self.assertEqual(formula_util.initSubformula("#x"), "#x")
        self.assertEqual(formula_util.initSubformula("@x"), "@x")
        self.assertEqual(formula_util.initSubformula("x&y"), "i(x)&i(y)")
        self.assertEqual(formula_util.initSubformula("x=>y"), "i(x)=>i(y)")

    def test_findAtomicFormulas(self):
        formula = "x&y|z"
        expected = ["x", "y", "z"]
        result = formula_util.findAtomicFormulas(formula)
        self.assertEqual(result, expected)
    
    def test_getConnectives(self):
        self.assertEqual(formula_util.getConnectives("x&y|z"), ["&", "|"])
        self.assertEqual(formula_util.getConnectives("x=>y"), ["=>"])
        self.assertEqual(formula_util.getConnectives("x<->y"), ["<->"])
        self.assertEqual(formula_util.getConnectives("x#y@z"), ["#", "@"])
        self.assertEqual(formula_util.getConnectives(""),[])
    
    def test_getVariable(self):
        self.assertEqual(formula_util.getVariable("x&y|z"), ["x", "y", "z"])
        self.assertEqual(formula_util.getVariable("#x@z"), ["x", "z"])
        self.assertEqual(formula_util.getVariable("i(x)"), ["x"])
        self.assertEqual(formula_util.getVariable("i(x)&i(y)"), ["x", "y"])
        self.assertEqual(formula_util.getVariable(""), [])
        self.assertEqual(formula_util.getVariable("i"), [])
        self.assertEqual(formula_util.getVariable("#"), [])
        self.assertEqual(formula_util.getVariable("@'=>@"), [])
"""