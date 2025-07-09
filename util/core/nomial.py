import re


class Nominal:
    def __init__(self):
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

    def __str__(self):
        return f"Nominal(nominal_dict={self.nominal_dict})"


def checkNominal(string:str):
    return bool(re.fullmatch(r"^[uvw]_\d+$",string))