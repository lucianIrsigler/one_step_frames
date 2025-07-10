from AST.core.abstract_syntax_tree import AbstractSyntaxTree
from AST.core.ast_util import getSpecificNodes,toInfix
from util.errors.errors import InferenceError
from util.rules.nominal_rules import NominalInference
from util.rules.adjunction_rules import AdjunctionInference


def processFormulaWithAST(formula: str) -> list[str]:
    """Process formula using AST and return nominal inferences."""
    tree = AbstractSyntaxTree()
    tree.buildTree(formula)
    
    if tree.root is None:
        raise InferenceError("Failed to build AST from formula")
    
    nodes = getSpecificNodes(tree.root, "<")
    if not nodes:
        raise InferenceError("No '<' nodes found in AST")
    
    infixStrings = [toInfix(i) for i in nodes]

    return infixStrings


def inferenceRules(formula:str)->dict[str,list[str]]:
    formulae = processFormulaWithAST(formula)
    inferenceEngignes = [NominalInference(),AdjunctionInference()]
    resultDict = {i:[] for i in formulae}

    for engine in inferenceEngignes:
        for form in resultDict.keys():
            availableInferenceRules = engine.get_inferences(form)
            resultDict[form].extend(availableInferenceRules)
    
    return resultDict


if __name__=="__main__":
    formula = "#x<i(y)=>#x<#y"
    inferenceRules(formula)