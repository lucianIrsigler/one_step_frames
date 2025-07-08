from util.formula import initFormula
from util.nomial import Nominal
from AST.abstract_syntax_tree import AbstractSyntaxTree
from util.errors import InputError

nominalTracker = Nominal()

def parseRule(rule:str):
    if (rule.find("/")==-1):
        raise InputError("Can't find /")

    arguements = rule.split("/")
    arguements = [i.strip() for i in arguements]

    if (arguements[0]==""):
        rule = arguements[1]
    else:
        # Don't think this really makes sense, because then you dont have a conclusion
        rule = arguements[0]

    return rule

def findStepFrameCondition(rule:str):
    formula = initFormula(rule)
    return formula

if __name__=="__main__":
    rule = "/#x->x"
    rule = parseRule(rule)
    formula = findStepFrameCondition(rule)
    print(formula)

    # tree = AbstractSyntaxTree()
    # tree.buildTree(formula)
    # #Can start cooking inference rules now
    # if (tree.root.left.value=="<"):
    #     print(tree.toInfix(tree.root.left))

