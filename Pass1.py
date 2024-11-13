# Open and read the file line by line
    
import os

class PassOne:

    def __init__(self):
        
        self.fileName = "two"

        self.lines = [

        ]

        self.InterMediateCode = [

        ]

        self.LC = 0

        self.symbolTable = {

        }

        self.poolTable = [

        ]

        self.Commands = {
            "STOP" : ["IS", 0, 1],
            "ADD" : [ "IS", 1, 1 ],
            "SUB": ["IS", 2, 1],
            "MULT" : ["IS", 3, 1],
            "MOVER" : ["IS", 4, 1],
            "MOVEM" : ["IS", 5, 1],
            "COMP" : ["IS", 6, 1],
            "BC" : ["IS", 7, 1],
            "DIV"  : ["IS", 8, 1],
            "READ" : ["IS", 9, 1],
            "PRINT" : ["IS", 10, 1],
            "START" : ["AD", 1, 0],
            "END" : ["AD", 2, 0],
            "ORIGIN" : ["AD", 3, 0],
            "EQU" : ["AD", 4, 0],
            "LTORG" : ["AD", 5, 0],
            "DC" : ["DL", 1, 1],
            "DS" : ["DL", 2, 0],
            "AREG" : ["RG", 1],
            "BREG" : ["RG", 2],
            "CREG" : ["RG", 3],
            "EQ" : ["CC", 1, 0],
            "LT" : ["CC", 2, 0],
            "GT" : ["CC", 3, 0],
            "LE" : ["CC", 4, 0],
            "GE" : ["CC", 5, 0],
            "NE" : ["CC", 6, 0],
            "ANY" : ["CC", 7, 0]
            
        }

        self.literalTable = [

        ]



#Helper functions
    def strIsLiteral(self, a):
        if "=" in a:
            return True
        return False

    def extractLiteral(self, literalstr):
        if self.strIsLiteral(literalstr):

            literalstr = literalstr.strip("=")  # as literal looks like:   (  ='5'  )
            literalstr = literalstr.strip("'")
            if literalstr.isdigit():
                return literalstr
            return "/0"
        else:
            return "/0"
        
    def GenerateStrForCommand(self,CommandStr) -> str:
        return "(" + self.Commands[CommandStr][0] + "," + str(self.Commands[CommandStr][1]) + ")"

        
    def GenerateStrForSymbole(self,symbole) -> str:
        sr = "(" + "S" + ","
        for i, a in enumerate(self.symbolTable.keys()):
            if a == symbole:
                sr += str(i)
                break
        sr += ")"

        return sr


    def resolveSymbolOrConstant(self, value):
        """
        Resolves value from self.symbolTable or converts it to integer if it's a digit.
        Returns tuple (nextS, num) where:
            - nextS: Intermediate code string for the symbol or constant
            - num: Integer value of the symbol or constant
        """
        if value in self.symbolTable and self.symbolTable[value] != "":
            # Symbol exists and is defined
            for i, key in enumerate(self.symbolTable.keys()):
                if value == key:
                    return f"(S,{i})", self.symbolTable[value]
        elif value.isdigit():
            # Value is a digit
            return value, int(value)
        # If symbol is undefined or invalid
        return None, -1  








#Append Functions(Appending symboles to symbole table and literals to literal table also assigning LC values if we can do that)
    def ProcessLiteral(self,line):
        for a in line:
            if self.strIsLiteral(a=a):  # Use 'in' to check for "=" in the string
                self.literalTable.append([a, ""])
                return True, len(self.literalTable)-1
        return False, -1

    def MakeSymbTable(self,line, LC):
        for a in line:
            if (not self.strIsLiteral(a)) and  (a not in self.Commands) and ( not a.isdigit()) and ("ORIGIN" not in line) and ( "'" not in a) and ("+" not in a) and ("-" not in a): 
                #If neither of above conditions are fullfilled then [a] can only be a symble.  it is not a command
                #not a literal
                #not ORIGIN
                #doesnt have '' / + / - in it so not constant like '1' or an expression like LABEL1-3 or LABEL2+3 used in things like ORIGIN LABEL1+3 
                if (a not in self.symbolTable) and (line[0] != a):
                    self.symbolTable[a] = ""
                elif (a not in self.symbolTable)  and (line[0] == a):
                    # print("ABRAKADABRA", a)
                    self.symbolTable[a] = LC
                elif (self.symbolTable[a] == "") and (line[0] == a):
                    self.symbolTable[a] = LC










