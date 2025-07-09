from AST.core.abstract_syntax_tree import Node


def getLeafNodes(node:Node,parent=None,result=None):
    if result is None:
        result = []

    if node is None:
        return result
    
    if node.arity==2:
        if (node.left!=None):
            getLeafNodes(node.left,node,result)
        if (node.right!=None):
            getLeafNodes(node.right,node,result)
    else:
        if node.child!=None:
            getLeafNodes(node.child,node,result)
        else:
            result.append((node,parent))

    return result


def getSpecificNodes(node:Node,searchValue:str="",result=None,):
    if result is None:
        result = []

    if node is None:
        return result
    
    if (node.value==searchValue):
        result.append(node)

    if node.arity==2:
        if (node.left!=None):
            getSpecificNodes(node.left,searchValue,result)
        if (node.right!=None):
            getSpecificNodes(node.right,searchValue,result)

    else:
        if node.child!=None:
            getSpecificNodes(node.child,searchValue,result)

    return result


def toInfix(node) -> str:
    """Reconstruct the infix formula string from the AST with proper parentheses for specific unary operators."""
    if node is None:
        return ""

    if node.arity == 0:
        return str(node.value)

    elif node.arity == 1:
        child_expr = toInfix(node.child)
        # Only add parentheses for i, i*, and i! operators
        if node.value in ["i", "i*", "i!"]:
            return f"{node.value}({child_expr})"
        else:
            return f"{node.value}{child_expr}"

    elif node.arity == 2:
        left_expr = toInfix(node.left)
        right_expr = toInfix(node.right)
        return f"{left_expr}{node.value}{right_expr}"

    else:
        raise ValueError(f"Unsupported arity: {node.arity}")