from . import general as testing
from random import randint
from typing import Callable

#Pass in getLogs
def runTests(algorithm:Callable[..., object]):
    for i in testing.generatePaperTests():
        output = algorithm(i[0])[0][-1]
        solution = i[1]
        assert(output==solution)

    print("Test paper formulae passed")

    for i in testing.edgeCases():
        output = algorithm(i[0])[0][-1]
        solution = i[1]
        assert(output==solution)
    
    print("Edge cases passed")

    tuples = [(randint(2, 15), randint(2, 15), randint(2, 15), randint(2, 15)) for _ in range(6)]

    for i in tuples:
        n,k,m,l = i
        test = testing.repeated_boxes(n,k)
        sol = testing.repeated_boxes_solution(n,k)
        algSol = algorithm(test)[0][-1]
        assert(algSol==sol)

        test = testing.single_diamond_repeated_boxes(n,k)
        sol = testing.single_diamond_repeated_boxes_solution(n,k)
        algSol = algorithm(test)[0][-1]
        assert(sol==algSol)


        test = testing.repeated_diamonds_and_boxes(n,k,m,l)
        sol = testing.repeated_diamonds_and_boxes_solution(n,k,m,l)
        algSol = algorithm(test)[0][-1]

        # In this case, gamma might be in different order, but it is the same.
        #  So we just sort before checking
        gammaAlgoritm = sorted(algSol.split("=>")[0].split(","))
        deltaAlgorithm = algSol.split("=>")[1]
        algStringRecon = f"{"".join(gammaAlgoritm)}=>{deltaAlgorithm}"

        gammaSol = sorted(sol.split("=>")[0].split(","))
        deltaSol = sol.split("=>")[1]
        solStringRecon = f"{"".join(gammaSol)}=>{deltaSol}"

        assert(algStringRecon==solStringRecon)

    
    print("PASSED ALL")


#Pass in getLogs
def testAlgorithmExpansion(algorithm:Callable[..., object],verbose:bool=False):
    file = "expansion.log"

    import logging

    logging.basicConfig(
        filename=file,        # file name
        filemode="w",              # overwrite ("a" = append)
        level=logging.INFO,       # capture everything
        format="%(message)s"
    )

    tuples = [(randint(2, 30), randint(2, 30), randint(2, 30), randint(2, 30)) for _ in range(10)]

    for i in tuples:
        n,k,m,l = i
        test = testing.repeated_boxes(n,k)
        minimum_nodes = testing.minimum_rules_repeated_boxes(n,k)
        algSol = algorithm(test)
        logging.info(
            f"REPEATED BOXES [n={n}, k={k}]\n"
            f"Nodes expanded: {len(algSol[0])}\n"
            f"Nodes added: {algSol[3]}\n"
            f"Minimum required: {minimum_nodes}\n"
        )

        test = testing.single_diamond_repeated_boxes(n,k)
        minimum_nodes = testing.minimum_rules_single_diamond_repeated_boxes(n,k)
        algSol = algorithm(test)
        logging.info(
            f"REPEATED BOXES AND SINGLE DIAMOND [n={n}, k={k}]\n"
            f"Nodes expanded: {len(algSol[0])}\n"
            f"Nodes added: {algSol[3]}\n"
            f"Minimum required: {minimum_nodes}\n"
        )



        test = testing.repeated_diamonds_and_boxes(n,k,m,l)
        minimum_nodes = testing.minimum_rules_repeated_diamond_repeated_boxes(n,k,m,l)
        algSol = algorithm(test)
        logging.info(
            f"REPEATED BOXES AND REPEATED DIAMOND [n={n}, k={k}, m={m}, l={l}]\n"
            f"Nodes expanded: {len(algSol[0])}\n"
            f"Nodes added: {algSol[3]}\n"
            f"Minimum required: {minimum_nodes}\n"
        )

    
    if verbose:
        with open(file,"r") as f:
            data = f.readlines()
        
        for i in data:
            print(i,"")
    else:
        print("Finished testing")

