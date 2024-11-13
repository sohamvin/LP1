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


#Helper functions


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


    #get location like 1, 2, 3 of the parameter in the PNTab
    def GetPositionKOfParameterInPNTABfor(self, parameter):
        for k, arg in enumerate(self.PNTabs[self.CurrentMacroName]):
            if arg == parameter:
                return k
        return -1












#Line analizing functions
    def IdentifyMacro(self, i):
        if "MACRO" in self.lines[i] and not self.InMacro:
            #If this keyword was used then in the next line there should be the macro name and 
            #Arguments defined so 

            if i+1 >= len(self.lines): #if there are no more lines after the MACRO keyword, thats wrong
                #No lines after the MACRO keyword:
                print("WRONG CODE and use of MACRO Keyword")
                return -1, False
            
            else:
                self.InMacro = True
                #We use the above guy for nested macro cases
                macroLine = self.lines[i+1] # this is the line which has macro name and all that

                if macroLine[0] in self.MNT: # 
                    print("WRONG CODE macro name already used")
                    return -1, False
                
                positionalArgs = 0 # num of positional args
                keywordArgs = 0 # num of keyword args
 
                data = [
                    #Number of positional args/ number of keyword args/  MDT pointer/  KPDTab pointer
                    0,                          0,                          0,          -1
                ]

                parameters = [

                ] # add all parameters

                keywordParameters = [

                ] # add only keyword parameters
                
                macroName = "" 

                for j, word in enumerate(macroLine): #analyze the macro defination line
                    if j == 0:
                        macroName = word # could have do this above / outside of loop also, i dont know whay i did this
                        continue

                    if "&" in word: # so it is indeed an argument cuz
                        #MACRO_NAME     &ARG1      &ARG2    &ARG3=     &ARG4=AREG etc
                        if "=" in word: # is keyword argument
                            keywordArgs += 1
                            parts = word.split("=")
                            if parts[1] == "" or not parts[1]: # so if nothing after keyword argument (like ARG3)
                                keywordParameters.append([parts[0], ""]) #Add default value as none
                            else:
                                keywordParameters.append([parts[0], parts[1]])
                            
                            parameters.append(parts[0])
                            #We need to add the keyword argument nonetheless to PNTAB 

                        else: # is positional argument
                            positionalArgs += 1
                            parameters.append(word)
                            
                        
                    else:
                        print("WRONG CODE, & is not used before parameters")
                        return -1, False
                
                self.CurrentMacroName = macroName #name of the macro we trying to analyze
                self.PNTabs[macroName] = parameters

                data[0] = positionalArgs
                data[1] = keywordArgs
                data[2] = len(self.MDT) 
                data[3] =  len(self.KPDTab) if keywordArgs != 0 else -1 # that is if keywordArgs are there then pointer, else -1 to indicate no keyword args

                self.MNT[macroName] = data

                self.KPDTab += keywordParameters 

                return i+2, True
        else:
            #If MACRO keyword is not in the line, then just continue to the -> def AnalyzeLineByLine
            return i, False
        
    
    #For MEND we need special processing
    def IdentifyMEND(self, i):
        if "MEND" in self.lines[i]:
            self.InMacro = False

            self.MDT.append(["MEND"])

            return i+1, True
        else:
            return i, False


    def AnalyzeLine(self, i): #If neither MEND or MACRO Declaration line -> so append to MDT
        replacement = []
        for word in self.lines[i]:
            if "&" in word: # so if we are using a parameter, we need to replace it with like (P,1) or (P,2) ...
                if word in self.PNTabs[self.CurrentMacroName]:
                    if self.GetPositionKOfParameterInPNTABfor(word) == -1:
                        #something went wrong
                        return -1
                    else:
                        replacement.append(f"(P,{self.GetPositionKOfParameterInPNTABfor(word)})")
                else:
                    print(f"WRONG CODE, {word} is not an argument in {self.CurrentMacroName}")
                    return -1
                
                #A lot of error prevention code, which is not really necessary
                
            else:
                replacement.append(word) # if it is not a parameter, then place that word as is
                
        self.MDT.append(replacement)
        return i+1 # Go to next line
    

















#Analyze line by line:
    def AnalyzeLineByLine(self):
        i = 0

        while i < len(self.lines):
            print("lines: ", i, "\t", self.lines[i])

            i, wasStartLine = self.IdentifyMacro(i=i) 
            #If Macro Start, special processing is done, continue to next lines
            if wasStartLine and i != -1:
                continue

            

            i, wasEndLine = self.IdentifyMEND(i=i)
            #similar to macro start
            if wasEndLine and i != -1:
                continue


            i = self.AnalyzeLine(i=i)

            # This will prevent an infinite loop if `AnalyzeLine` or other methods return -1
            if i == -1:
                print("Error encountered in line analysis. Exiting.")
                break
                        # break from the k loop, the one trying to find the position of the word












#File reading
    def ReadFile(self):
        with open(self.fileName + ".txt", "r") as file:
            for line in file:
                line_part = [ part.strip(" ").replace(",", "") for part in line.strip().split(" ") if part]
                if line_part:
                    self.lines.append(line_part)
    



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
    










#Actual Functions to call
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


