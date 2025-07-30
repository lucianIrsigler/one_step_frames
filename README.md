# Logic research
The research was tasked to implement the algorithms for this [paper](https://www.sciencedirect.com/science/article/pii/S0168007214000785?via%3Dihub). 

I was required to implement 2 algorithms. The first algorithm is packaged into ```one_step_frame_package```, and the second one is ```spass_python```.

## one_step_frame_package
### Overview
This algorithm solves the problem of finding a first order condition on one-step frames, given an inference rule written as a modal formula with complexity (max) one.

### Installing
The package is importable by the following command:
```
pip install one_step_frames
```
Then in python code:
```
from one_step_frames ...
```
### Algorithm
The algorithm itself solves the problem in several steps:
#### Rule parsing
#### Formula initiation
#### Finding a one-step frame condition
#### Translating
#### Simplification

## spass_python
### overview
This algorithm was tasked with using [SPASS](https://www.mpi-inf.mpg.de/departments/automation-of-logic/software/spass-workbench/classic-spass-theorem-prover/download/) to automatically find a proof for the implication in the paper.

For more info, check the ```README.md``` in the ```spass_python``` folder