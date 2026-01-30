import re
from typing import List, Optional

VARIABLE_PATTERN = r"[a-hj-tx-z](?:_\d+)?"
NOMINAL_PATTERN = r"\b[uwv](?:_\d+)?\b|i\(\b[uwv](?:_\d+)?\b\)"


def findVariables(formula:str):
    """Find all variables in a given formula.
    Args:
        formula (str): The formula to search for variables.
    Returns:
        set: A set of variables found in the formula.
    """
    # Matches single lowercase letters that are not 'u', 'v', 'w', or 'i'
    matches = re.findall(VARIABLE_PATTERN, formula)
    variables = set(matches)
    return variables


def findNominals(string:str):
    matches = re.findall(NOMINAL_PATTERN, string)
    nominals = set(matches)
    return nominals


def checkNominal(string:str):
    # return bool(re.fullmatch(r"\b[uwv](?:_\d+)?\b",string))
    return bool(re.fullmatch(NOMINAL_PATTERN,string))


def checkPolarity(formula:str,variable:str,op:str="<")->bool|None:
    """Check the polarity of a variable in a formula.

    Args:
        formula (str): The formula to check.
        variable (str): The variable to check the polarity of.

    Returns:
        None|bool: Returns true if polarity is positive, false if negative, 
        and None if the variable is not found/not valid.
    """
    
    if variable not in findVariables(formula):
        return None
    
    # find ~variable and varaible
    pos_pattern = rf'(?<!~){variable}\b'
    neg_pattern = rf'~{variable}\b'
    pos_matches = re.findall(pos_pattern, formula)
    neg_matches = re.findall(neg_pattern, formula)
    all_matches = pos_matches + neg_matches

    if len(all_matches)==1:
        if len(pos_matches)>0:
            return True
        else:
            return False
    else:
        return None


class SQEMARules:
    """Collection of adjunction inference rules."""
    
    @staticmethod
    def rule_1(phi: str, psi: str, operator:str) -> Optional[str]:
        if operator=="=>" and phi.strip()=="":
            return f"~({psi})=>"
        else:
            return None
    
    @staticmethod
    def rule_2(phi: str, psi: str,operator:str) -> Optional[str]:
        if operator!="=>" and psi.strip()!="" and phi.strip()[0]=="~":
            return None
        
        insides = re.findall(r"^~?\((.*)\)$",phi)

        #TODO generalize the regex pattern
        PATTERN = "^#p_1(?:\^(?:#)?\([^()]*\|[^()]*\))*$"
        PATTERN1 = "\~?p_\d+\|\~?p_\d+|(?:~?[a-zA-Z_]\w*)|\(~?p_\d+(?:\|~?p_\d+)+\)\|~?p_\d+"

        substrings =re.findall(PATTERN1,insides[0])


        output = ""

        if (len(substrings)==0):
            return None
        

        for i,j in enumerate(substrings):
            if i==0:
                if j[0]=="~":
                    output+=f"{j[1:]}^"
                else:
                    output+="@~"+j+"^"
                continue

            if j.count("|")==1:
                args = j.split("|")
                first_arg, second_arg = args[0], args[1]
                temp = ""

                if first_arg[0]=="~":
                    temp+=f"{first_arg[1:]}^"
                else:
                    temp+=f"~{first_arg}^"

                if second_arg[0]=="~":
                    temp+=f"{second_arg[1:]}"
                else:
                    temp+=f"~{second_arg}"

                output+= f"@({temp})^"
            else:
                # j.count("|")>1
                args = j.rsplit("|",1)
                first_arg, second_arg = args[0], args[1]
                temp = ""

                # #((~p_1|~p_2)|p_3))
                s_inner = first_arg[1:-1] if first_arg.startswith("(") and first_arg.endswith(")") else first_arg

                premises = re.match(r"~?p_\d+(?:\|~?p_\d+)+",s_inner)[0]
                premises = premises.split("|")

                for premise in premises:
                    if premise[0]=="~":
                        temp+=f"{premise[1:]}^"
                    else:
                        temp+=f"~{premise}^"
                
                temp = f"({temp[:-1]})^"  # Remove last ^

                if second_arg[0]=="~":
                    temp+=f"{second_arg[1:]}"
                else:
                    temp+=f"~{second_arg}"

                
                output += f"@({temp})^"
        
        return output[:-1]+operator           
    
    @staticmethod
    def rule_3(phi: str, psi: str,operator:str) -> Optional[str]:
        formula = phi+operator+psi
        variables = findVariables(formula)

        polarities = zip(variables, [checkPolarity(formula, var, op=operator) for var in variables])

        formulae = []
        for i,j in polarities:
            if j is False:
                formula = formula.replace(i,"0")
                formulae.append(formula)
        
        if len(formulae)==0:
            return None
        else:
            return formulae

    @staticmethod
    def rule_4(phi: str, psi: str,operator:str) -> Optional[str]:
        formula = phi+operator+psi

        formulae = []

        for _ in range(formula.count("~0")):
            formula = formula.replace("~0","1",1)
            formulae.append(formula)

        if len(formulae)==0:
            return None
        else:
            return formulae
    
    @staticmethod
    def rule_5(phi: str, psi: str,operator:str) -> Optional[str]:
        formula = phi+operator+psi

        #find all strings like x ^ 1 or 1 ^ x where x can be any string
        pattern = r'(\b1\b\^|\^\b1\b)'
        matches = re.findall(pattern, formula)
        formulae = []
        for _ in matches:
            formula = re.sub(pattern, '', formula, count=1)
            formulae.append(formula)

        if len(formulae)==0:
            return None
        else:
            return formulae
        
    
    @staticmethod
    def rule_6(phi: str, psi: str,operator:str) -> Optional[str]:
        nominals = findNominals(phi)
        
        if len(nominals)==0 or checkNominal(phi) is False or psi.find("^")==0:
            return None
        
        formulae = psi.split("^")
        return ",".join([f"{phi}{operator}{part}" for part in formulae])

        
