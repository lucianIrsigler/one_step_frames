__all__ = ["findAtomicFormulas", "getConnectives", "checkIfFree", "initAtomicFormula", "initSubformula"]

import re


modalOperators = ["#","@","#'","@'"]
#TODO add <-> if needed
logicConnectives = ["=>","<","<'","#","#'","@","@'","~","i*","i!","i","^","|","&","->","<->"]


def findAtomicFormulas(formula:str,additionalConnectives:list[str]=[])->list[str]:
    """Given some formula, it returns all the atomic formulas
    in order. Given #x&x, it returns [#x,x]

    Args:
        formula (str): formula to split

    Returns:
        list[str]: list of atomic formulas in order
    """
    symbols = None
    if additionalConnectives==[]:
        symbols = logicConnectives
    else:
        additionalConnectives.extend(logicConnectives)
        symbols = additionalConnectives.copy()

    delimiters = f'[{"".join(symbols)}]'
    subformulasAntecdent = re.split(delimiters,formula)

    # Remove empty strings from the list
    subformulasAntecdent = [subformula for subformula in subformulasAntecdent if subformula.strip()]
    
    return subformulasAntecdent


def getConnectives(formula:str,additionalConnectives:list[str]=[])->list[str]:
    """Given some formula, it returns all the connectives used in order.
    Given #x&x|y, it returns [&,|]

    Args:
        formula (str): formula to split

    Returns:
        list[str]: list of logical connectives in order
    """
    symbols = None
    if additionalConnectives==[]:
        symbols = logicConnectives
    else:
        additionalConnectives.extend(logicConnectives)
        symbols = additionalConnectives.copy()

    symbols = sorted(symbols, key=len, reverse=True)
    delimiters = f"(?:{'|'.join(map(re.escape,symbols))})"
    connectives = re.findall(delimiters,formula)
    return connectives


def getVariable(formula:str)->list[str]:
    outputList = []
    for i in formula:
        if i.isalpha() and i!="i" and i not in modalOperators:
            outputList.append(i)
    return outputList


def checkIfFree(atomicFormula:str)->bool:
    """Given some atomic formula, it checks if the variable is free.
    Example:#x -> NOT FREE,x -> FREE. 
    It works by first finding the propositional variable,
    then checking if it has some modal operator connected to it. 

    Args:
        atomicFormula (str): atomic formula to check

    Returns:
        bool: True if free, otherwise False
    """
    propIdx = -1

    for i,j in enumerate(atomicFormula):
        if j.isalpha():
            propIdx = i

        if (propIdx!=-1):
            break
    
    temp = propIdx

    while (temp>=0):
        if atomicFormula[temp] in modalOperators:
            return False
        temp-=1

    return True


def initAtomicFormula(formula:str)->str:
    """Initializes an atomic formula. If it is free, then it puts a 
    nominial with it, otherwise leaves as is.

    Args:
        formula (str): atomic formula

    Returns:
        str: initialized formula
    """
    isFree = checkIfFree(formula)

    if (isFree):
        return f"i({formula})"
    else:
        return formula


def initSubformula(subformula:str)->str:
    output = ""
    subformula = subformula.strip()
    if "->" not in subformula:
        antecedent = subformula
        consequent = ""
    else:
        antecedent,consequent = subformula.split("->")
    
    #TODO take length of subformulaAntecdent, and connectives. if 
    # connectives -1 length of subformulaAnt., then its valid?

    #STEP 1
    #antecedent

    subformulaAntecedent = findAtomicFormulas(antecedent)
    connectives = getConnectives(antecedent)
    connectiveCounter = 0

    for i in range(len(subformulaAntecedent)):
        atomicForm = initAtomicFormula(subformulaAntecedent[i])
        output += atomicForm

        if (connectiveCounter != len(connectives)):
            output += connectives[connectiveCounter]
            connectiveCounter+=1
    
    #STEP 2
    if consequent == "":
        return output
    
    output+="<"

    #STEP 3
    #consequent
    subformulaConsequent = findAtomicFormulas(consequent)
    connectives = getConnectives(consequent)
    connectiveCounter = 0
    
    for i in range(len(subformulaConsequent)):
        atomicForm = initAtomicFormula(subformulaConsequent[i])
        output += atomicForm

        if (connectiveCounter != len(connectives)):
            output += connectives[connectiveCounter]
            connectiveCounter+=1

    return output
