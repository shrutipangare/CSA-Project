def decimalToBinary(n, n_bits = 32):
    # converting decimal to binary
    # and removing the prefix(0b)
    binary_n = bin(n & (2**n_bits - 1))[2:]
    return "0" * (n_bits - len(binary_n)) + binary_n

def binaryToDecimal(n):
    return int(n,2)

def twosCompliment(n):
    if n[0] == "0":
        return(int("0b" + n, 2))
    else:
        return -(
            -int(
                "0b" + n,
                2,
            )
            & 0b11111111111
        )

def reset(state):
    if state.EX["nop"]: 
        return
    state.EX["Read_data1"] = 0
    state.EX["Read_data2"] = 0
    state.EX["Imm"] = 0
    state.EX["Rs"] = 0
    state.EX["Rt"] = 0
    state.EX["Wrt_reg_addr"] = -1
    state.EX["is_I_type"] = False
    state.EX["rd_mem"] = 0
    state.EX["wrt_mem"] = 0
    state.EX["alu_op"] = 0
    state.EX["wrt_enable"] = 0

def detectHazard(state, rs):
    
    if rs == state.MEM["Wrt_reg_addr"] and state.MEM["rd_mem"]==0:
        # EX to 1st (state.MEM["ALUresult"])
        return 1
    elif rs == state.WB["Wrt_reg_addr"] and state.WB["wrt_enable"]:
        # EX to 2nd
        # MEM to 2nd (state.WB["Wrt_data"])
        return 2
    elif rs == state.MEM["Wrt_reg_addr"] and state.MEM["rd_mem"] != 0:
        # MEM to 1st (state.WB["Wrt_data"])
        state.EX["nop"] = True
        state.ID["is_hazard"] = True
        return 3
    else:
        return 0
    