def _extract_antecedent(result: str | list | None, operator: str) -> str | None:
    """Extract the antecedent from a rule result for chaining.
    
    Handles list results by taking the first element, and returns
    the portion before the operator for the next rule application.
    
    Args:
        result: The output from a rule (str, list, or None)
        operator: The operator separating antecedent and consequent
    
    Returns:
        The antecedent portion or None if result is None
    """
    if result is None:
        return None
    # If result is a list, take the first element
    if isinstance(result, list):
        result = result[0]
    # Extract the antecedent (portion before the operator)
    return result.split(operator)[0]


def pipeline(rule: str) -> Optional[str]:
    """Apply SQEMA rules in sequence to transform a formula.
    
    Args:
        rule: The initial formula to transform
    
    Returns:
        The final transformed formula or None if transformation fails
    """
    # Rule 1: Add negation and implication
    res = SQEMARules.rule_1("", rule, "=>")
    
    # Rule 2: Handle complex premise transformations
    res = SQEMARules.rule_2(_extract_antecedent(res, "=>"), "", "=>")
    
    # Rule 3: Substitute 0 for negative polarity variables
    res = SQEMARules.rule_3(_extract_antecedent(res, "=>"), "", "=>")
    res = _extract_antecedent(res, "=>")
    
    # Rule 4: Replace ~0 with 1
    res = SQEMARules.rule_4(res, "", "=>")
    res = _extract_antecedent(res, "=>")
    
    # Rule 5: Remove 1 from conjunctions/disjunctions
    res = SQEMARules.rule_5(res, "", "=>")
    res = _extract_antecedent(res, "=>")
    
    # Prepare for rule 6 by adding nominal
    res = f"w_0<{res}"
    
    # Rule 6: Handle nominal splitting
    antecedent, consequent = res.split("<")
    res = SQEMARules.rule_6(antecedent, consequent, "<")
    
    return res+"=>"



if __name__ == "__main__":
    # res = SQEMARules.rule_1("","#p_1^#(~p_1|p_2)^#((~p_1|~p_2)|p_3)","=>")
    res = pipeline("#p_1^#(~p_1|p_2)")
    res = pipeline("#p_1^#(~p_1|p_2)^#((~p_1|~p_2)|p_3)")
    # res = SQEMARules.rule_1("","#p_1^#(~p_1|p_2)","=>")
    # print(res)