#Process Line

    def ProcessEQU(self,line_parts):

            '''
            No Intermediate Code is generated for EQU
            The EQU directive is a symbolic equate, meaning it assigns
            the value of one symbol to another symbol without allocating memory.
            When you write X EQU Y, you are telling the assembler that X should
            have the same value as Y, effectively creating an alias. 
            However, no new memory location is allocated for X.
            '''

            if len(line_parts) != 3 or line_parts[1] != "EQU":
                print("WRONG CODE")
                return
            else:
                print("SYMBOLE TABLE BEFORE: ", self.symbolTable)
                
                # if line_parts[0] not in self.symbolTable:
                #     LC += 1

                if "+" in line_parts[2]:
                    parts = line_parts[2].split("+")
                    _, left_val = self.resolveSymbolOrConstant(parts[0])
                    _, right_val = self.resolveSymbolOrConstant(parts[1])
                    if left_val == -1 or right_val == -1:
                        print("Wrong use of EQU")
                        return
                    self.symbolTable[line_parts[0]] = left_val + right_val

                elif "-" in line_parts[2]:
                    parts = line_parts[2].split("-")
                    _, left_val = self.resolveSymbolOrConstant(parts[0])
                    _, right_val = self.resolveSymbolOrConstant(parts[1])
                    if left_val == -1 or right_val == -1:
                        print("Wrong use of EQU")
                        return
                    self.symbolTable[line_parts[0]] = left_val - right_val

                elif line_parts[2].isdigit():
                    self.symbolTable[line_parts[0]] = int(line_parts[2])

                elif line_parts[2] in self.symbolTable:
                    self.symbolTable[line_parts[0]] = self.symbolTable[line_parts[2]]

                else:
                    print("Wrong use of EQU")
                    return
    
                print("SYMBOLE TABLE AFTER: ", self.symbolTable)



    def ifOrigin(self, line):
        ICCode = []
        nextS = ""

        # Check if we have an addition in the origin statement
        if "+" in line[1]:
            a = line[1].split("+")
            leftS, leftNum = self.resolveSymbolOrConstant(a[0])
            rightS, rightNum = self.resolveSymbolOrConstant(a[1])

            if leftNum == -1 or rightNum == -1:
                print("WRONG CODE: Undefined symbol in ORIGIN statement")
                return
            
            # Sum the resolved values
            self.LC = leftNum + rightNum
            nextS = leftS + "+" + rightS

        elif "-" in line[1]:
            a = line[1].split("-")
            leftS, leftNum = self.resolveSymbolOrConstant(a[0])
            rightS, rightNum = self.resolveSymbolOrConstant(a[1])

            if leftNum == -1 or rightNum == -1:
                print("WRONG CODE: Undefined symbol in ORIGIN statement")
                return
            
            # Sum the resolved values
            self.LC = leftNum - rightNum
            nextS = leftS + "-" + rightS
        else:
            # Simple ORIGIN value
            simpleS, simpleNum = self.resolveSymbolOrConstant(line[1])
            if simpleNum == -1:
                print("WRONG CODE: Invalid or undefined ORIGIN value")
                return
            
            self.LC = simpleNum
            nextS = simpleS

        ICCode.append(self.GenerateStrForCommand("ORIGIN"))
        ICCode.append(nextS)
        ICCode.append(-1) # insert -1 for saying No LC 
        self.InterMediateCode.append(ICCode)



    def ProcessENDOrLTORG(self,line_parts):


        if "END" in line_parts:
            self.InterMediateCode.append([self.GenerateStrForCommand("END"), -1]) # insert -1 for saying No LC 

        for i, a in enumerate(self.literalTable):
            ICCode = []
            if a[1] == "":
                ICCode.append(self.GenerateStrForCommand("DC")) # unprocessed literals are appended as DC literal statements
                a[1] = self.LC # LC for the literal becomes this
                self.LC += 1
                getNumFromLiteral = self.extractLiteral(a[0])
                if getNumFromLiteral != "/0":
                    ICCode.append("(" + "C" + "," + getNumFromLiteral + ")") # IC for literal DC statements , literals are treated as constants
                    ICCode.append(a[1]) # Append Value Of LC
                else:
                    print("WRONG CODE LITERAL")
                    return
            if ICCode:
                self.InterMediateCode.append(ICCode)


    #I.E. no EQU, ORIGIN, END, LTORG, START statement -> then do this 
    def SimpleProcessing(self, line_parts, literalThere, pos):
        ICCode = []

        for i, a in enumerate(line_parts):
            if a in self.symbolTable:
                if i == 0:
                    #Dont append Symbole if it is start of the Statement
                    pass
                else:
                    ICCode.append(self.GenerateStrForSymbole(a))
                    
            elif self.strIsLiteral(a):
                if literalThere: #if there is indeed a literal in this line: 
                    ICCode.append("(" + "L" + "," + str(pos) + ")") # pos is position of the literal in the literal table
                else:
                    print("WRONG CODE AS IT SEEMS THAT THERE WAS NO LITERAL FOUND")
                    return 
                
            elif a in self.Commands:
                ICCode.append(self.GenerateStrForCommand(a))
            else:
                if a.isdigit():
                    ICCode.append("(" + "C" + "," + a + ")") # Append constants as constnats 
                elif a.strip("'").isdigit():  # Sometimes in DC Statments constants are written like '5' / '1' so thats why this line
                    ICCode.append("(" + "C" + "," + a.strip("'") + ")")
        
        ICCode.append(self.LC) # Append Val of LC for that line -> line_parts
        self.LC += 1
        self.InterMediateCode.append(ICCode)


    #If it is a DS statement, we dont increment LC by 1 but rather 
    #By however much like: 
    #LABEL1 DS 3
    #Then LC += 3
    #And in Intermediate code, LABEL1 Intermediate code is not generated
    def ProcessDS(self, line_parts):
        ICCode  = []
        # if line_parts[0] in self.symbolTable:
        #     ICCode.append(self.GenerateStrForSymbole(line_parts[0]))
        if line_parts[1] in self.Commands: # If the 2nd [1st index position] is indeed in Commands(is  DS) then add that
            ICCode.append(self.GenerateStrForCommand(line_parts[1]))
        if line_parts[2].isdigit(): # Process the 3 / whatever constant
            ICCode.append("(" + "C" + "," + line_parts[2] + ")")
            ICCode.append(str(self.LC))
            self.LC += int(line_parts[2])
        
        if ICCode:
            self.InterMediateCode.append(ICCode)
        


    #Redirect to Approriate line processing function
    def ProcessAndInterMediateCode(self,line_parts):

        # print(line_parts, self.LC)

        if "START" in line_parts:
            self.LC = int(line_parts[1])
            ICLine = []
            ICLine.append(self.GenerateStrForCommand("START"))
            ICLine.append("(" + "C" + "," + line_parts[1] + ")")
            ICLine.append(-1)
            self.InterMediateCode.append(ICLine)
            return
        
        #First Make Symboles
        self.MakeSymbTable(line_parts, LC=self.LC)
        literalThere, position = self.ProcessLiteral(line=line_parts)
        
        if "EQU" in line_parts:
            self.ProcessEQU(line_parts=line_parts)

        elif "ORIGIN" in line_parts:
            self.ifOrigin(line=line_parts)

        elif "END" in line_parts or "LTORG" in line_parts:
            #No increment of LC for END but process/ assign unassigned literals Values
            self.ProcessENDOrLTORG(line_parts=line_parts)
            pass
        elif "DS" in line_parts:
            self.ProcessDS(line_parts=line_parts)
        else:
            self.SimpleProcessing(line_parts, literalThere=literalThere, pos=position)
            







