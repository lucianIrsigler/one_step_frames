import re
from typing import List, Optional
from one_step_frames.util.rules.ackermann_rules import findNominals, findVariables
from one_step_frames.util.core.nomial import checkNominal
from one_step_frames.AST.core.abstract_syntax_tree import AbstractSyntaxTree


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


class AltNRules:
    """Collection of adjunction inference rules."""
    
    @staticmethod
    def rule_1(phi: str, psi: str, operator:str,isDelta:bool=False) -> Optional[str]:
        if phi.strip()=="" and isDelta is True:
            return f"~({psi})=>"
        else:
            return None
    
    @staticmethod
    def rule_2(phi: str, psi: str,operator:str) -> Optional[str]:
        #TODO BREAK FOR n=2
        if operator!="=>" and psi.strip()!="":
            return None
        
        if phi[0:2]!="~(":
            return None
        
        insides = re.findall(r"^~?\((.*)\)$",phi)
        
        ast = AbstractSyntaxTree()
        ast.buildTree(phi)
        # ast.printTree()

        #TODO generalize the regex pattern
        PATTERN1 = r"\~?p_\d+\|\~?p_\d+|(?:~?[a-zA-Z_]\w*)|\(~?p_\d+(?:\|~?p_\d+)+\)\|~?p_\d+"
        
        #TODO broken. Used AST. where you find ^, instead check to see if any parent has
        # like a modal operator. If does, then it is not indepdentent subformula/conjunction
        # substrings =re.findall(PATTERN1,insides[0])
        
        right_splits = insides[0].rsplit("^#",1)
        right_splits_processed = []
        for i in right_splits:
            if i.count("(")<=1:
                right_splits_processed.append(i)
                continue
            if i[0]=="(" and i[-1]==")" :
                i = i[1:-1]
            elif i[0]=="(" and i[-1]!=")":
                i = i[1:]
            elif i[0]!="(" and i[-1]==")":
                i = i[:-1]
            right_splits_processed.append(i)

        temp_str = "^#".join(right_splits_processed)
        substrings = temp_str.split("^#")
        substrings[0] = substrings[0][1:] if substrings[0].startswith("#") else substrings[0]

        output = ""

        if (len(substrings)==0):
            return None
        

        for i,j in enumerate(substrings):
            if i==0 or j.count("|")==0:
                if j[0]=="~":
                    output+=f"{j[1:]}^"
                else:
                    output+="@~"+j+"^"
                continue

            if j.count("|")==1:
                j = j.replace("(","").replace(")","")
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
                j = j.replace("(","").replace(")","")

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
        formula = phi
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

        ast = AbstractSyntaxTree()
        ast.buildTree(psi)
        # ast.printTree()
        
        if len(nominals)==0 or checkNominal(phi) is False or psi.find("^")==0:
            return None
        
        PATTERN = r"@~?p_\d+|@\((?:[^()]+|\([^()]*\))*\)"

        # formulae = re.findall(PATTERN, psi)
        formulae = psi.split("^@")
        if not formulae:
            return None
        
        for i in range(len(formulae)):
            if i==0:
                continue
            if not formulae[i].startswith("@"):
                formulae[i] = "@" + formulae[i]
        
        return ",".join([f"{phi}{operator}{part}" for part in formulae])
    

    @staticmethod
    def rule_7(phi: str, psi: str,operator:str="=>") -> Optional[str]:
        PATTERN = r"@~?p_\d+|@\((?:[^()]+|\([^()]*\))*\)"

        formulae = [i for i in re.findall(PATTERN, phi) if "^" in i]

        if (len(formulae)==0) and len(phi.split(","))==2:
            output_string = phi.split(",")[0]
            target = phi.split(",")[1]
            var = list(findVariables(target))

            output_string+=f",w_0<@v_0,v_0<{var[0]}"
            return output_string

        output_string = phi.split(",")[0]

        for i,j in enumerate(formulae):
            outputs = []
            v = f"v_{i}"
            outputs.append(f"w_0<@{v}")
            PATTERN = r"~?p_\d+"
            literals = re.findall(PATTERN,j)

            for k in literals:
                outputs.append(f"{v}<{k}")
            
            temp_str = ",".join(outputs)

            output_string+=f",{temp_str}"
        
        return output_string
    

    @staticmethod
    def rule_8(phi: str, psi: str,operator:str="=>") -> Optional[str]:
        variables = findVariables(phi)
        output_str = phi

        for i in variables:
            target = i
            PATTERN = rf"\b\w+<{target}\b"
            matches = re.findall(PATTERN,phi)

            if len(matches)<=1:
                continue
            
            temp_str = ""
            for j in matches:
                output_str = output_str.replace(f",{j}","")
                temp_str+=f"{j.split("<")[0]}|"
            
            temp_str = f",{temp_str[:-1]}<{target}"
            output_str+=temp_str

        return output_str



def set_ant_and_cons(rule:str,isDelta:bool)->tuple[str,str]:
    if "=>" in rule:
        antecedent, consequent = rule.split("=>", 1)
    else:
        if isDelta:
            antecedent = ""
            consequent = rule
        else:
            antecedent = rule
            consequent = ""
    
    return antecedent, consequent


