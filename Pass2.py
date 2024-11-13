import os


class PassTwo:
    def __init__(self):

        self.filename = "one"

        self.Adjective = "Pass2.txt"

        self.PNTab = {
            #Macro name : [parameters]
        }

        self.KPDTab = [

        ]

        self.MNT = {
            #Macro name : [#pp,     #kp,     MDTPoiter,     KPDTabPointer] 
        }

        self.MDT = [

        ]

        # self.lines = [
           
        # ]


        self.ApTab = [
            #Actual parameter table:
            #[Macro name : [actual parameters] -- length same to PNTab and maps PNTab]
        ]
        #Not a dictionary because what will you do if:
        #M2 100, 200, &V=CREG, &U=BREG
        #M2 16, 120, &V=AREG, &U=BREG 
        #here then there are two macro calls for same macro name
        

        self.MacroExpandedCode = [
            #
            #       [
            #           Macro Name , [
            #               [] -> line 1, [] -> line 2, ..... [] -> line n
            #           ] 
            #       ],
            #  
            #       [   
            #           Macro Name , [
            #               [] -> line 1, [] -> line 2, ..... [] -> line n
            #           ] 
            #       ],
            # 
           #  Same as ApTab Structure. len(self.MacroExpanded) = len(self.ApTab)
        ]



        self.ReadPassTwoLines = [

        ] # read the actual lines like: M1 10, 20, &B=CREG // or -- M2 100, 200, &V=AREG, &U=BREG 
        #to analyze them





#Helper function
    #Check if the line is a macro call or not
    def IfMacroCall(self, line):
        if len(line) < 1:
            return False
        if line[0] in self.MNT:
            return True
        return False
    















#


#Actual Functions

    def GenerateAPTab(self, macro_call_line):

        '''
         it is safe to assume that the assembler's pass 1 enforces 
         this rule and blocks or flags any incorrect ordering in macro 
         definitions, ensuring that 


         !!!!!positional parameters come before keyword parameters!!!!!!. 
         

         And we assume that is how they are stored as well in 
         PNTab 
        '''

        macroname = macro_call_line[0]

        if macroname not in self.PNTab or macroname not in self.MNT:
            print(f"WRONG CODE, no such Macro as {macroname}")
            return -1, {}
        
        KPTPointer, numberOfKP, numberOfPP = self.MNT[macroname][3], self.MNT[macroname][1], self.MNT[macroname][0]

        KeywordParams = {
            
        }


        if KPTPointer != -1: #So keyword parameters are there
            for i in range(KPTPointer, KPTPointer+ numberOfKP):
                KeywordParams[self.KPDTab[i][0]] = self.KPDTab[i][1] 

        #generate the KeywordParam datastructure which has keyword parameters and default vals 
        #for this macro whose name is -> macroname

        parameters = self.PNTab[macroname] #get PNTab for the macro

        APTab = {
            #Maps macro Paremeter to argument passed/ default argument
        }


        ArgsGiven = macro_call_line[1:] # as first element if macro name, all rest are parameters

        if len(ArgsGiven) > len(parameters) or len(ArgsGiven) < numberOfPP:
            print("WRONG CODE, Wrong number of positional parameters")
            return -1, {}

        #Example:
        #Macro -> INCR_M &ARG1, &ARG2, &ARG3=, &ARG4=AREG, &ARG5=
        #Macro call -> 1) INCR_M BREG, CREG, AREG, &ARG5=DREG --> this is valid
        #Macro call -> 2) INCR_M BREG, CREG, &ARGE5= AREG --> Invalid

        for j in range(len(ArgsGiven)):
            if "=" in ArgsGiven[j]: # so if it is a keyword argument
                parts = ArgsGiven[j].split("=")
                if parts[0] not in KeywordParams:
                    print("WRONG CODE, No such keyword param ", parts[0])
                    return -1, {}
                else:
                    APTab[parts[0]] = parts[1]
            else:#jth parameter of APTab maps the jth argument, 
                #True for positional obviously but maybe also for keyword arguments passed in that order 
                #So ARG1, and ARG2 are mapped but 
                #ARG3 is also mapped to AREG for 1)
                APTab[parameters[j]] = ArgsGiven[j]    

        #Finish of remaining keyword parameters missed in loop

        for key, val in KeywordParams.items():
            if key not in APTab:
                if val == '': # if keyword argument not already passed and that keyword parameter doesnt have a default value then wrong.
                    #So for 2) &AREG3 is not in APTab and it doesnt have a default val so wrong argument passing
                    print("WRONG ARGUMENT PASSING, ", key, " Keyword argument wasnt initialized")
                    return -1, {}
                else:
                    APTab[key] = val
        
        return 0, APTab



    #Given that you have the APTAb and the macro name, generate the 
    #Code for that
    def ProduceCodeForAPTabAndMacro(self, macroname, APtab):
        ParameterToPosition = {

        }
        #maps parameter to position like:
        #1 : &AREG1
        #2 : &AREG2             .....etc

        for j, param in enumerate(self.PNTab[macroname]):
            ParameterToPosition[j] = param # position -> name maping


        
        MDTForMacro = [] #what is the macro expansion looks like for that macro call

        for i in range(self.MNT[macroname][2], len(self.MDT)): # self.MNT[macroname][2] is MDT pointer
            if "MEND" in self.MDT[i]: #So we done
                break
            line = []
            for ele in self.MDT[i]:
                if "(" in ele: # if '(' in the string then prolly
                    #ADD (P,1)  (P,2)
                    #And ele = (P,1) or (P,2)
                    #So we need to replace P,1 and P,2 with the APTab values 
                    position = ele.strip("(").strip(")").split(",")[1]
                    if position.isdigit():
                        position = int(position)
                        line.append(APtab[ParameterToPosition[position]])
                    else:
                        print("WRONG CODE,", position)
                        return -1
                else:
                    #Otherwise append the string as is
                    line.append(ele)
        
            MDTForMacro.append(line)

        return MDTForMacro
        















