## processor.py
## Part of EECS 645 Project
## Zachary McGrath & Shogun Thomas
import sys

class processor():
    def __init__(self, id):
        self.cache = [('i', 0) for x in range(512)]
        self.p_id = id
        
    def execute(self, rw, tag, index, offset): ##Focuses on PR and PW, returns bus_action
        ret = None

        # check to see if the tag at our index is our tag
        if self.cache[index][1] == tag:
            # check the state of our cache line
            state = self.cache[index][0]

            # modified state
            if 'm' in state:
                # if in the modified state, I don't have to do anything for read or write
                # no bus signal
                ret = None

            # owner state
            elif 'o' in state:
                    # if reading, no bus signal needed
                    if rw == 0:
                        ret = None
                    # if writing, need bus upgrd signal and change state to m
                    else:
                        ret = 'BusUpgr'
                        self.cache[index] = ('m', self.cache[index][1])
                    
            # exclusive state
            elif 'e' in state:
                # if reading, no change state needed, no bus signal
                if rw == 0:
                    ret = None
                # if writing, no bus signal, change to m state
                else:
                    ret = None
                    self.cache[index] = ('m', self.cache[index][1])

            # shared state
            elif 's' in state:
                # if reading, no state change, no bus signal
                if rw == 0:
                    ret = None
                #if writing, need to change to m state and bus upgr signal
                else:
                    ret = 'BusUpgr'
                    self.cache[index] = ('m', self.cache[index][1])

            # invalid state
            else:
                # can only read, should need to know if i'm going to shared or not
                pass

        # if i don't have it, i need to request it
        else:
            pass
        pass

    def change_state_bus(self, bus_sig, flush, address): ##Handles the bus tranactions, returns 
        pass

    def count_states(self):
        pass