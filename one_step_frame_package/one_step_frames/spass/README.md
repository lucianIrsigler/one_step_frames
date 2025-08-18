# SPASS

## Overview
The program automatically finds(if possible) a proof for the implication in the paper. It uses v3.9 of [SPASS](https://www.mpi-inf.mpg.de/departments/automation-of-logic/software/spass-workbench/classic-spass-theorem-prover/download/) as a tool.

The ```spass.py``` python does the following:
- Takes in two arguments(the first order conditon and S).
- Loads the default config, or uses a user-supplied config.
- Automatically create the ```.dfg``` file for SPASS. This is named ```spass_output/spass.dfg```
- Outputs the console output, and writes to ```spass_output/output.txt```.
- Errors are written to ```spass_output/errors.txt```

## Config
SPASS() takes in an optional ```config``` option. The config looks as follows:
- ```problemName```: Name of the problem SPASS is solving. Defaulted to ```StepFrames```.
- ```name```:Name of the problem for list_of_descriptions. Defaulted to ```{*StepFrames*}```.
- ```author```:Author of the file. Defaulted to ```{*Author*}```.
- ```description```:Description of the problem. Defaulted to ```{*Output of SPASS python file*}```.

## Loading SPASS
In order to actually use SPASS, the binaries/code must be stored in a folder called ```spass39``` on the same level as the python script calling SPASS. The code effectively looks for the executable ```spass39/SPASS```. If this executable is not found, then the code will not execute succesfully.

As an example, the file structure must look as follows:

```
project
│   main.py(file that calls SPASS)
└───spass39
│   │   SPASS
│   │   ...all the other .c and .h files
```

## Output
The output of the program are the following files:
- ```spass_output/output.txt```: The proof derived from SPASS.
- ```spass_output/error.txt```: Any errors from the procedure are written here. Includes syntax error.
- ```spass_output/spass.dfg```: The SPASS file that SPASS is actually ran on.