#Simply goes line by line and processes each line 
    def goThroughLineByLine(self):
        for line_parts in self.lines:
            self.ProcessAndInterMediateCode(line_parts=line_parts)









#File Processing functions
    def ProcessFile(self) :
        with open(self.fileName + ".txt", 'r') as file:
            for line in file:
                line_parts = [ part.replace(",", "") for part in line.strip().split(" ") if part ]
                if line_parts:
                    self.lines.append(line_parts)
            

    def StoreTables(self):
        os.makedirs(self.fileName, exist_ok=True)

        with open(f"{self.fileName}/" +self.fileName + "Symbole" + ".txt", "w") as file:
            for i, (key, val) in enumerate(self.symbolTable.items()):
                # Write index, key, and value to file
                file.write(f"{i}:{key}:{str(val)}\n")
        
            file.close()
        
        with open(f"{self.fileName}/" +self.fileName + "Literal" + ".txt", "w") as file:
            for i, ele in enumerate(self.literalTable):
                file.write(f"{i}:{str(ele[0])}:{str(ele[1])}\n")
            
            file.close()

        
        with open(f"{self.fileName}/" +self.fileName + "ICCode" + ".txt", "w") as file:
            for element in self.InterMediateCode:
                for ele in element:
                    file.write(f"{ele}:")
                file.write("\n")
            
            file.close()

        







#Actual function to call
    def DoStuff(self):
        self.ProcessFile()
        self.goThroughLineByLine()

        print("\n\n\n\n\n\n\n\n\n\n")

        print(self.literalTable)
        print(self.poolTable)
        print(self.symbolTable)

        print("\n\n\n\n\n\n\n\n\n\n")

        for Ic in self.InterMediateCode:
            print(Ic)

        self.StoreTables()

        



p1 = PassOne()

p1.DoStuff()