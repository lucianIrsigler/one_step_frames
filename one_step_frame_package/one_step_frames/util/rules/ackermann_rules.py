import re


def findNominals(string:str):
    matches = re.findall(r"\b[uwv](?:_\d+)?\b", string)
    nominals = set(matches)
    return nominals


def findVariables(formula:str):
    """Find all variables in a given formula.
    Args:
        formula (str): The formula to search for variables.
    Returns:
        set: A set of variables found in the formula.
    """
    # Matches single lowercase letters that are not 'u', 'v', 'w', or 'i'
    matches = re.findall(r"[a-hj-tx-z](?:_\d+)?", formula)
    variables = set(matches)
    return variables


def checkPolarity(formula:str,variable:str)->bool|None:
    """Check the polarity of a variable in a formula.

    Args:
        formula (str): The formula to check.
        variable (str): The variable to check the polarity of.

    Returns:
        None|bool: Returns true if polarity is positive, false if negative, 
        and None if the variable is not found/not valid.
    """
    
    if variable not in findVariables(formula) or formula.find("<")==-1:
        return None
    
    splitParts = formula.split("<")

    if (len(splitParts)!=2):
        return None

    if variable in findVariables(splitParts[0]):
        return False
    else:
        return True 


def ackermannHeuristic(formula:str,subformula:str,totalNumberVariables:int=-1):
    """Calculate the Ackermann heuristic for a given formula.
    If no => -> get -2, if varaibles eliminated, return the number of variables eliminated -2.
    Checks both version of the Ackermann rule.
    +1 if the variable is in the antecedent, +1 if the variable is not in the consequent, and 
    +1 if the polarity is negative.
    +1 if the variable is in the consequent, +1 if the variable is not in the antecedent, and 
    +1 if the polarity is positive.

    Args:
        formula (str): The formula to evaluate.
        totalNumberVariables (int, optional): The total number of variables in the formula. Defaults
        to -1

    Returns:
        int: The score based on the Ackermann heuristic.
    """
    checkNumberVariablesElim = totalNumberVariables-len(findVariables(formula))
    numberNominals = len(findNominals(formula))

    baseScore = checkNumberVariablesElim + numberNominals

    if (formula.find(subformula)==-1):
        errorMessage = f"{subformula} does not occur in formula {formula}"
        raise ValueError(errorMessage)
    
    

    if (formula.find("=>")==-1):
        return baseScore-3 # -3 since cant apply
    
    score = -3 + baseScore
    variables = findVariables(formula)
    arguments = formula.split("=>")

    if (len(arguments)!=2):
        return baseScore
    
    gamma = arguments[0].split(",")
    delta = arguments[1]

    subformula_args = subformula.split("<")

    if (len(subformula_args)!=2):
        return baseScore

    # ackermann 1
    if (subformula_args[0] in variables):
        currentVariable = subformula_args[0]
        
        # +1 if you cant find x in phi
        if (subformula_args[1].find(currentVariable)==-1):
            score+=1

        allPositive = True
        for arg in gamma:
            polarity = checkPolarity(arg,currentVariable)

            if polarity==False:
                allPositive = False

        # +1 if x is postive in all gamma
        if (allPositive):
            score+=1
        
        # +1 if x is negative/not there in delta
        if checkPolarity(delta,currentVariable)!= True:
            score+=1
    # ackermann 2
    elif (subformula_args[1] in variables):
        currentVariable = subformula_args[1]
        
        # +1 if you cant find x in phi
        if (subformula_args[0].find(currentVariable)==-1):
            score+=1

        allNegative = True
        for arg in gamma:
            if (arg == subformula):
                continue

            polarity = checkPolarity(arg,currentVariable)

            if polarity==True:
                allNegative = False

        # +1 if x is negative in all gamma
        if (allNegative):
            score+=1
        
        # +1 if x is postive/not there in delta
        if checkPolarity(delta,currentVariable)!= False:
            score+=1
    else:
        return baseScore
    
    return score


