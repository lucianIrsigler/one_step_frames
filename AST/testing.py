# add tests for stepFrameConditions.py
import unittest
from AST.shunting_yard import shuntingYard,replaceCharacters
from AST.abstract_syntax_tree import AbstractSyntaxTree
from AST.AST_error import ASTError


class TestShunt(unittest.TestCase):
    def test_shunting_yard(self):
        self.assertEqual(shuntingYard(""), "")

        tests = [
            ("#x<i(y)=>#x<#y", "x # y i < x # y # < =>"),
            ("i*(#x)<y=>#x<#y", "x # i* y < x # y # < =>"),
            ("#x<#i*(#x)", "x # x # i* # <"),
            ("w<#x=>w<#i*(#x)", "w x # < w x # i* # < =>"),
            ("@'w<x=>w<#i*(#x)", "w @' x < w x # i* # < =>"),
            ("w<#i*(#@'w)", "w w @' # i* # <"),
                   # Additional tests:
            ("i!i(y)", "y i i!"),                    # nested unary operators i! applied twice
            ("~#x&y", "x # ~ y &"),                   # unary ~ with binary &
            ("x=>y|z", "x y z | =>"),                  # implication and disjunction
            ("(x&y)|z", "x y & z |"),                 # parentheses to group
            ("i!(#@'x)", "x @' # i!"),              # unary i! with binary &
            ("i*(@z)", "z @ i*"),                    # unary i* with unary @
            ("i(#@'#@x)<z", "x @ # @' # i z <"),              # unary # with binary |
            ("i(i!(x))", "x i! i"),                   # nested i operators with parentheses
            ("i(i!(i*(x)))", "x i* i! i"),                   # nested i operators with parentheses
            ("w<#x=>w<#i!(#x)", "w x # < w x # i! # < =>"),
        ]

        for formula, expected_postfix in tests:
            print(formula)
            reverted = shuntingYard(formula)
            self.assertEqual(reverted, expected_postfix)


class TestAbstractSyntaxTree(unittest.TestCase):
    def setUp(self):
        self.ast = AbstractSyntaxTree()

    def test_empty_formula(self):
        with self.assertRaises(ASTError):
            self.ast.buildTree("")

    def test_simple_operand(self):
        root = self.ast.buildTree("x")
        self.assertEqual(root.value, "x")
        self.assertEqual(root.arity, 0)
        self.assertIsNone(getattr(root, 'left', None))
        self.assertIsNone(getattr(root, 'right', None))
        self.assertIsNone(getattr(root, 'child', None))

    def test_unary_operator(self):
        root = self.ast.buildTree("#x")
        self.assertEqual(root.value, "#")
        self.assertEqual(root.arity, 1)
        self.assertIsNotNone(root.child)
        self.assertEqual(root.child.value, "x")
        self.assertEqual(root.child.arity, 0)

    def test_binary_operator(self):
        root = self.ast.buildTree("#x<#y")
        self.assertEqual(root.value, "<")
        self.assertEqual(root.arity, 2)
        self.assertIsNotNone(root.left)
        self.assertIsNotNone(root.right)
        self.assertEqual(root.left.value, "#")
        self.assertEqual(root.right.value, "#")
        self.assertEqual(root.left.child.value, "x")
        self.assertEqual(root.right.child.value, "y")

    def test_complex_formula(self):
        formula = "#x<y=>#x<#y"
        root = self.ast.buildTree(formula)
        # root should be =>
        self.assertEqual(root.value, "=>")
        self.assertEqual(root.arity, 2)
        # left subtree is (#x < y)
        left = root.left
        self.assertEqual(left.value, "<")
        self.assertEqual(left.arity, 2)
        self.assertEqual(left.left.value, "#")
        self.assertEqual(left.left.arity, 1)
        self.assertEqual(left.left.child.value, "x")
        self.assertEqual(left.right.value, "y")
        # right subtree is (#x < #y)
        right = root.right
        self.assertEqual(right.value, "<")
        self.assertEqual(right.arity, 2)
        self.assertEqual(right.left.value, "#")
        self.assertEqual(right.left.child.value, "x")
        self.assertEqual(right.right.value, "#")
        self.assertEqual(right.right.child.value, "y")

    def test_invalid_expression_not_enough_operands(self):
        with self.assertRaises(ASTError):
            self.ast.buildTree("#")

    def test_invalid_expression_extra_operands(self):
        with self.assertRaises(ASTError):
            self.ast.buildTree("x y")

if __name__ == "__main__":
    unittest.main()