#File reading code and file writing code
    def ReadFiles(self):
        with open(f"{self.filename}/" +self.filename + "KPDTAB" + ".txt", "r") as file:
            for line in file:
                l = [line.split(":")[0], line.split(":")[1].strip("\n")]
                self.KPDTab.append(l)
            file.close()

        with open(f"{self.filename}/" +self.filename + "MDT" + ".txt", "r") as file:
            for line in file:
                l = [part.strip("\n") for part in line.split(";") if part.strip() != '']
                self.MDT.append(l)
            file.close()

        with open(f"{self.filename}/" +self.filename + "MNT" + ".txt", "r") as file:
            for line in file:
                l = line.split(":")
                self.MNT[l[0].strip()] = [int(ele.strip()) for ele in l[1].split(",") if ele.strip() != '']
            file.close()


        with open(f"{self.filename}/" +self.filename + "PNTAB" + ".txt", "r") as file:
            for line in file:
                l = line.split(":")
                self.PNTab[l[0].strip("\n").strip()] = [ele.strip("\n").strip() for ele in l[1].split(",") if ele.strip() != '']
            file.close()

        with open(self.filename + self.Adjective, "r") as file:
            for line in file:
                l = [ele.strip().strip("\n").strip(",") for ele in line.split(" ") if ele.strip().strip("\n").strip(",") != '']
                if l != ['']:
                    self.ReadPassTwoLines.append(l)

            file.close()


    
    def WriteExpandedCodeToFile(self):
        os.makedirs(self.filename, exist_ok=True)
        
        with open(f"{self.filename}/" + self.filename + "PassTwoExpansion" + ".txt", "w") as file:
            for line in self.MacroExpandedCode:
                for word in line:
                    file.write(word)
                    file.write("\t")
                file.write("\n")
            
            file.close()
















#Functions to call
    def DoStuff(self):
        self.ReadFiles()

        for line in self.ReadPassTwoLines:

            if self.IfMacroCall(line=line): #Check if line is a macro call

                num, aptab = self.GenerateAPTab(line) #Generate AP tab for the macro

                print(f"{line[0]} : {aptab}\n\n\n")
                if num == -1:
                    #Summin went wrong
                    return
                self.MacroExpandedCode += self.ProduceCodeForAPTabAndMacro(macroname=line[0], APtab=aptab) #Add the expanded code for the macro call
                    
            else:
                self.MacroExpandedCode.append(line) #If no macro call, add line ass is

        self.WriteExpandedCodeToFile()
                
            
    def PrintDataStructres(self):
        # print("PNTAB")
        # for key, val in self.PNTab.items():
        #     print(key, " : ", val)
        

        # print("\n\n\nMNTab")
        # for key, val in self.MNT.items():
        #     print(key, " : ", val)


        # print("\n\n\nKPDTab")
        # for ele in self.KPDTab:
        #     print(ele)

        # print("\n\n\nLines Read From Pass2")
        # for ele in self.ReadPassTwoLines:
        #     print(ele)

        # print("\n\n\n\n\nMacro Defination Table")
        # for ele in self.MDT:
        #     print(ele)

        print("\n\n\n\n\n\nLines Read")
        for ele in self.ReadPassTwoLines:
            print(ele)

        print("\n\n\n\n\n\nExpanded Code")
        for ele in self.MacroExpandedCode:
            print(ele) 





p2 = PassTwo()

p2.DoStuff()

p2.PrintDataStructres()