# Digital Circuit Critical Path Analysis Tool



Author: Ahmad6564

Date: December 31, 2024

## Table of Contents
* Overview
* Installation
* Usage
* Examples
* Design Decisions & Assumptions
## Overview
This tool analyzes digital circuits to find their critical paths - the longest combinational paths that determine the maximum operating frequency. It supports both combinational and sequential circuits, providing visualization and detailed timing analysis.

## Installation
### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)



## Input File Format
Circuit descriptions should follow this format:

Circuit name

Format: <node_type> <node_id> <input_nodes...>

INPUT in1

INPUT in2

ADD add1 in1 in2

MUL mul1 in1 add1

REG reg1 mul1

### Component Delay Values
* Adder (ADD): 1.0 time units
* Multiplier (MUL): 1.0 time units
* Register (REG): 0.2 time units
* Multiplexer (MUX): 1.0 time units


## Examples
### Example 1: 4-bit Carry Lookahead Adder


Input file: cla_4bit.txt

INPUT a3

INPUT a2
...

OUTPUT sum3 p3_xor_c3

OUTPUT cout c4

### Output:

Circuit name: 4-bit Carry Lookahead Adder

Critical Path: in1 -> g0 -> c1 -> c2 -> c3 -> c4 -> cout

Total Delay: 5.0 time units



## Example 2: Sequence Detector (1011)

 Input file: sequence_detector.txt

INPUT clock

INPUT reset

INPUT data_in
...

OUTPUT detected state_s3_and_in

Output:


Circuit name: Sequence Detector (1011)

Critical Path: data_in -> next_state_logic -> state_reg -> output_logic

Total Delay: 2.2 time units

## Example 3: FIR Filter

 Input file: fir_filter.txt

INPUT data_in

INPUT clock
...

OUTPUT fir_output sum_reg

Output:


Circuit name: FIR Filter

Critical Path: data_in -> mult0 -> add1 -> add2 -> add3 -> output_reg

Total Delay: 4.2 time units



## Design Decisions & Assumptions
### Circuit Representation

Used NetworkX library for graph representation
* Efficient graph algorithms
* Built-in visualization capabilities
* Easy path analysis
### Component Delays
1. Fixed delay values for basic components

2. Assumptions:
* Delays are constant
* No wire delays
* No clock skew
### Critical Path Analysis
1. Implementation using:

* Topological sorting
* Dynamic programming
* Depth-first search
## Error Handling

1. Robust error checking for:
* File format validation
* Circuit consistency
* Missing connections
* Cyclic dependencies
### Visualization
 
 1. Graph visualization features:
* Color-coded components
* Highlighted critical path
* Interactive graph display
### Limitations
1. Current limitations:
* Maximum circuit size (1000 nodes)
* Single clock domain
* No timing constraints
* No setup/hold time analysis
### Future Improvements
1. Potential enhancements:
* Multiple clock domains
* Variable delay models
* Timing constraint checking
* Setup/hold time analysis
* JSON/XML input support


## OUTPUT:
#### cir.txt
![image](https://github.com/user-attachments/assets/17eec204-33e9-4822-9e7f-7ca4b2c6badd)


#### 4-bit CLA.txt
![image](https://github.com/user-attachments/assets/d65f061d-6498-4ad2-bd65-5e0a68534b5e)


#### FIR Filter.txt
![image](https://github.com/user-attachments/assets/73c94be6-0c54-4e62-99f9-3de0c4fa0389)


#### 6-Bit Binary Adder.txt
![image](https://github.com/user-attachments/assets/d88aeb59-83c1-42f4-a92e-837293f2ffa7)


#### Sequence Detector.txt
![image](https://github.com/user-attachments/assets/e4f2b207-4392-44e9-a95f-2d0b62c8d796)












