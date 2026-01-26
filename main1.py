from one_step_frame_package.one_step_frames.step_frame_conditions import getLogs,findStepFrameCondition,translateCondition,simplifyConditon
import time
import csv
from one_step_frame_package.one_step_frames.spass.parser import create_SPASS_input
from one_step_frame_package.one_step_frames.testing.core.tests import runTests


def main():
    # assert(runTests(getLogs)==True)
    
    testForm = "/#(p->p_1)->(#p->#p_1|#p_2|#p_3)"
    # testForm = "/#p_1|#(p_1->p_2)"
    # res = findStepFrameCondition(testForm)
    res = translateCondition("w_0<@'w_1=>w_0<T",{})
    res = simplifyConditon(res)
    print(res)
    

if __name__=="__main__":
    main()

# def runTimingTests():
#     boxes_lst = []
#     single_diamond_and_boxes_lst = []
#     diamonds_and_boxes_lst = []


#     for i in range(10,240,10):
#         print(f"Running ({i},{i}) on repeated boxes")
#         totalBoxes = i*2

#         form = generalTesting.repeated_boxes(i,i)

#         start_time = time.perf_counter()
#         algSol = getLogs(form)[0][-1]
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         sol = generalTesting.repeated_boxes_solution(i,i)

#         assert(algSol==sol)

#         boxes_lst.append([totalBoxes,elapsed_time])

#         print(f"Running ({i},{i}) on repeated boxes and single diamond")

#         totalSingleDiamondAndRepeatedBoxes = i*2+2

#         form = generalTesting.single_diamond_repeated_boxes(i,i)

#         start_time = time.perf_counter()
#         algSol = getLogs(form)[0][-1]
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         sol = generalTesting.single_diamond_repeated_boxes_solution(i,i)

#         assert(algSol==sol)

#         single_diamond_and_boxes_lst.append([totalSingleDiamondAndRepeatedBoxes,elapsed_time])
    

#     for i in range(10,160,10):
#         print(f"Running ({i},{i},{i},{i}) on repeated boxes and diamonds")

#         totalOperators = i*4

#         form = generalTesting.repeated_diamonds_and_boxes(i,i,i,i)

#         start_time = time.perf_counter()
#         algSol = getLogs(form)[0][-1]
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         sol = generalTesting.repeated_diamonds_and_boxes_solution(i,i,i,i)


#         gammaAlgoritm = sorted(algSol.split("=>")[0].split(","))
#         deltaAlgorithm = algSol.split("=>")[1]
#         algStringRecon = f"{"".join(gammaAlgoritm)}=>{deltaAlgorithm}"

#         gammaSol = sorted(sol.split("=>")[0].split(","))
#         deltaSol = sol.split("=>")[1]
#         solStringRecon = f"{"".join(gammaSol)}=>{deltaSol}"

#         assert(algStringRecon==solStringRecon)
        
#         diamonds_and_boxes_lst.append([totalOperators,elapsed_time])
    

#     print("REPEATED BOXES OUTPUT")
#     for i in boxes_lst:
#         print(i)
    

#     print("REPEATED BOXES AND SINGLE DIAMOND OUTPUT")
#     for i in single_diamond_and_boxes_lst:
#         print(i)

    
#     print("REPEATED BOXES AND REPEATED DIAMONDS OUTPUT")
#     for i in diamonds_and_boxes_lst:
#         print(i)

    
#     with open("repeated_boxes.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "ms"])
#         writer.writerows(boxes_lst)
    

#     with open("repeated_boxes_single_diamond.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "ms"])
#         writer.writerows(single_diamond_and_boxes_lst)
    

#     with open("repeated_boxes_repeated_diamonds.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "ms"])
#         writer.writerows(diamonds_and_boxes_lst)


# def runExpansionTests():
#     boxes_lst = []
#     single_diamond_and_boxes_lst = []
#     diamonds_and_boxes_lst = []


#     for i in range(10,240,10):
#         print(f"Running ({i},{i}) on repeated boxes")
#         totalBoxes = i*2

#         form = generalTesting.repeated_boxes(i,i)
#         output = getLogs(form)
#         algSol = output[0][-1]
#         sol = generalTesting.repeated_boxes_solution(i,i)

#         boxes_lst.append([totalBoxes,len(output[0]),output[3]])

#         print(f"Running ({i},{i}) on repeated boxes and single diamond")

#         totalSingleDiamondAndRepeatedBoxes = i*2+2

#         form = generalTesting.single_diamond_repeated_boxes(i,i)
#         output = getLogs(form)
#         algSol = output[0][-1]
#         sol = generalTesting.single_diamond_repeated_boxes_solution(i,i)

#         assert(algSol==sol)

#         single_diamond_and_boxes_lst.append([totalSingleDiamondAndRepeatedBoxes,len(output[0]),output[3]])
    

#     for i in range(10,160,10):
#         print(f"Running ({i},{i},{i},{i}) on repeated boxes and diamonds")

#         totalOperators = i*4

#         form = generalTesting.repeated_diamonds_and_boxes(i,i,i,i)
#         output = getLogs(form)
#         algSol = output[0][-1]
#         sol = generalTesting.repeated_diamonds_and_boxes_solution(i,i,i,i)


#         gammaAlgoritm = sorted(algSol.split("=>")[0].split(","))
#         deltaAlgorithm = algSol.split("=>")[1]
#         algStringRecon = f"{"".join(gammaAlgoritm)}=>{deltaAlgorithm}"

#         gammaSol = sorted(sol.split("=>")[0].split(","))
#         deltaSol = sol.split("=>")[1]
#         solStringRecon = f"{"".join(gammaSol)}=>{deltaSol}"

#         assert(algStringRecon==solStringRecon)
        
#         diamonds_and_boxes_lst.append([totalOperators,len(output[0]),output[3]])
    

#     print("REPEATED BOXES OUTPUT")
#     for i in boxes_lst:
#         print(i)
    

#     print("REPEATED BOXES AND SINGLE DIAMOND OUTPUT")
#     for i in single_diamond_and_boxes_lst:
#         print(i)

    
#     print("REPEATED BOXES AND REPEATED DIAMONDS OUTPUT")
#     for i in diamonds_and_boxes_lst:
#         print(i)

    
#     with open("repeated_boxes_nodes.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "nodes_expanded","nodes_added"])
#         writer.writerows(boxes_lst)
    

#     with open("repeated_boxes_single_diamond_nodes.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "nodes_expanded","nodes_added"])
#         writer.writerows(single_diamond_and_boxes_lst)
    

#     with open("repeated_boxes_repeated_diamonds_nodes.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["totalOperators", "nodes_expanded","nodes_added"])
#         writer.writerows(diamonds_and_boxes_lst)


# if __name__ == "__main__":
#     condi = findStepFrameCondition(generalTesting.repeated_diamonds_and_boxes(2,2,2,2))
#     # condi = findStepFrameCondition("#x->y/#x->#y")

#     print(condi)