# add tests for stepFrameConditions.py
import unittest
from util.preprocess import checkIfNoTextAfterCharacter, checkIfNoTextBeforeCharacter, checkIfValidCharacters
from util.errors import InputError
import util.formula as formula_util
from AST.shunting_yard import shunting_yard

class TestStepFrameConditions(unittest.TestCase):
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

    def test_initSubformula(self):
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

    
    def test_shuntingYard(self):
        # Test cases for shunting_yard function
        # Basic binary operators
        self.assertEqual(shunting_yard("x=>y"), "x y =>")
        self.assertEqual(shunting_yard("a->b"), "a b ->")
        self.assertEqual(shunting_yard("p<->q"), "p q <->")
        self.assertEqual(shunting_yard("x&y"), "x y &")
        self.assertEqual(shunting_yard("a|b"), "a b |")
        self.assertEqual(shunting_yard("p<q"), "p q <")
        self.assertEqual(shunting_yard("x<'y"), "x y <'")

        # Unary operators
        self.assertEqual(shunting_yard("~x"), "~x")
        self.assertEqual(shunting_yard("#p"), "#p")
        self.assertEqual(shunting_yard("@a"), "@a")
        self.assertEqual(shunting_yard("#'x"), "#'x")
        self.assertEqual(shunting_yard("@'y"), "@'y")
        self.assertEqual(shunting_yard("^z"), "^z")

        # Complex expressions with parentheses
        self.assertEqual(shunting_yard("(x=>y)"), "x y =>")
        self.assertEqual(shunting_yard("~(p&q)"), "p q & ~")
        self.assertEqual(shunting_yard("#(a|b)"), "a b | #")
        self.assertEqual(shunting_yard("(a&b)=>(c|d)"), "a b & c d | =>")

        # Multiple operators with precedence
        self.assertEqual(shunting_yard("x&y|z"), "x y & z |")
        self.assertEqual(shunting_yard("a=>b=>c"), "a b => c =>")
        self.assertEqual(shunting_yard("p<q<r"), "p q < r <")
        self.assertEqual(shunting_yard("x<->y<->z"), "x y <-> z <->")

        # Mixed precedence
        self.assertEqual(shunting_yard("a&b=>c"), "a b & c =>")
        self.assertEqual(shunting_yard("a=>b&c"), "a b c & =>")
        self.assertEqual(shunting_yard("a|b&c"), "a b c & |")
        self.assertEqual(shunting_yard("a&b|c&d"), "a b & c d & |")

        # Nested unary operators
        self.assertEqual(shunting_yard("~~x"), "~~x")
        self.assertEqual(shunting_yard("~#p"), "~#p")
        self.assertEqual(shunting_yard("#@a"), "#@a")
        self.assertEqual(shunting_yard("^~x"), "^~x")

        # Mixed unary and binary
        self.assertEqual(shunting_yard("~x=>y"), "~x y =>")
        self.assertEqual(shunting_yard("x=>#y"), "x #y =>")
        self.assertEqual(shunting_yard("~x&~y"), "~x ~y &")
        self.assertEqual(shunting_yard("#x<@y"), "#x @y <")

        # Complex nested expressions
        self.assertEqual(shunting_yard("(~x=>y)&(z|w)"), "~x y => z w | &")
        self.assertEqual(shunting_yard("~(x&y)=>(z<->w)"), "x y & ~ z w <-> =>")
        self.assertEqual(shunting_yard("#(a=>b)<'@(c|d)"), "a b => # c d | @ <'")

        # Precedence with comparison operators
        self.assertEqual(shunting_yard("#x<y=>#x<#y"), "#x y < #x #y < =>")
        self.assertEqual(shunting_yard("x<y&z<w"), "x y < z w < &")
        self.assertEqual(shunting_yard("a<b=>c<d"), "a b < c d < =>")

        # Right associative operators
        self.assertEqual(shunting_yard("a=>b=>c=>d"), "a b => c => d =>")
        self.assertEqual(shunting_yard("#x=>#y=>#z"), "#x #y => #z =>")

        # Left associative operators
        self.assertEqual(shunting_yard("a<->b<->c"), "a b <-> c <->")
        self.assertEqual(shunting_yard("x<y<z"), "x y < z <")

        # Complex mixed precedence
        self.assertEqual(shunting_yard("~a&b=>c|d"), "~a b & c d | =>")
        self.assertEqual(shunting_yard("#a<b&#c<d"), "#a b < #c d < &")
        self.assertEqual(shunting_yard("(a&b)|(c=>d)"), "a b & c d => |")

        # Edge cases with single variables
        self.assertEqual(shunting_yard("x"), "x")
        self.assertEqual(shunting_yard("a"), "a")
        self.assertEqual(shunting_yard("z"), "z")

        # Special i() operands
        self.assertEqual(shunting_yard("i(x)=>i(y)"), "i(x) i(y) =>")
        self.assertEqual(shunting_yard("~i(p)&i(q)"), "~i(p) i(q) &")
        self.assertEqual(shunting_yard("#i(a)<@i(b)"), "#i(a) @i(b) <")

        # Complex expressions with multiple levels
        self.assertEqual(shunting_yard("((a&b)=>(c|d))<=>(e<->f)"), "a b & c d | => e f <-> <->")
        self.assertEqual(shunting_yard("~(#a<b)=>(c&(d|e))"), "a b < # ~ c d e | & =>")
        self.assertEqual(shunting_yard("#(a=>b)&@(c<->d)"), "a b => # c d <-> @ &")

if __name__ == '__main__':
    # unittest.main()
    pass
