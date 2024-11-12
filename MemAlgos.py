
size = 60
class BestFit():
    def __init__(self):
        self.processMap = {}
        self.memory = ["*" for _ in range(size)]

    def insert(self, letter, sz):
        tempMap = {}
        counter = 0
        start = -1

        # Loop through the memory to find suitable spaces
        for i in range(len(self.memory)):
            if self.memory[i] == "*":
                if counter == 0:
                    start = i  # Mark the start of a new empty space
                counter += 1  # Increment the counter of empty spaces
            else:
                if counter >= sz:  # Found a space large enough
                    tempMap[start] = counter  # Store start index and size
                counter = 0  # Reset counter for next empty segment

        # Check for the last segment if it ends with empty space
        if counter >= sz:
            tempMap[start] = counter

        # Find the best fit
        startPoint = -1
        lestaVal = float('inf')
        for key, val in tempMap.items():  # Use .items() to get key-value pairs
            if val < lestaVal:
                lestaVal = val
                startPoint = key

        if startPoint == -1:  # No suitable space found
            return None
        else:
            # Allocate memory and update process map
            self.memory[startPoint:startPoint + sz] = [letter for _ in range(sz)]
            self.processMap[letter] = [startPoint, sz]  # Store the process in the map
            return startPoint

    def mapOfProcesses(self):
        return self.processMap

    def printArray(self):
        return self.memory

    def processExists(self, letter):
        return letter in self.processMap  # Use 'in' to check for existence

    def removeProcess(self, letter):
        if letter in self.processMap:
            sz = self.processMap[letter][1]
            # Find the starting index of the process to remove
            startIndex = self.processMap[letter][0]
            self.memory[startIndex:startIndex + sz] = ["*" for _ in range(sz)]  # Free memory
            del self.processMap[letter]  # Remove from process map





class NextFit():
    def __init__(self):
        self.processMap = {}
        self.memory = [ "*" for _ in range(size) ]
    def insert(self, letter, sz):
        pass
    def mapOfProcesses(self):
        return self.processMap
    def printArray(self):
        return self.memory
    def processExists(self, letter):
        if self.processMap[letter]:
            return True
        return False
    def removeProcess(self, letter):
        pass


class FirstFit():
    def __init__(self):
        self.processMap = {}
        self.memory = [ "*" for _ in range(size) ]
    def insert(self, letter, sz):

        tempMap = {}
        start = -1
        counter = 0

        for i in range(len(self.memory)):
            if self.memory[i] == "*":
                if counter == 0:
                    start = i
                counter += 1
            else:
                if counter >= sz:
                    self.memory[start: start+sz] = [letter for _ in range(sz)]
                    self.processMap[letter] = [start, sz]
                    return start
                counter = 0
        
        if  counter >= sz:
                self.memory[start: start+sz] = [letter for _ in range(sz)]
                self.processMap[letter] = [start, sz]
                return start
        
        return None


        
    def mapOfProcesses(self):
        return self.processMap


    def printArray(self):
        return self.memory


    def processExists(self, letter):
        if self.processMap[letter]:
            return True
        return False


    def removeProcess(self, letter):
        if self.processMap[letter]:
            startpoint = self.processMap[letter][0]
            siize = self.processMap[letter][1]
            self.memory[startpoint:startpoint+siize] = ["*" for _ in range(siize)]
        else:
            print("No such process")



class WorstFit():
    def __init__(self):
        self.processMap = {}
        self.memory = ["*" for _ in range(size)]
    
    def insert(self, letter, sz):
        tempMap = {}
        start = -1
        counter = 0

        # Find all free blocks of memory
        for i in range(len(self.memory)):
            if self.memory[i] == "*":
                if counter == 0:
                    start = i
                counter += 1
            else:
                if counter >= sz:
                    tempMap[start] = counter
                counter = 0
        
        # Check the last block
        if counter >= sz:
            tempMap[start] = counter
        
        # Find the largest free block
        startKey = -1
        startVal = float('-inf')
        for key, val in tempMap.items():
            if val > startVal:  # Use > for Worst Fit
                startVal = val
                startKey = key
        
        if startKey == -1:
            return None
        
        # Fill the selected block with the process
        self.memory[startKey:startKey + sz] = [letter for _ in range(sz)]
        self.processMap[letter] = [startKey, sz]

        return startKey

    def mapOfProcesses(self):
        return self.processMap

    def printArray(self):
        return self.memory

    def processExists(self, letter):
        return letter in self.processMap  # Use 'in' to check for existence

    def removeProcess(self, letter):
        if letter in self.processMap:  # Use 'in' to check for existence
            startpoint = self.processMap[letter][0]
            size = self.processMap[letter][1]
            self.memory[startpoint:startpoint + size] = ["*" for _ in range(size)]
            del self.processMap[letter]  # Remove the process from processMap
        else:
            print("No such process")
