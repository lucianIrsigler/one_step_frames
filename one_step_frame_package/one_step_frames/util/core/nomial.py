import re
import copy
from .regexPatterns import NOMINAL_PATTERN,NOMINAL_PATTERN_STRICT

class Nominal:
    """A class to manage nominals for modal logic."""
    def __init__(self):
        self.nominal_dict = {
            "w": {},
            "v": {},
            "u": {}
        }
    
    def reset(self):
        self.nominal_dict = {
            "w": {},
            "v": {},
            "u": {}
        }
        
    def get_nominal(self, name: str) -> str:
        """Returns a fresh nominal based on the name and value."""
        if name not in self.nominal_dict:
            raise ValueError(f"Invalid nominal name: {name}")
        
        temp_dict = self.nominal_dict[name]
        new_nom = f"{name}_{len(temp_dict)}"
        temp_dict[new_nom] = True
        return new_nom
    
    def pop_nominal(self,name:str):
        """Pops the last nominal(last generated) for a nominal string

        Args:
            name (str): nominal to pop

        Raises:
            ValueError: Invalid nominal name
        """
        if name not in self.nominal_dict:
            raise ValueError(f"Invalid nominal name: {name}")
        
        temp_dict = self.nominal_dict[name]

        if (len(temp_dict)==0):
            return
        
        pop_nom = f"{name}_{len(temp_dict)-1}"
        temp_dict.pop(pop_nom)

    def __str__(self):
        return f"Nominal(nominal_dict={self.nominal_dict})"

    def copy(self):
        """Return a deep copy of this Nominal instance."""
        new_instance = Nominal()
        new_instance.nominal_dict = copy.deepcopy(self.nominal_dict)
        return new_instance


def checkNominal(string:str):
    # return bool(re.fullmatch(r"\b[uwv](?:_\d+)?\b",string))
    return bool(re.fullmatch(NOMINAL_PATTERN,string))


def getNominals(string:str):
    matches = re.findall(NOMINAL_PATTERN, string)
    return matches

def getNominalsStrictly(string:str):
    matches = re.findall(NOMINAL_PATTERN_STRICT, string)
    return matches