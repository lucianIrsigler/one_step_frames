from util.core.preprocess import parseRule
from util.core.formula import initFormula
from util.core.solution_search import greedyFirstSearch


def findStepFrameCondition(rule:str):
    rule = parseRule(rule)
    formula = initFormula(rule)
    result = greedyFirstSearch(formula)
    return result


if __name__=="__main__":
    # rule = "#x->y/#x->#y"
    # rule = "/#x->x"

    rule = input("Enter formula:")
    res = findStepFrameCondition(rule)

    for i in res[0]:
        print(i)
    print()
    for i in res[1]:
        print(i)