def _apply_rule_1(rule: str, outputs: list,isDelta:bool=False) -> None:
    """Apply rule 1: Add negation wrapper if needed."""
    try:
        if not rule or rule[0] == "~" or "=>" in rule:
            return
        
        res = AltNRules.rule_1("", rule, "=>",isDelta)
        if res is not None:
            outputs.append(res)
    except (IndexError, Exception) as e:
        pass
        # print(f"Warning in rule 1: {e}")


def _apply_rule_2(rule: str, outputs: list,isDelta:bool) -> None:
    """Apply rule 2: Handle complex premise transformations."""
    try:
        antecedent, consequent = set_ant_and_cons(rule,isDelta)
            
        res = AltNRules.rule_2(antecedent, consequent, "=>")
        if res is not None:
            outputs.append(res)
    except (ValueError, Exception) as e:
        pass
        # print(f"Warning in rule 2: {e}")


def _apply_rule_3(rule: str, outputs: list,isDelta:bool) -> None:
    """Apply rule 3: Substitute 0 for negative polarity variables."""
    try:
        antecedent, consequent = set_ant_and_cons(rule,isDelta)
        res = AltNRules.rule_3(antecedent, consequent, "=>")
        if res is not None:
            outputs.extend(res)
    except (ValueError, Exception) as e:
        pass
        # print(f"Warning in rule 3: {e}")


def _apply_rule_4(rule: str, outputs: list) -> None:
    """Apply rule 4: Replace ~0 with 1."""
    try:
        res = AltNRules.rule_4(rule, "", "")
        if res is not None:
            outputs.extend(res)
    except Exception as e:
        pass
        # print(f"Warning in rule 4: {e}")


def _apply_rule_5(rule: str, outputs: list) -> None:
    """Apply rule 5: Remove 1 from conjunctions."""
    try:
        res = AltNRules.rule_5(rule, "", "")
        if res is not None:
            outputs.extend(res)
    except Exception as e:
        pass
        # print(f"Warning in rule 5: {e}")


def _apply_rule_6(rule: str, outputs: list) -> None:
    """Apply rule 6: Handle nominal splitting."""
    try:
        if "<" not in rule:
            return
        
        parts = rule.split("<", 1)
        if len(parts) != 2:
            return
            
        antecedent, consequent = parts
        res = AltNRules.rule_6(antecedent, consequent, "<")
        if res is not None:
            outputs.append(res)
    except Exception as e:
        pass
        #print(.*)


def _apply_rule_7(rule: str, outputs: list,isDelta:bool) -> None:
    """Apply rule 7: Extract variables and create nominal bindings."""
    try:
        if findNominals(rule)==set():
            return
        
        antecedent, consequent = set_ant_and_cons(rule,isDelta)
        
        res = AltNRules.rule_7(antecedent, consequent, "")
        if res is not None:
            outputs.append(res)
    except (ValueError, Exception) as e:
        pass
        # print(f"Warning in rule 7: {e}")


def _apply_rule_8(rule: str, outputs: list,isDelta:bool) -> None:
    """Apply rule 8: Merge multiple targets."""
    try:
        if findNominals(rule)==set():
            return
        
        antecedent, consequent = set_ant_and_cons(rule,isDelta)


        res = AltNRules.rule_8(antecedent, consequent, "")
        if res is not None:
            outputs.append(res)
    except (ValueError, Exception) as e:
        pass
        # print(f"Warning in rule 8: {e}")


def _prepare_for_rule_6(rule: str, outputs: list) -> None:
    """Prepare formula for rule 6 by adding nominal."""
    try:
        antecedent, consequent = set_ant_and_cons(rule,False)
        
        #TODO remove
        if "^" not in antecedent or antecedent is None or antecedent == "":
            return
        
        if findNominals(antecedent):
            return
        
        prepared = f"w_0<{antecedent}"
        outputs.append(prepared)
    except Exception as e:
        pass
        # print(f"Warning in preparation: {e}")


def run_adapter(rule: str,isDelta:bool) -> set[str]:
    """Apply SQEMA rules in sequence to transform a formula.
    
    This function applies Alt-N rules in a specific order to transform
    propositional logic formulas into one-step frame conditions.
    
    Args:
        rule (str): The initial formula to transform.
    
    Returns:
        set[str]: A set of all generated formulas from rule applications.
    """
    if not isinstance(rule, str) or not rule.strip():
        return set()
    
    outputs = []
    
    # Apply rules in sequence
    _apply_rule_1(rule, outputs,isDelta)
    _apply_rule_2(rule, outputs,isDelta)
    _apply_rule_3(rule, outputs,isDelta)
    _apply_rule_4(rule, outputs)
    _apply_rule_5(rule, outputs)
    _prepare_for_rule_6(rule, outputs)
    _apply_rule_6(rule, outputs)
    _apply_rule_7(rule, outputs,isDelta)
    _apply_rule_8(rule, outputs,isDelta)

    outputs.remove(rule) if rule in outputs else None

    return set(outputs)


