import os


class Pass1:
    def __init__(self):

        self.InMacro = False # can be used for nested macro

        self.PNTabs = {

        } # macro name : [ parameter1, parameter2 ... ]

        self.KPDTab = [

        ] # 1, arg, default val // not dict with arg as primary key as two macros can have same name for a 
        #keyword arg

        self.MDT = [

        ]

        #simply write lines.

        self.MNT = {

        }
        # Name of Macro : [ #PP #KP MDTP    KPDTP]


        self.lines = [

        ]

        self.fileName = "one"

        self.CurrentMacroName = ""



    def AnalyzeLineByLine(self):
        i = 0

        while i < len(self.lines):
            print("lines: ", i, "\t", self.lines[i])

            i, wasStartLine = self.IdentifyMacro(i=i) 
            if wasStartLine and i != -1:
                continue

            i, wasEndLine = self.IdentifyMEND(i=i)
            if wasEndLine and i != -1:
                continue


            i = self.AnalyzeLine(i=i)

            # This will prevent an infinite loop if `AnalyzeLine` or other methods return -1
            if i == -1:
                print("Error encountered in line analysis. Exiting.")
                break

    def GetPositionKOfParameterInPNTABfor(self, parameter):
        for k, arg in enumerate(self.PNTabs[self.CurrentMacroName]):
            if arg == parameter:
                return k
        return -1
                            # break from the k loop, the one trying to find the position of the word

    def AnalyzeLine(self, i):
        replacement = []
        for word in self.lines[i]:
            if "&" in word:
                if word in self.PNTabs[self.CurrentMacroName]:
                    if self.GetPositionKOfParameterInPNTABfor(word) == -1:
                        return -1
                    else:
                        replacement.append(f"(P,{self.GetPositionKOfParameterInPNTABfor(word)})")
                else:
                    print(f"WRONG CODE, {word} is not an argument in {self.CurrentMacroName}")
                    return -1
                
            else:
                replacement.append(word) # if it is not a parameter, then place that word as is
                
        self.MDT.append(replacement)
        return i+1
    
    def StoreTablesInFile(self):
        os.makedirs(self.fileName, exist_ok=True)
        with open(f"{self.fileName}/" + self.fileName + "MNT" + ".txt", "w") as file:
            for key, val in self.MNT.items():
                file.write(key + ":")
                for ele in val:
                    file.write(str(ele) + ",")
                file.write("\n")

            file.close()

        with open(f"{self.fileName}/" +self.fileName + "PNTAB" + ".txt", "w") as file:
            for key, val in self.PNTabs.items():
                file.write(key + ":")
                for ele in val:
                    file.write(ele + ",")
                file.write("\n")
            file.close()

        with open(f"{self.fileName}/" +self.fileName + "MDT" + ".txt", "w") as file:
            for array in self.MDT:
                for ele in array:
                    file.write(ele + ";")
                file.write("\n")
            file.close()

        with open(f"{self.fileName}/" +self.fileName + "KPDTAB" + ".txt", "w") as file:
            for array in self.KPDTab:
                file.write(array[0] + ":" + array[1])
                file.write("\n")
            file.close()
        


    def IdentifyMacro(self, i):
        if "MACRO" in self.lines[i] and not self.InMacro:

            if i+1 >= len(self.lines):
                #No lines after the MACRO keyword:
                print("WRONG CODE and use of MACRO Keyword")
                return -1, False
            
            else:
                self.InMacro = True
                macroLine = self.lines[i+1]

                print(macroLine)

                if macroLine[0] in self.MNT:
                    print("WRONG CODE macro name already used")
                    return -1, False
                
                positionalArgs = 0
                keywordArgs = 0

                data = [
                    #Number of positional args/ number of keyword args/  MDT pointer/  KPDTab pointer
                    0,                          0,                          0,          -1
                ]

                parameters = [

                ]

                keywordParameters = [

                ]
                
                macroName = ""

                for j, word in enumerate(macroLine):
                    if j == 0:
                        macroName = word
                        continue

                    if "&" in word:
                        if "=" in word: # is keyword argument
                            keywordArgs += 1
                            parts = word.split("=")
                            if parts[1] == "" or not parts[1]:
                                keywordParameters.append([parts[0], ""])
                            else:
                                keywordParameters.append([parts[0], parts[1]])
                            
                            parameters.append(parts[0])

                        else: # is positional argument
                            positionalArgs += 1
                            parameters.append(word)
                            
                        
                    else:
                        print("WRONG CODE, & is not used before parameters")
                        return -1, False
                
                self.CurrentMacroName = macroName
                self.PNTabs[macroName] = parameters

                data[0] = positionalArgs
                data[1] = keywordArgs
                data[2] = len(self.MDT)
                data[3] =  len(self.KPDTab) if keywordArgs != 0 else -1 # that is if keywordArgs are there then pointer, else -1 to indicate no args

                self.MNT[macroName] = data

                self.KPDTab += keywordParameters

                return i+2, True
        else:
            return i, False
        



    def IdentifyMEND(self, i):
        if "MEND" in self.lines[i]:
            self.InMacro = False

            self.MDT.append(["MEND"])

            return i+1, True
        else:
            return i, False 
        

    def PrintTables(self):
        print("MNT: ")
        for l, val in self.MNT.items():
            print(l, " : ", val)

        print("\n\n")

        print("MDT: ")
        for l in self.MDT:
            print(l)

        print("\n\n")

        print("KPDT: ")
        for l in self.KPDTab:
            print(l)
        
        print("\n\n")

        print("PNTAB: ")
        for l, val in self.PNTabs.items():
            print(l, " : ", val)


    def ReadFile(self):
        with open(self.fileName + ".txt", "r") as file:
            for line in file:
                line_part = [ part.strip(" ").replace(",", "") for part in line.strip().split(" ") if part]
                if line_part:
                    self.lines.append(line_part)
    

    def DoStuff(self):
        self.ReadFile()
        self.AnalyzeLineByLine()
        self.StoreTablesInFile()

    
    def PrintStuff(self):
        for l in self.lines:
            print(l)
        
        print("\n\n\n\n\n\n\n\n")

        self.PrintTables()



p1 = Pass1()

p1.DoStuff()

p1.PrintStuff()


