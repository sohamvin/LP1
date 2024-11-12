# Assuming that BestFit is imported correctly from the file
from MemAlgos import BestFit, WorstFit, NextFit, FirstFit

# Initialize algorithm based on user's choice
x = int(input("What do you want to use? \n1 for first fit\n2 for worst fit\n3 for next fit\n4 for best fit\n\n\n"))

algo = None

if x == 1:
    algo = FirstFit()
elif x == 2:
    algo = WorstFit()
elif x == 3:
    algo = NextFit()
else:
    algo = BestFit()


print("\n\n\n\n")

# Memory size for processes
size = 60
while True:
    sToPrint = "1 for Entering a process\n2 for Seeing all processes\n3 for Looking at memory\n4 for Removing a process"

    if x == 3:
        sToPrint += "\n5 to see last memory index"
    
    sToPrint += "\nAnything else for quitting\n\n\n"

    print(sToPrint)

    x1 = input("Enter a choice: ")
    
    if x1 == "1":
        letter = input("Enter Name of Process: ")
        print()
        sz = int(input(f"Enter size of process (should be less than {size}): "))
        ans = algo.insert(letter, sz)
        if ans is not None:
            print(f"Process {letter} added at position {ans}")
        else:
            print("Not enough memory to add process.")

    elif x1 == "2":
        print(algo.mapOfProcesses())
    
    elif x1 == "3":
        print("Memory Layout:", algo.printArray())
    
    elif x1 == "4":
        proces = input("What process to remove? ")
        if not algo.processExists(proces):
            print("Invalid process")
        else:
            algo.removeProcess(proces)
            print(f"Process {proces} removed.")

    elif x == 3 and x1 == "5":
        print(algo.getLastIndex())
    
    else:
        print("Exiting...")
        break
