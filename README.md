The project simulates the functionality of a RISC-V RV32I processor with two configurations: a single-stage core and a five-stage pipeline core. The simulation includes the handling of instruction memory, data memory, register file, and processor state for each core.

Single-Stage Processor Architecture

In the single-stage architecture, each instruction passes through all stages in one cycle. While this simplicity facilitates straightforward execution and debugging, it lacks parallelism, as each instruction occupies the entire processor for one cycle.

Design Schematic:

The single-stage design performs the following steps in one cycle:
Instruction Fetch (IF): Fetches instruction from imem.txt based on the program counter (PC).
Instruction Decode/Register Read (ID/RR): Decodes the instruction, identifying control signals, source registers, destination registers, and immediate values.
Execute (EX): The Arithmetic Logic Unit (ALU) performs computations.
Memory Access (MEM): Executes load/store instructions with data memory (from dmem.txt).
Write-Back (WB): Writes results back to the register file if applicable.

Five-Stage Pipeline Core
Simulates a pipeline processor with five stages:
Instruction Fetch (IF): Fetch the instruction from memory.
Instruction Decode (ID): Decode the instruction and determine dependencies.
Execution (EX): Perform arithmetic operations using the ALU.
Memory (MEM): Access data memory for load and store instructions.
Write-Back (WB): Write results back to the register file.
Hazard Handling:
The implementation tracks hazards in the ID stage and stalls the pipeline when needed.
Execution Flow:
Each stage is executed in parallel for multiple instructions, with each stage handling a different instruction in the pipeline.
The step method executes one cycle of the pipeline, updating states for all stages.

Implementation:

The implementation relies on the following external modules:
SingleStageDecode & SingleStageExecution:
Functions for decoding and executing instructions in the single-stage core.
FiveStageDecode & FiveStageExecution:
Functions for decoding and executing instructions in the five-stage core.
Conversion:
Utility functions for binary/decimal conversions and two's complement representation.


Output:

State Results:
Single-stage core: StateResult_SS.txt.
Five-stage core: StateResult_FS.txt.
Register File: RFResult.txt.
Data Memory: *_DMEMResult.txt for both cores.
Performance Metrics: PerformanceMetrics.txt.

Performance Parameters:
The simulation measures performance for both cores in terms of:
CPI (Cycles Per Instruction): Average number of cycles required to execute an instruction.

CPI = No. of cycles/No. of instructions Instructions per cycle = 1/Cycles per instruction
For single-stage, CPI is always 1 since all operations occur in one cycle.
For the five-stage pipeline, CPI depends on pipeline hazards and stalls.
IPC (Instructions Per Cycle): Number of instructions executed per cycle.
IPC is calculated as (Instructions Executed)/(Total Cycles).
The performance metrics are written to a file PerformanceMetrics.txt.



