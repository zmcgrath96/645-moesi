## processor.py
## Part of EECS 645 Project
## Zachary McGrath & Shogun Thomas
import sys

class processor():
    def __init__(self, id):
        self.cache = [('i', 0) for x in range(512)]
        self.p_id = id
        self.dirty_wbs = 0
        self.invalids = [0,0,0,0,0]
        
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

    def change_state_bus(self, bus_sig, index, address): ##Handles the bus tranactions, DOES THIS NEED THE ADDRESS and if so FOR WHAT
        state = self.cache[index][0]
        flush = False
        
        if 'm' in state: ##MODIFIED STATE
            if bus_sig == "BusRd":
                flush = True
                self.cache[index] = ('o', self.cache[index][1])

            elif bus_sig == "BusRdX":
                flush = True
                self.dirty_wbs += 1
                self.cache[index] = ('i', self.cache[index][1])

        elif 'o' in state: ##OWNER CASE
            if bus_sig == "BusRd":
                flush = True

            elif bus_sig == "BusRdX":
                flush = True
                self.dirty_wbs += 1
                self.cache[index] = ('i', self.cache[index][1])

            elif bus_sig == "BusUpgr":
                flush = False
                self.dirty_wbs += 1
                self.cache[index] = ('i', self.cache[index][1])
        
        elif 'e' in state: ##EXCLUSIVE CASE
            if bus_sig == "BusRd":
                flush = True
                self.cache[index] = ('s', self.cache[index][1])

            elif bus_sig == "BusRdX":
                flush = True
                self.cache[index] = ('i', self.cache[index][1])

        elif 's' in state: ##SHARED CASE
            if bus_sig == "BusRdX" or bus_sig == "BusUpgr":
                flush = False
                self.cache[index] = ('i', self.cache[index][1])
        
        else: ##INVALID CASE
            ##Has to check if other processors are in S or not
            pass
        
        return flush

    def count_states(self):
        ##Counts the total number of each state and puts them on the list
        state_list = [0, 0, 0, 0, 0]

        for x in self.cache:
            (s, num) = x

            if s == 'm': ##m state at index 0
                state_list[0] = state_list[0]+1

            elif s == 'o': ## o state at index 1
                state_list[1] = state_list[1]+1

            elif s == 'e': ## e state at index 2
                state_list[2] = state_list[2]+1

            elif s == 's': ##s state at index 3
                state_list[3] = state_list[3]+1

            else: ##i state at index 4
                state_list[4] = state_list[4]+1

        return state_list

    def get_state(self, index, tag):
        if self.cache[index][1] == tag:
            return self.cache[index][0]
        return 'i'