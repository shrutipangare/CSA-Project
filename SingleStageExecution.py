from conversion import *

def PerformOperation(dInst, register,dataMem,take_Branch,PC):
    
    #R-type----------------------------------------------------------------------

    if(dInst['type'] == 'add'):
        rs1 = binaryToDecimal(dInst['rs1'])
        rs2 = binaryToDecimal(dInst['rs2'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = data1 + data2
        register.writeRF(rd, result)
    
    elif(dInst['type'] == 'sub'):
        rs1 = binaryToDecimal(dInst['rs1'])
        rs2 = binaryToDecimal(dInst['rs2'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = data1 - data2
        register.writeRF(rd, result)
    
    elif(dInst['type'] == 'xor'):
        rs1 = binaryToDecimal(dInst['rs1'])
        rs2 = binaryToDecimal(dInst['rs2'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = data1 ^ data2
        register.writeRF(rd, result)
    
    elif(dInst['type'] == 'or'):
        rs1 = binaryToDecimal(dInst['rs1'])
        rs2 = binaryToDecimal(dInst['rs2'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = data1 | data2
        register.writeRF(rd, result)

    elif(dInst['type'] == 'and'):
        rs1 = binaryToDecimal(dInst['rs1'])
        rs2 = binaryToDecimal(dInst['rs2'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = data1 & data2
        register.writeRF(rd, result)

    #I-type --------------------------------------------------------------------

    elif(dInst['type'] == 'addi'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        result = data1 + imm
        register.writeRF(rd, result)
    
    elif(dInst['type'] == 'xori'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        result = data1 ^ imm
        register.writeRF(rd, result)

    elif(dInst['type'] == 'ori'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        result = data1 | imm
        register.writeRF(rd, result)
    
    elif(dInst['type'] == 'andi'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        data1 = register.readRF(rs1)
        result = data1 & imm
        register.writeRF(rd, result)
    
    #Load-type --------------------------------------------------------------------
    
    elif(dInst['type'] == 'lw'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        address = register.readRF(rs1)
        address = address + imm
        result = dataMem.readDataMem(address)
        register.writeRF(rd, result)
    
    #Store-type --------------------------------------------------------------------
    
    elif(dInst['type'] == 'sw'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rs2 = binaryToDecimal(dInst['rs2'])
        data = register.readRF(rs2)
        address = register.readRF(rs1)
        address = address + imm
        dataMem.writeDataMem(address,data)
    
    #Branch-type --------------------------------------------------------------------

    elif(dInst['type'] == 'beq'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rs2 = binaryToDecimal(dInst['rs2'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        
        result = abs(data1-data2)
        if result==0:
            take_Branch = True
            PC.IF["PC"] += imm
    
    elif(dInst['type'] == 'jal'):
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        register.writeRF(rd, PC.IF["PC"]+4)
        take_Branch = True
        PC.IF["PC"] += imm << 1
    
    elif(dInst['type'] == 'bne'):
        rs1 = binaryToDecimal(dInst['rs1'])
        imm = twosCompliment(dInst['imm'])
        rs2 = binaryToDecimal(dInst['rs2'])
        data1 = register.readRF(rs1)
        data2 = register.readRF(rs2)
        result = abs(data1-data2)
        if result!=0:
            take_Branch = True
            PC.IF["PC"] += imm
    
    #JAL-type --------------------------------------------------------------------
    
    elif(dInst['type'] == 'jal'):
        imm = twosCompliment(dInst['imm'])
        rd = binaryToDecimal(dInst['rd'])
        register.writeRF(rd, PC.IF["PC"]+4)
        take_Branch = True
        PC.IF["PC"] += imm << 1
    
    elif(dInst['type'] == 'HALT'):
        take_Branch = True
        PC.IF["nop"] = True

    if not take_Branch:
        PC.IF["PC"] += 4

    
    
    
    
    

"""
Assuming x20 = 12

sw x10, 0(x20)
lw x11, 4(x20)
add x12, x10, x11
sw x12, 8(x0)
"""
