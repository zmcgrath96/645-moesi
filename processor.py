## processor.py
## Part of EECS 645 Project
## Zachary McGrath & Shogun Thomas
import sys

bus_states = {
    'r': 'BusRd', 
    'rx': 'BusRdX',
    'u': 'BusUpgr'
}
# Class to hold processor cache and states
class processor():
    def __init__(self, id):
        self.cache = [('i', 0) for x in range(512)]
        self.p_id = id
        self.dirty_wbs = 0
        self.invalids = [0,0,0,0] #MOES
        
    # Given a Read or write operation and the state of the that cache value, return the bus action needed
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
                    # read
                    if rw == 0:
                        ret = None
                    # write
                    else:
                        ret = bus_states['u']
                    
            # exclusive state
            elif 'e' in state:
                # read
                if rw == 0:
                    ret = None
                # write
                else:
                    ret = None

            # shared state
            elif 's' in state:
                # read
                if rw == 0:
                    ret = None
                # write
                else:
                    ret = bus_states['u']

            # invalid state
            else:
                # read
                if rw == 0:
                    ret = bus_states['r']
                #write
                else:
                    ret = bus_states['rx']

        # if i don't have it, i need to request it
        else:
            that_state = self.cache[index][0]
            if 'm' in that_state or 'o' in that_state or 'e' in that_state:
                self.dirty_wbs += 1
             # read
            if rw == 0:
                ret = bus_states['r']
            #write
            else:
                ret = bus_states['rx']

        return ret

    # changing the state of the executing processor
    def change_state_rw(self, rw, index, shared, tag):
        current_state = self.cache[index][0]

        if 'm' in current_state: #Modified current_State (does nothing)
            return
        
        elif 'o' in current_state: #Owner current_State (only in write)
            if rw == 0:
                return
            else:
                self.cache[index] = ('m', tag)

        elif 'e' in current_state: #Exclusive current_state (only in write)
            if rw == 0:
                return 
            else:
                self.cache[index] = ('m', tag)
        
        elif 's' in current_state: #Shared current_State
            if rw == 0:
                return 
            else:
                self.cache[index] = ('m', tag)
        
        else: #Invalid State
            if rw == 0:
                if shared:
                    self.cache[index] = ('s', tag)
                else:
                    self.cache[index] = ('e', tag)
            else:
                self.cache[index] = ('m', tag)
                    
    # Given a bus signal, change the state of the data at the cache tag and index
    def change_state_bus(self, bus_sig, index, tag): ##Handles the bus tranactions
        # If its not the right tag, return so that we don't mess with that data
        if self.cache[index][1] != tag:
            return

        state = self.cache[index][0]
        if 'm' in state: ##MODIFIED STATE
            if bus_sig == bus_states['r']:
                self.cache[index] = ('o', tag)

            elif bus_sig == bus_states['rx']:
                self.dirty_wbs += 1
                self.cache[index] = ('i', tag)
                self.invalids[0] += 1

        elif 'o' in state: ##OWNER CASE
            if bus_sig == bus_states['rx']:
                self.dirty_wbs += 1
                self.cache[index] = ('i', tag)
                self.invalids[1] += 1

            elif bus_sig == bus_states['u']:
                self.cache[index] = ('i', tag)
                self.invalids[1] += 1
        
        elif 'e' in state: ##EXCLUSIVE CASE
            if bus_sig == bus_states['r']:
                self.cache[index] = ('s', tag)

            elif bus_sig == bus_states['rx']:
                self.cache[index] = ('i', tag)
                self.invalids[2] += 1

        elif 's' in state: ##SHARED CASE
            if bus_sig == bus_states['rx'] or bus_sig == bus_states['u']:
                self.cache[index] = ('i', tag)
                self.invalids[3] += 1

    # used for reporting the number of data in each state
    def count_states(self):
        ##Counts the total number of each state and puts them on the list
        state_list = [0, 0, 0, 0, 0]

        for x in self.cache:
            (s, _) = x

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

    # return the
    def get_state(self, index, tag):
        if self.cache[index][1] == tag:
            return self.cache[index][0]
        return 'i'