def checkAckermannConditions(formula: str, subformula: str) -> tuple[bool, int, str]:
    """Check if the Ackermann rule can be applied to a given formula with a specific variable.
    Args:
        formula (str): The formula to check.
        subformula (str): The subformula to check
    Returns:
        tuple: A tuple containing a boolean indicating if the rule can be applied and an integer
        indicating the rule index (0 or 1) if applicable, or -1 if not applicable. Also str to
        indicate the variable
    """
    emptyOutput = (False,-1,"")

    if (formula.find(formula)==-1):
        errorMessage = f"{subformula} does not occur in formula {formula}"
        raise ValueError(errorMessage)
    
    if (formula.find("=>")==-1):
        return emptyOutput
    
    variables = findVariables(formula)
    
    # toAdd = [f"i({i})" for i in variables]
    # for i in toAdd:
    #     variables.add(i)
    
    arguments = formula.split("=>")

    gamma = arguments[0].split(",")
    delta = arguments[1]

    subformula_args = subformula.split("<")

    if (len(subformula_args)!=2):
        return emptyOutput

    # ackermann 1
    canApply = True
    ackRule = -1
    currentVariable = ""

    if (subformula_args[0] in variables):
        currentVariable = subformula_args[0]
        
        # +1 if you cant find x in phi
        if not (subformula_args[1].find(currentVariable)==-1):
            canApply = False

        allPositive = True
        for arg in gamma:
            polarity = checkPolarity(arg,currentVariable)

            if polarity==False:
                allPositive = False

        # +1 if x is postive in all gamma
        if not (allPositive):
            canApply = False
        
        # +1 if x is negative/not there in delta
        if not checkPolarity(delta,currentVariable)!= True:
            canApply = False

        ackRule = 0 if canApply else -1
    # ackermann 2
    elif (subformula_args[1] in variables):
        currentVariable = subformula_args[1]
        
        canApply = True

        # +1 if you cant find x in phi
        if currentVariable in findVariables(subformula_args[0]):
            canApply = False

        allNegative = True
        for arg in gamma:
            if (arg == subformula):
                continue

            polarity = checkPolarity(arg,currentVariable)

            if polarity==True:
                allNegative = False

        # +1 if x is negative in all gamma
        if not (allNegative):
            canApply = False
        
        # +1 if x is postive/not there in delta
        if not checkPolarity(delta,currentVariable)!= False:
            canApply = False

        ackRule = 1 if canApply else -1
    
    if (ackRule==-1):
        return emptyOutput
    
    return (canApply,ackRule,currentVariable)


def applyAckermannRule(formula:str,subformula:str)->tuple[str, str]:
    """
    Apply the Ackermann rule to a given formula.
    
    Args:
        formula (str): The formula to apply the Ackermann rule to.
    Returns:
        str: The modified formula after applying the Ackermann rule, or the original formula if
        Ackermann rule cannot be applied.
    """
    checkCondition = checkAckermannConditions(formula,subformula)
    canApply,rule,var = checkCondition

    if not (canApply):
        return formula,""
    
    arguments = formula.split("=>")

    gamma = arguments[0].split(",")
    delta = arguments[1]

    idx = gamma.index(subformula)
    
    """
    checkAckermannConditions2(denote as f) returns 0 if ack rule 1, and 
    1 if rule 2. However this doesnt correlate to the actual formula
    we need to sub in.
    So if ack 1[or 0 by f], then its x < phi. Thus index 1 is the phi
    If ack 2[or 1 by f], then its phi < x. Thus index  0 is the phi.
    Take the abs(rule-1): 
       abs(0-1) => 1 [works for rule 1]
       abs(1-1) => 0 [works for rule 2]
    """
    rule = abs(rule-1)

    phi = gamma[idx].split("<")[rule]

    gamma = [re.sub(rf"\b{var}(?!\d)", phi, j) for i,j in enumerate(gamma) if i!=idx]
    # gamma = [j.replace(var,phi) for i,j in enumerate(gamma) if i!=idx]

    # delta = delta.replace(var,phi)
    delta = re.sub(rf"\b{var}(?!\d)", phi, delta)

    return f"{",".join(gamma)}=>{delta}",var
