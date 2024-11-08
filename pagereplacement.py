class PageReplacement:
    def __init__(self, frames):
        self.frames = frames
        self.memory = []
        self.page_faults = 0

    def print_memory(self):
        print("Current Memory: ", self.memory)

    # FIFO Page Replacement Algorithm
    def fifo(self, pages):
        self.memory = []
        self.page_faults = 0
        print("\nFIFO Page Replacement:")
        
        for page in pages:
            if page not in self.memory:
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                else:
                    self.memory.pop(0)
                    self.memory.append(page)
                self.page_faults += 1
            self.print_memory()
        
        print(f"Total Page Faults (FIFO): {self.page_faults}")

    # LRU Page Replacement Algorithm
    def lru(self, pages):
        self.memory = []
        self.page_faults = 0
        recent_usage = []
        print("\nLRU Page Replacement:")
        
        for page in pages:
            if page not in self.memory:
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                else:
                    # Find the least recently used page and replace it
                    lru_page = recent_usage.pop(0)
                    self.memory.remove(lru_page)
                    self.memory.append(page)
                self.page_faults += 1
            else:
                # Move the accessed page to the most recently used position
                recent_usage.remove(page)

            recent_usage.append(page)
            self.print_memory()

        print(f"Total Page Faults (LRU): {self.page_faults}")

    # Optimal Page Replacement Algorithm
    def optimal(self, pages):
        self.memory = []
        self.page_faults = 0
        print("\nOptimal Page Replacement:")
        
        for i in range(len(pages)):
            page = pages[i]
            if page not in self.memory:
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                else:
                    # Find the page that won't be used for the longest period
                    future_use = []
                    for j in range(len(self.memory)):
                        if self.memory[j] not in pages[i+1:]:
                            future_use.append((self.memory[j], float('inf')))
                        else:
                            future_use.append((self.memory[j], pages[i+1:].index(self.memory[j])))
                    
                    # Replace the page that won't be used for the longest period
                    farthest_page = max(future_use, key=lambda x: x[1])[0]
                    self.memory.remove(farthest_page)
                    self.memory.append(page)
                self.page_faults += 1
            self.print_memory()

        print(f"Total Page Faults (Optimal): {self.page_faults}")


# Input and Testing
if __name__ == "__main__":
    # Example input
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    frames = 3
    
    pr = PageReplacement(frames)
    
    pr.fifo(pages)
    pr.lru(pages)
    pr.optimal(pages)
