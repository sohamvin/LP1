import os

class PassTwo:
    def __init__(self):
        self.fileName = "three"

        self.LiteralTable = [

        ]

        self.IntermediateCode = [

        ]

        self.SymboleTab = [

        ]

        self.finalCode = [

        ]


        self.poolTab = [

        ]
    

    def processFiles(self):
        with open(f"{self.fileName}/" +self.fileName + "Literal" + ".txt", "r") as file:
            for line in file:
                self.LiteralTable.append([int(el.strip("\n")) for i,el in enumerate(line.split(":")) if i != 1])
            file.close()

        with open(f"{self.fileName}/" +self.fileName + "ICCode" + ".txt" , "r") as file:
            for line in file:
                self.IntermediateCode.append([el.strip("\n") for el in line.split(":") if el.strip("\n") ])
            file.close()

        with open(f"{self.fileName}/" +self.fileName + "Symbole" + ".txt", "r") as file:
            for line in file:
                self.SymboleTab.append([int(el.strip("\n")) for i,el in enumerate(line.split(":")) if el.strip("\n") and i != 1])
        
            file.close()

        self.finalCode = [row[:] for row in self.IntermediateCode]

        self.ProcessInterMediateCodeRemoveNoLCLines()

        self.ProcessInterMediateCodeFirstElement()

        self.LastProcess()

        with open(f"{self.fileName}/" +self.fileName + "Pass2" + ".txt", "w") as file:
            for line in self.finalCode:
                file.write(f"{line[0]}:{line[1]}:{line[2]}:{line[3]}\n")
            
            file.close()

        
    def PrintTabs(self):
        for e in self.LiteralTable:
            print(e)

        print("\n\nIntermediateCOde: \n\n\n")

        for e in self.IntermediateCode:
            print(e)

        print("\n\n\n\n\n\nFinal Code : \n\n\n")

        for e in self.finalCode:
            print(e)

        print("\n\n\n\n\n\n\n")

        for e in self.SymboleTab:
            print(e)

        print("\n\n")

    
    def ProcessLiteralsSymbolesRegistersConstantsOthers(self, str1):
        if "L" in str1:
            str1 = str1.strip("(")
            str1 = str1.strip(")")
            str1 = str1.split(",")
            str1 = str(self.LiteralTable[int(str1[1])][1])
            return str1
        elif "S" in str1 and "IS" not in str1:
            str1 = str1.strip("(")
            str1 = str1.strip(")")
            str1 = str1.split(",")
            print(str1)
            str1 = str(self.SymboleTab[int(str1[1])][1])
            return str1
        elif "RG" in str1:
            str1 = str1.strip("(")
            str1 = str1.strip(")")
            str1 = str1.split(",")
            str1 = str1[1]
            return str1
        elif "C" in str1: #and "CC" not in str1: #Spliting C AND CC same you want the value only so 
            str1 = str1.strip("(")
            str1 = str1.strip(")")
            str1 = str1.split(",")
            str1 = str1[1]
            return str1
        else:
            return str1
        
    def LastProcess(self):
        for i, ele in enumerate(self.finalCode):
            if len(ele) == 3:
                ele.insert(2, '0')
            elif len(ele) == 2:
                ele.append('0')
                ele.append('0')
    
    def ProcessInterMediateCodeRemoveNoLCLines(self):
        newThing = [
            
        ]

        for i, ele in enumerate(self.finalCode):
            if int(ele[-1]) == -1:
                pass
            else:
                # newThing.append(self.IntermediateCode[i])
                last_ele = ele.pop()
                ele.insert(0, last_ele)
                # print(i, " : ", ele, "\t", self.IntermediateCode[i] == ele)
                newThing.append(self.finalCode[i])


        self.finalCode = newThing
    
    def ProcessInterMediateCodeFirstElement(self):

        newThing = [

        ]

        for i,ele in enumerate(self.finalCode):
            sr = ele[1].strip("()")
            sr = sr.strip(")")
            sr = sr.split(",")

            if sr[0] == "IS":
                sr = sr[1]
            elif sr[0] == "DL":
                if sr[1] == "2": # DL 2 is DS, DS has no Memory, look at the Commandstable, DC has Memory allocation, but not DS so dont compy anything for DS
                    #So we meed to remove the line which is of DS
                    continue
                elif sr[1] == "1":
                    #DC so allocate space
                    sr = "0"
            
            ele[1] = sr

            for j,mnt in enumerate(ele):
                ele[j] = self.ProcessLiteralsSymbolesRegistersConstantsOthers(mnt)

            self.finalCode[i] = ele
            newThing.append(ele)

        self.finalCode = newThing








p2 = PassTwo()


p2.processFiles()
p2.PrintTabs()

