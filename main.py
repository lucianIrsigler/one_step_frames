from one_step_frame_package.src.one_step_frames.step_frame_conditions import findStepFrameCondition


if __name__=="__main__":
    # rule = "#x->y/#x->#y"
    # rule = "/#x->x"

    rule = input("Enter formula:")
    res = findStepFrameCondition(rule)

    for i in res[0]:
        print(i)
    print()
    for i in res[1]:
        print(i)
