from util.formula import findAtomicFormulas, getConnectives


def checkNominal(nominal:str)->bool:
    return True


def sequentRules(rule:str):
    pass


def nominalRules(rule:str):
    # phi + psi
    psi0,psi1 = None,None
    split = rule.split("<")
    phi = split[0]
    conclusion = split[1]
    connectives = getConnectives(conclusion)
    subformulas = findAtomicFormulas(conclusion)
    
    #if x<y, then y is length 1/2 if valid
    lengthOne = None

    if (len(subformulas)==1):
        psi0 = subformulas[0]
        lengthOne=True
    elif (len(subformulas)==2):
        psi0 = subformulas[0]
        psi1 = subformulas[1]
        lengthOne=False
    else:
        #TODO ERROR HANDLE
        pass
    
    if lengthOne and psi0 not in ["0","1"]:
        if phi + "<" + psi0 == rule:
            return f"V(u)(u<{phi}->u<{psi0})"
    elif lengthOne:
        if psi0=="1":
            return "1"
        elif psi0=="0":
            return "0"
    
    pass


def adjunctionRules(rule:str):
    psi0,psi1 = None,None
    split = rule.split("<")
    phi = split[0]
    conclusion = split[1]
    connectives = getConnectives(conclusion)
    subformulas = findAtomicFormulas(conclusion)

    print(subformulas)

    pass


def ackermannRules(rule:str):
    pass
