class PassTwo:
    def __init__(self):

        self.filename = "one"

        self.Adjective = "pass2.txt"

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
        #here then there are two macro calls
        

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


    def PrintDataStructres(self):
        print("PNTAB")
        for key, val in self.PNTab.items():
            print(key, " : ", val)
        

        print("\n\n\nMNTab")
        for key, val in self.MNT.items():
            print(key, " : ", val)


        print("\n\n\nKPDTab")
        for ele in self.KPDTab:
            print(ele)

        print("\n\n\nLines Read From Pass2")
        for ele in self.ReadPassTwoLines:
            print(ele)

        print("\n\n\n\n\nMacro Defination Table")
        for ele in self.MDT:
            print(ele)
    

    def DoStuff(self):
        self.ReadFiles()


    def ReadFiles(self):
        with open(self.filename + "KPDTAB" + ".txt", "r") as file:
            for line in file:
                l = [line.split(":")[0], line.split(":")[1].strip("\n")]
                self.KPDTab.append(l)
            file.close()

        with open(self.filename + "MDT" + ".txt", "r") as file:
            for line in file:
                l = [part.strip("\n") for part in line.split(";") if part.strip() != '']
                self.MDT.append(l)
            file.close()

        with open(self.filename + "MNT" + ".txt", "r") as file:
            for line in file:
                l = line.split(":")
                self.MNT[l[0].strip()] = [int(ele.strip()) for ele in l[1].split(",") if ele.strip() != '']
            file.close()


        with open(self.filename + "PNTAB" + ".txt", "r") as file:
            for line in file:
                l = line.split(":")
                self.PNTab[l[0].strip("\n").strip()] = [ele.strip("\n").strip() for ele in l[1].split(",") if ele.strip() != '']
            file.close()

        with open(self.filename + self.Adjective, "r") as file:
            for line in file:
                l = [ele.strip().strip("\n").strip(",") for ele in line.split(" ") ]
                if l != ['']:
                    self.ReadPassTwoLines.append(l)

            file.close()



p2 = PassTwo()

p2.DoStuff()

p2.PrintDataStructres()