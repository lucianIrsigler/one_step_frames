
def generatePaperTests():
    rules = (
        "#x->y/#x->#y",
        "y->#x/#y->#x",
        "/#x->x",
        "c->#p,d->#c,#p->e,#e->f/#d->#f",
        "#p->y_1,#y_1->y_2/#p->#y_2"
    )

    answers = (
        "w_0<#i*(#@'w_0)",
        "w_0<#@'i(@'w_0)",
        "w_0<i(@'w_0)",
        "w_0<#i*(#i*(#@'i(@'i(@'w_0))))",
        "w_0<#i*(#i*(#@'w_0))"
    )

    return zip(rules,answers)


def repeated_boxes(n,k):
    gamma = ""
    for i in range(n-1):
        gamma += f"x_{i+1}->#x_{i},"

    for i in range(k-1):
        gamma += f"#y_{i}->y_{i+1},"
    
    if (n==1 and k>=2):
        delta = f"#p->#y_{k-1}"
    elif (n>=2 and k==1):
        delta = f"#x_{n-1}->#p"
    else:
        delta = f"#x_{n-1}->#y_{k-1}"

    
    gamma = gamma.replace("x_0","p")
    gamma = gamma.replace("y_0","p")
    gamma = gamma.removesuffix(",")

    return gamma+"/"+delta


def repeated_boxes_solution(n,k):
    boxes = "i*(#"*(k-1)
    diamonds = "@'i("*(n-1)
    leftBrackets = ")"*(k+n-2)
    output = f"w_0<#{boxes}{diamonds}@'w_0{leftBrackets}"
    return output

def single_diamond_repeated_boxes(n,k):
    gamma = ""
    for i in range(n):
        gamma += f"x_{i+1}->#x_{i},"
    
    for i in range(k):
        gamma += f"#y_{i}->y_{i+1},"

    gamma = gamma.replace("x_0","p")
    gamma = gamma.replace("#y_0","@p")
    gamma = gamma.removesuffix(",")

    if (n==1 and k>=2):
        delta = f"@p->#y_{k-1}"
    elif (n>=2 and k==1):
        delta = f"@x_{n-1}->#p"
    else:
        delta = f"@x_{n}->#y_{k}" 

    return gamma+"/"+delta


def single_diamond_repeated_boxes_solution(n,k):
    boxes = "i*(#"*(k-1)
    diamonds = "@'i("*(n)
    leftBrackets = ")"*(k+n-1)

    output = f"w_0<@v=>w_0<#{boxes}i*(@{diamonds}v{leftBrackets})"
    return output


def repeated_diamonds_and_boxes(m,n,k,l):
    gamma = ""

    for i in range(n):
        gamma += f"x_{i+1}->#x_{i},"

    #Since range is exclusive, need to go to n+m-1 instead of n-m-2
    for i in range(n,n+m-1):
        print(i)
        gamma += f"x_{i+1}->@x_{i},"
    
    gamma = gamma.replace("x_0","p")

    pi = ""
    for i in range(l):
        pi+= f"@y_{i}->y_{i+1},"
    
    # range is exclusive at the ends, so include l+k instead of l+k-1
    for i in range(l,l+k-1):
        pi+= f"#y_{i}->y_{i+1},"

    pi = pi.replace("y_0","p")

    x_sum = m+n-1
    y_sum = l+k-1

    if (x_sum<=0 and y_sum>=0):
        delta = f"@p->#y_{y_sum}"
    elif (x_sum>=0 and y_sum<=0):
        delta = f"@x_{x_sum}->#p"
    elif (x_sum>=0 and y_sum>=0):
        delta = f"@x_{x_sum}->#y_{y_sum}"
    else:
        delta = f"@p->#p" 

    premise = gamma+pi
    premise = premise.removesuffix(",")

    return premise + "/" + delta

def repeated_diamonds_and_boxes_solution(m,n,k,l):
    pass


def generateTests(maxN, maxK, maxM=0, maxL=0, algorithm=0):
    """Generates tests for a specific algorithm.

    algorithm:
      0 → repeated boxes
      1 → single diamond + repeated boxes
      2 → repeated diamonds + boxes
    """

    if algorithm not in (0, 1, 2):
        raise IndexError("Algorithm does not exist")

    # Number of parameters per algorithm
    dims = {0: 2, 1: 2, 2: 4}[algorithm]

    # Build ranges once
    ranges = [
        range(1, maxN),
        range(1, maxK),
        range(1, maxM),
        range(1, maxL),
    ][:dims]

    # Unified tuple generation
    def cartesian_product(ranges):
        if len(ranges) == 2:
            return [(i, j) for i in ranges[0] for j in ranges[1]]
        elif len(ranges) == 4:
            return [(i, j, k, l)
                    for i in ranges[0]
                    for j in ranges[1]
                    for k in ranges[2]
                    for l in ranges[3]]

    pairs = cartesian_product(ranges)

    # Sorting by sum
    sorted_pairs = sorted(pairs, key=lambda x: sum(x))

    # Table-driven algorithm selection
    builders = {
        0: (repeated_boxes, repeated_boxes_solution),
        1: (single_diamond_repeated_boxes, single_diamond_repeated_boxes_solution),
        2: (repeated_diamonds_and_boxes, repeated_diamonds_and_boxes_solution),
    }

    build_form, build_solution = builders[algorithm]

    output = []

    for params in sorted_pairs:

        # Skip (1,1,...,1)
        if sum(params) == len(params):
            continue

        form = build_form(*params)
        solution = build_solution(*params)
        output.append((form, solution))

    return output, sorted_pairs
