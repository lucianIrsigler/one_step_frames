from .nomial import Nominal,getNominals
from .translate_util import replaceNominals,cleanUp
from .text_functions import checkOperand,replaceCharacters,operatorTranslations,checkNominal
from .regexPatterns import NOMINAL_PATTERN
import re

nominalManager = Nominal()

#Take it like this, if #xy, then put symbol as "#", and "xy" as formula
def translateSymbol(symbol:str,formula:str,lastVariable:str)->tuple[str,str]:
    """Translate a symbol into its corresponding translation based on the operatorTranslations dictionary.
    If the symbol is an operand, it will use the "u" translation. If the symbol is not found 
    in the dictionary, it will raise a KeyError. 


    Args:
        symbol (str): symbol to translate
        formula (str): the rest of the formula after the symbol

    Raises:
        KeyError: If the symbol is not found in the operatorTranslations dictionary and is not an operand.

    Returns:
        str: The translated symbol, which may include variables and the rest of the formula.
    """
    
    # If not operator or operand
    if symbol not in operatorTranslations.keys() \
        and not checkOperand(symbol) \
        and not checkNominal(symbol):
        raise KeyError("Key not found:",symbol)
    
    isOperand = checkOperand(symbol)

    temp = operatorTranslations["u"] if isOperand else operatorTranslations[symbol]
    
    if "x" not in temp or "y" not in temp:
        temp = temp.replace("z","{"+f"{formula}"+"}")
        return temp,lastVariable
    

    nextVariable = ""

    if lastVariable=="":
        #First time doing this
        tempFormula = replaceNominals(symbol + formula,reverse=True)
        nominalsInForm = getNominals(tempFormula)

        #TODO make dynamic?
        if ("w_0" in nominalsInForm):
            lastVariable = nominalManager.get_nominal("w")
            nextVariable = nominalManager.get_nominal("w")
    elif "w" in lastVariable or "v" in lastVariable:
        if isOperand:
            nextVariable = replaceNominals(symbol, reverse=True)
        else:
            next_nominal = "v" if "w" in lastVariable else "w"
            nextVariable = nominalManager.get_nominal(next_nominal)


    temp = temp.replace("x",lastVariable)
    temp = temp.replace("y",nextVariable)
    temp = temp.replace("z","{"+f"{formula}"+"}")
    lastVariable = nextVariable

    return temp,lastVariable


def find_all_indices(main_string, substring):
    indices = []
    start_index = 0
    while True:
        try:
            # Find the next occurrence starting from start_index
            index = main_string.index(substring, start_index)
            indices.append(index)
            # Update start_index to search from the position right after the found occurrence
            start_index = index + 1
        except ValueError:
            # If the substring is not found, a ValueError is raised, breaking the loop
            break
    return indices


def translateCondition(formula:str, ruleOrder:dict[str,str])->str:
    """Translate a formula into a one-step condition by replacing nominals and 
    characters with their corresponding translations. It works by iterating through the
    formula, translating each symbol, and building a base translation. It also handles
    nested translations by storing them in a dictionary and replacing them in the base translation.
    Lastly, some rules add universal quantification(the nominal rules), thus as the last step, the algorithm
    checks for any global nominals using the ruleOrder dict, and applies the corresponding quantification.

    Args:
        formula (str): The formula to translate, which may contain nominals and characters.
        ruleOrder (dict[str,str]): Holds the rules order and the rule applied at that step

    Returns:
        str: The translated formula as a one-step condition, with nominals and 
        characters replaced by their translations.
    """
    nominalManager.reset()

    formula = replaceCharacters(formula)

    #match nominals first
    nominals = re.findall(NOMINAL_PATTERN,formula)
    indices = {}

    for i in set(nominals):
        indices[i] = find_all_indices(formula,i)
        formula = formula.replace(i,"")

    symbols = list(formula)

    for i,j in indices.items():
        for k in j:
            symbols.insert(k,i)
    
    runningTranslations = {}

    lastTranslation = None
    base = ""

    lastVariable = ""

    for i,j in enumerate(symbols):
        translation,lastVariable = translateSymbol(j,formula[i+1:],lastVariable)

        if lastTranslation!=None:
            key = "{"+lastTranslation+"}"
            runningTranslations[key] = translation
        else:
            base = translation

        lastTranslation = formula[i+1:]

    
    for k,v in runningTranslations.items():
        base = base.replace(k,v)
    
    base = cleanUp(base)

    # When some nominal rules are applied, they add a quantifer to the whole expression. This checks that
    globalNominals = []
    for i,j in ruleOrder.items():
        if j=="N1":
            nominal = i.split("<",1)[0]
            globalNominals.append(f"F({nominal})")
        #TODO add other cases

    for i in globalNominals:
        base = f"{i}({base})"

    return base


# if __name__ == "__main__":
#     formula = "w_0<#*#@'w_0"
#     # formula = "w_0<i@'w_0"
#     # formula = "w_0<#@'i@'w_0"
#     res = translateCondition(formula)
#     print(res)
