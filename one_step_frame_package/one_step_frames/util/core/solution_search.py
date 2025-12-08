from .priority_queue import PriorityQueue
from ..rules.inference_rules import inferenceRules
from ..rules.ackermann_rules import findVariables,applyAckermannRule,ackermannHeuristic


def goalTest(formula:str)->bool:
    return len(findVariables(formula))==0


def getRules(currentFormula:str, formula:str,numVariables:int,delta=False):
    output = []

    currentInferenceRules,trackingRules = inferenceRules(formula,currentFormula)

    for subform in currentInferenceRules.keys():
        for replacement in currentInferenceRules[subform]:
            tempFormula = currentFormula

            if delta and tempFormula.count("=>") == 1 and replacement.count("=>")>0:
                tempFormula = tempFormula.replace(f"=>{subform}",f",{replacement}")
            else:
                tempFormula = tempFormula.replace(subform,replacement)

            if (tempFormula.count("=>"))>1:
                continue
            
            if replacement.count("=>")==1:
                score = ackermannHeuristic(tempFormula,replacement.split("=>")[0],numVariables)
            else:
                score = ackermannHeuristic(tempFormula,replacement,numVariables)

            output.append((score,replacement))

    return output,trackingRules


def updateRulesLogs(tracking,currentFormula,form,trackRules):
    for _,inferenceRules in tracking.items():
        for k,v in inferenceRules.items():
            tempFormula = currentFormula.replace(form,k)
            trackRules[tempFormula] = v


def applyInferenceRules(formulae:list,currentFormula,numberVariables,trackRules,isDelta=False):
    newRules = []
    for i,j in enumerate(formulae):
        rulesWithScores,tracking = getRules(currentFormula,j,numberVariables,isDelta)

        for k in rulesWithScores:
            replacedFormula = currentFormula

            if isDelta and k[1].find("=>")!=-1 and replacedFormula.find("=>")!=-1:
                replacedFormula = replacedFormula.replace("=>",",")
            
            # TODO: Limit delta rules to only nominal
            if isDelta and tracking[j][k[1]].find("N")==-1:
                continue

            replacedFormula = replacedFormula.replace(j,k[1])
            newRules.append((k[0],replacedFormula))

        updateRulesLogs(tracking,currentFormula,j,trackRules)

    return newRules


def greedyFirstSearch(formula: str) -> tuple[list[str], list[str], dict[str,str]]:
    """Perform a greedy first search on the formula to find a solution.
    A Priority stack is used with the ackermann heuristic 
    to prioritize items.

    Args:
        formula (str): The formula to search on.
        
    Returns:
        tuple: A tuple containing:
            - list[str]: The order of rules 
            - list[str]: Logging information
            - dict[str,str]: The corresponding rules index(Nominal rule 1, adjunction 1 etc)
    """
    if "=>" not in formula:
        gamma = []
        delta = formula
    else:
        gamma = formula.split("=>")[0].split(",")
        delta = formula.split("=>")[1]

    variables = set(findVariables(formula))

    search = True
    iterations = 0

    visited = []

    trackState = []
    trackLog = []
    trackRules = {}
    
    #init
    trackRules[formula]="INIT"

    pq = PriorityQueue()

    pq.push(-len(variables),formula)   
    
    while not pq.empty() and search:
        iterations+=1
        item = pq.pop() 

        if (item is None):
            break

        currentFormula = item[-1]

        if currentFormula in visited:
            continue
        
        visited.append(currentFormula)
        trackState.append(currentFormula)


        if goalTest(currentFormula):
            search = False
            trackLog.append(f"Goal found:{currentFormula}")
            continue
        
        #Split by something arbitary
        arguments = [i.split(",") for i in currentFormula.split("=>")]

        if currentFormula.count("=>")==1:
            gamma = arguments[0]
            delta = arguments[1]
        else:
            delta = arguments[0]
        

        trackLog.append(f"Current formula:{currentFormula}. SCORE: {item[0]}")

        appliedAck = False

        for i,j in enumerate(gamma):
            if appliedAck:
                continue

            #Checks if can apply, then applys
            resultFormula,var = applyAckermannRule(currentFormula,j)

            if (resultFormula==currentFormula):
                continue

            appliedAck = True
            gamma = resultFormula.split("=>")[0].split(",")
            delta = resultFormula.split("=>")[1]

            if (gamma[0]==""):
                #We have eliminate all the games now
                gamma.clear()
                resultFormula = resultFormula.replace("=>","")
            

            trackRules[resultFormula] = "ACK"
            trackLog.append(f"Eliminated {var} in {j} yielding {currentFormula}-->{resultFormula}")
            
            pq.push(999,resultFormula)

        if appliedAck:
            continue
        
        #Apply rules to gamma
        rules = applyInferenceRules(gamma,currentFormula,len(variables),trackRules)

        for i in rules:
            pq.push(*i)
        
        #Apply rules to delta
        rules = applyInferenceRules(delta,currentFormula,len(variables),trackRules,True)

        for i in rules:
            pq.push(*i)
        

    #Filter to only have the rules that leads to the solution
    trackRulesFiltered = {k:v for k,v in trackRules.items() if k in trackState}

    return trackState,trackLog,trackRulesFiltered,pq.counter
    
