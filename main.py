#Name: Shruti Tulshidas Pangare
#NetID: stp8232
#main file to execute
import os
import argparse
from SingleStageDecode import decode
from conversion import *
from SingleStageExecution import PerformOperation
from FiveStageDecode import *
from FiveStageExecution import *

MemSize = 1000 # memory size
class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        
        with open(ioDir + os.sep + "imem.txt") as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]
        

    def readInstr(self, ReadAddress):
        #read instruction memory
        #return 32 bit hex val
        instruction = ''.join(self.IMem[ReadAddress : ReadAddress+4])
        return instruction
          
class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(ioDir + os.sep + "dmem.txt") as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]
            self.DMem.extend(["00000000"]*(1000-len(self.DMem)))
        

    def readDataMem(self, ReadAddress):
        #read data memory
        #return 32 bit hex val
        data = ''.join(self.DMem[ReadAddress : ReadAddress+4])
        
        return twosCompliment(data)
        
    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        WriteData = decimalToBinary(WriteData)
        arr = [WriteData[i:i+8] for i in range(0, len(WriteData), 8)]
        
        for i in range(len(arr)):
            self.DMem[Address+i] = arr[i]
                     
    def outputDataMem(self):
        resPath = self.ioDir + os.sep + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])

class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = [0x0 for i in range(32)]
    
    def readRF(self, Reg_addr):
        return self.Registers[Reg_addr]
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        if Reg_addr !=0:
            self.Registers[Reg_addr] = Wrt_reg_data
         
    def outputRF(self, cycle):
        op = ["-"*70+"\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([decimalToBinary(val)+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)

class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": True, "Instr": 0, "is_hazard":False}
        self.EX = {"nop": True, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": True, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
                   "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": True, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem
        self.takeBranch = False

# Single-Stage 
class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        # Initialize Single-Stage Core with specific I/O directory and memory
        super(SingleStageCore, self).__init__(ioDir + os.sep + "SS_", imem, dmem)
        self.opFilePath = ioDir + os.sep + "StateResult_SS.txt"  # Output file for state results

    def step(self):
        # Execute one step (one cycle) of the single-stage core
        if self.state.IF["nop"]:  # If the pipeline is in a no-operation state, halt the core
            self.halted = True

        instr = imem.readInstr(self.state.IF["PC"])  # Fetch instruction from instruction memory
        decodedInst = decode(instr)  # Decode the fetched instruction

        if decodedInst is None: 
            self.halted = True  # Halt if no valid instruction
        else: 
            # Perform the decoded instruction
            PerformOperation(decodedInst, self.myRF, self.ext_dmem, self.takeBranch, self.state)

        self.myRF.outputRF(self.cycle)  # Dump the register file state after the current cycle
        self.printState(self.state, self.cycle)  # Print the processor's state after the cycle

        self.cycle += 1  # Increment the cycle count

    def printState(self, state, cycle):
        # Print and save the state of the processor after each cycle
        printstate = ["-" * 70 + "\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")
        
        perm = "w" if cycle == 0 else "a"  # Overwrite for the first cycle, append for others
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

# Five-Stage 
class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        # Initialize Five-Stage Core with specific I/O directory and memory
        super(FiveStageCore, self).__init__(ioDir + os.sep + "FS_", imem, dmem)
        self.opFilePath = ioDir + os.sep + "StateResult_FS.txt"  # Output file for state results

    def step(self):
        # Execute one step (one cycle) of the five-stage pipeline core

        # Halt the pipeline if all stages are in a no-operation state
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True

        # --------------------- WB Stage ---------------------
        if not self.state.WB["nop"]:  # Write-back stage
            WB(self.state, self.myRF)  # Perform the write-back operation
            if self.state.MEM["nop"]:
                self.state.WB["nop"] = True
        else:
            if not self.state.MEM["nop"]:
                self.state.WB["nop"] = False

        # --------------------- MEM Stage --------------------
        if not self.state.MEM["nop"]:  # Memory stage
            Mem(self.state, self.ext_dmem)  # Perform memory operations (read/write)
            if self.state.EX["nop"]:
                self.state.MEM["nop"] = True
        else:
            if not self.state.EX["nop"]:
                self.state.MEM["nop"] = False

        # --------------------- EX Stage ---------------------
        if not self.state.EX["nop"]:  # Execute stage
            EX(self.state)  # Perform ALU operations
            self.state.MEM["nop"] = False
            if self.state.ID["nop"]:
                self.state.EX["nop"] = True
        else:
            if not self.state.ID["nop"]:
                self.state.EX["nop"] = False

        # --------------------- ID Stage ---------------------
        if not self.state.ID["nop"]:  # Instruction Decode stage
            self.state.EX["nop"] = False
            ID(self.state, self.myRF)  # Decode the instruction
            if self.state.IF["nop"]:
                self.state.ID["nop"] = True
        else:
            if not self.state.IF["nop"]:
                self.state.ID["nop"] = False

        # --------------------- IF Stage ---------------------
        if not self.state.IF["nop"]:  # Instruction Fetch stage
            if self.state.ID["nop"] or (self.state.EX["nop"] and self.state.ID["is_hazard"]):
                pass
            else:
                IF(self.state, self.ext_imem)  # Fetch the next instruction
                if not self.state.IF["nop"]:
                    self.state.ID["nop"] = False

        # Dump the register file and state after the current cycle
        self.myRF.outputRF(self.cycle)
        self.printState(self.state, self.cycle)

        self.cycle += 1  # Increment the cycle count

    def printState(self, state, cycle):
        # Print and save the state of the processor after each cycle
        printstate = ["-" * 70 + "\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        perm = "w" if cycle == 0 else "a"  # Overwrite for the first cycle, append for others
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

# Function to Print Performance Metrics
def printPerformanceMetrics(ioDir, CPI_SS, IPC_SS, cycles_SS, CPI_FS, IPC_FS, cycles_FS):
    opFilePath = ioDir + os.sep + "PerformanceMetrics.txt"

    # Single-stage performance metrics
    printstate_SS = ["Performance of Single Stage:\n"]
    printstate_SS.append("#Cycles -> " + str(cycles_SS) + "\n")
    printstate_SS.append("#Instructions -> " + str(cycles_SS - 1) + "\n")
    printstate_SS.append("CPI -> " + str(CPI_SS) + "\n")
    printstate_SS.append("IPC -> " + str(IPC_SS) + "\n\n")

    # Five-stage performance metrics
    printstate_FS = ["Performance of Five Stage:\n"]
    printstate_FS.append("#Cycles -> " + str(cycles_FS) + "\n")
    printstate_FS.append("#Instructions -> " + str(cycles_SS - 1) + "\n")
    printstate_FS.append("CPI -> " + str(CPI_FS) + "\n")
    printstate_FS.append("IPC -> " + str(IPC_FS) + "\n")

    # Write performance metrics to file
    with open(opFilePath, 'w') as wf:
        wf.writelines(printstate_SS)
        wf.writelines(printstate_FS)

# Main Function
if __name__ == "__main__":
    # Parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)

    # Initialize instruction and data memory
    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)

    # Initialize single-stage and five-stage cores
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    # Simulate single-stage core
    while True:
        if not ssCore.halted:
            ssCore.step()
        if ssCore.halted:
            break

    # Simulate five-stage core
    while True:
        if not fsCore.halted:
            fsCore.step()
        if fsCore.halted:
            break

    # Output data memory for both cores
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()

    # Calculate and print performance metrics
    IPC_SS = round((ssCore.cycle - 1) / ssCore.cycle, 6)
    CPI_SS = round(1 / IPC_SS, 5)

    IPC_FS = round((ssCore.cycle - 1) / fsCore.cycle, 6)
    CPI_FS = round(1 / IPC_FS, 5)

    printPerformanceMetrics(ioDir, CPI_SS, IPC_SS, ssCore.cycle, CPI_FS, IPC_FS, fsCore.cycle)
