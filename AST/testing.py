from  abstract_operator import AbstractOperator
from  abstract_syntax_tree import AbstractSyntaxTree

#TODO UPDATE
operators = [
    # perf 2
    AbstractOperator("=>",2,2),

    # perf 1
    AbstractOperator("<",2,1),
    AbstractOperator("<'",2,1),

    #perf 0
    AbstractOperator("#",1),
    AbstractOperator("#'",1),
    AbstractOperator("@",1),
    AbstractOperator("@'",1),
    AbstractOperator("~",1),
    AbstractOperator("i*",1),
    AbstractOperator("i!",1),
    AbstractOperator("i",1),

    AbstractOperator("^",2),
    AbstractOperator("&",2),
    AbstractOperator("->",2),
    AbstractOperator("<->",2),


]

# TODO : make operators default so less initialization is needed
abstractTree = AbstractSyntaxTree(operators)

# abstractTree.buildTree("i(x)=>i(y)")
# i(x) i(y) => 
formula = "#x<i(y)=>#x<#y"
# formula = "#x<y=>w_1^w_2 => #'x"
abstractTree.buildTree(formula)

abstractTree.printTree()