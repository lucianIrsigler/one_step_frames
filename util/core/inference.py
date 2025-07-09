from util.rules.inference_rules import inferenceRules

if __name__=="__main__":
    formulae = [
        "#x<i(y)=>#x<#y",
        "i*(#x)<y=>#x<#y",
        "#x<#i*(#x)",
        "w<#x=>w<#i*(#x)",
        "@'w<x=>w<#i*(#x)",
    ]

    for formula in formulae:
        inferenceRules(formula)