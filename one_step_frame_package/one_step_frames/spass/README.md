# SPASS

## Overview
The program automatically finds(if possible) a proof for the implication in the paper. It uses v3.9 of [SPASS](https://www.mpi-inf.mpg.de/departments/automation-of-logic/software/spass-workbench/classic-spass-theorem-prover/download/) as a tool.

The ```main.py``` python does the following:
- Load the arguments from ```args.txt```
- load config info from ```config.json```(initializes a config.json if not found)
- Automatically create the ```.dfg``` file for SPASS. This is named ```spass_output/spass.dfg```
- Outputs the console output, and writes to ```spass_output/output.txt```.
- Errors are written to ```spass_output/errors.txt```

## Arguments
The ```args.txt``` file is formatted as follows:
- lines with % are intrepreted as comments
- 2 arguments are required(one for the first order condtion, and one for the S).These are seperated by a new line.

## Example
An example of a valid ```.dfg``` is given in the ```example``` folder.
