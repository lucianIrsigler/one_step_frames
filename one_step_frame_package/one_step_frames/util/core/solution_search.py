from .priority_queue import PriorityQueue
from ..rules.inference_rules import inferenceRules
from ..rules.ackermann_rules import findVariables,applyAckermannRule,ackermannHeuristic


def goalTest(formula:str)->bool:
    return len(findVariables(formula))==0


def getRules(currentFormula:str, formula:str,numVariables:int):
    output = []

    currentInferenceRules,trackingRules = inferenceRules(formula)

    for subform in currentInferenceRules.keys():
        for replacement in currentInferenceRules[subform]:
            tempFormula = currentFormula
            tempFormula = tempFormula.replace(subform,replacement)

            if (tempFormula.count("=>"))>1:
                continue

            score = ackermannHeuristic(tempFormula,replacement,numVariables)
            output.append((score,replacement))

    return output,trackingRules



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

    trackState = []
    trackLog = []
    trackRules = {}
    
    #init
    trackRules[formula]="INIT"

    pq = PriorityQueue()
    # -1, "" represents first
    pq.push(0,(-1,""))   
    
    while not pq.empty() and search:
        iterations+=1
        item = pq.pop() 

        if (item==None):
            break
        

        prevFormula = f"{",".join(gamma)}=>{delta}"

        if prevFormula.split("=>")[0]=="":
            prevFormula = prevFormula.replace("=>","")

        
        if goalTest(prevFormula):
            search = False
            trackLog.append(f"Goal found:{prevFormula}")
            continue

        poppedIdx = item[0]
        poppedFormula = item[1]

        if (poppedIdx!=-1):
            gamma[poppedIdx] = poppedFormula
        
        currentFormula = f"{",".join(gamma)}=>{delta}"
        
        #Some nominal rules add ",", making sure it gets caught
        gamma = [part for item in gamma for part in item.split(",")]

        if gamma==[]:
            if (poppedFormula!=""):
                currentFormula = poppedFormula


            if (currentFormula.find("=>")!=-1):
                gamma = currentFormula.split("=>")[0].split(",")
                delta = currentFormula.split("=>")[1]
            else:
                delta = currentFormula
            
            #Couldnt get a gamma
            if gamma==[] or gamma[0]=="":
                gamma = []
                currentFormula = currentFormula.replace("=>","")

        trackState.append(currentFormula)
        trackLog.append(f"Current formula:{currentFormula}")

        if (poppedIdx==-1):
            for i,j in enumerate(gamma):
                rulesWithScores,tracking = getRules(currentFormula,j,len(variables))

                for k in rulesWithScores:
                    pq.push(k[0],(i,k[1]))

                for _,inferenceRules in tracking.items():
                    for k,v in inferenceRules.items():
                        tempFormula = currentFormula.replace(j,k)
                        trackRules[tempFormula] = v

            if (gamma == []):
                rulesWithScores,tracking = getRules(currentFormula,delta,len(variables))

                for k in rulesWithScores:
                    pq.push(k[0],(-1,k[1]))

                for _,inferenceRules in tracking.items():
                    for k,v in inferenceRules.items():
                        tempFormula = currentFormula.replace(delta,k)
                        trackRules[tempFormula] = v

            continue
        

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
            trackState.append(resultFormula)
            trackLog.append(f"Eliminated {var} in {j} yielding {resultFormula}")


            currentFormula = resultFormula


        if appliedAck:
            pq.clear()
            for i,j in enumerate(gamma):
                rulesWithScores,tracking = getRules(currentFormula,j,len(variables))

                for k in rulesWithScores:
                    pq.push(k[0],(i,k[1]))
                
                for _,inferenceRules in tracking.items():
                    for k,v in inferenceRules.items():
                        tempFormula = currentFormula.replace(j,k)
                        trackRules[tempFormula] = v
            
            # Case when all the deltas are eliminated. We need to apply rules to the delta now.
            # The rules applied will probably be the nominal introductions ones
            if (gamma == []):
                rulesWithScores,tracking = getRules(currentFormula,delta,len(variables))

                for k in rulesWithScores:
                    pq.push(k[0],(-1,k[1]))

                for _,inferenceRules in tracking.items():
                    for k,v in inferenceRules.items():
                        tempFormula = currentFormula.replace(delta,k)
                        trackRules[tempFormula] = v

    #Filter to only have the rules that leads to the solution
    trackRules = {k:v for k,v in trackRules.items() if k in trackState}

    return trackState,trackLog,trackRules
    
