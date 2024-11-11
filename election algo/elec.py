class ElectionAlgorithm:
    def __init__(self, processes):
        self.processes = processes  # Keep the original, non-ascending order
        self.coordinator = None

    def ring_election(self, initiator):
        print(f"Process {initiator} starts a Ring election.")
        
        # Initialize the election ring with the initiator
        election_ring = [initiator]
        current_index = self.processes.index(initiator)

        while True:
            # Find the next process in the ring
            next_index = (current_index + 1) % len(self.processes)
            next_process = self.processes[next_index]
            election_ring.append(next_process)
            print(f"Process {next_process} passes the election message: {election_ring}")
            
            # Move to the next process
            current_index = next_index

            # If we are back to the initiator, stop
            if next_process == initiator:
                break

        # Highest ID in the election_ring becomes the coordinator
        self.coordinator = max(election_ring)
        print(f"Ring Election complete. Process {self.coordinator} is the new coordinator.\n")

    def bully_election(self, initiator):
        print(f"Process {initiator} starts a Bully election.")
        
        # Find all processes with IDs higher than the initiator
        higher_processes = [p for p in self.processes if p > initiator]

        if not higher_processes:
            self.coordinator = initiator
            print(f"Process {initiator} becomes the coordinator as no higher process responded.")
        else:
            for process in higher_processes:
                print(f"Process {initiator} sends election message to Process {process}")
                if process > initiator:
                    print(f"Process {process} responds to election from Process {initiator}")
                    self.coordinator = process
                    self.bully_election(process)
                    return

        print(f"Bully Election complete. Process {self.coordinator} is the new coordinator.\n")

    def start_election(self, algorithm, initiator):
        if algorithm == "ring":
            self.ring_election(initiator)
        elif algorithm == "bully":
            self.bully_election(initiator)
        else:
            print("Invalid algorithm specified. Choose 'ring' or 'bully'.")

# Example usage
processes = [23, 11, 30, 15, 27]  # Processes with unique IDs in non-ascending order
election = ElectionAlgorithm(processes)

# Start Ring election with initiator 11
election.start_election(algorithm="ring", initiator=11)

# Start Bully election with initiator 23
election.start_election(algorithm="bully", initiator=23)
