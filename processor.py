## processor.py
## Part of EECS 645 Project
## Zachary McGrath & Shogun Thomas

import sys

class Processor():
    def __init__(self, id):
        self.cache = [('i', 0) for x in range(512)]
        self.p_id = id
        
    def execute(self, rw, tag, index, offset): ##Focuses on PR and PW, returns (Bus_action, Flush (T/F), mem_addr)
        pass

    def change_state_bus(self, bus_sig, flush, address): ##Handles the bus tranactions, returns 
        pass

    def count_states(self):
        pass