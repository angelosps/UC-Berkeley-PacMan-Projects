import heapq

class PriorityQueue(object):

    def __init__(self):
        self.heap = []                          # initialize the heap as an empty list
        self.itemrec = {}                       # items record for knowing which items are in the queue and their priorities
        self.count = 0                          # size of the Priority Queue. Initialized as zero

    def push(self, item, priority):
        if (self.itemrec.get(item) != None ):                       # if item already in the pq do not add it again
            raise KeyError('Item already in the priority queue')
        self.count += 1                                             # increase the size of priority queue        
        entry = [priority, item]                
        self.itemrec[item] = priority                               # assign the priority for the item
        heapq.heappush(self.heap, entry)                            # push the new entry(priority,item) in the heap

    def update(self, item, priority):
        if self.itemrec.get(item) != None and self.itemrec.get(item) > priority:    # if item is in the queue but with bigger "priority", 
            self.itemrec[item] = None                                               # set it as None temporarily in order to pass the "if" in push function and insert the item with the new priority in the pq
            self.push(item, priority)                                               # update its priority by pushing it again with the new (smaller) priority  
        elif self.itemrec.get(item) == None:                                        # if item is not in the queue, 
            self.push(item, priority)                                               # push it for first time with its priority

    def isEmpty(self):
        return self.count == 0                  # return True if size ("count") of PQ is 0, else False
    
    def pop(self): 
        if self.isEmpty():
            raise KeyError('pop from an empty priority queue')
        entry = heapq.heappop(self.heap)                # pop the next item
        self.count -= 1                                 # decrease queue size
        if self.itemrec.get(entry[1]) != 'POPPED':      # if item wasn't popped before (in case of priority update),
            self.itemrec[entry[1]] = 'POPPED'           # mark item as 'POPPED', so when the item with the "old" priority (bigger) found later, won't pop it again
            return entry[1]                             # return the popped item
       

def PQSort(list):
    q = PriorityQueue()         # initialize the Priority Queue
    for i in list:
        q.push(i, 0)            # push every element in the queue with the same priority in order to compare their values
    sorted_list = []            # initialize the sorted list
    while not q.isEmpty():      
        item = q.pop()          
        if item != None:       
            sorted_list.append(item)    # add the popped element in the end of the sorted list
    if q.isEmpty():                             # if the pq has emptied, i should clear the dictionary which, 
        q.itemrec.clear()                       # i keep record of the items of pq    
    return sorted_list
    

if __name__ == '__main__':                      # main function for testing the PQ
    q = PriorityQueue()
    q.push("task0", 0)
    q.push("task1", 1)
    q.push("task2", 2)
    q.push("task3", 3)                          # 0 1 2 3 
    q.update("task3", -1)                       # 3 0 1 2

    while not q.isEmpty():
        item = q.pop()
        if item != None:
            print(item)
    if q.isEmpty():                             # if the pq has emptied, i should clear the dictionary which, 
        q.itemrec.clear()                       # i kept record of the items of pq    

    print()
    
    q.push("task0", 0)
    q.push("task1", 1)
    q.push("task2", 2)
    q.push("task3", 3)                          # 0 1 2 3
    q.update("task2", -1)                       # 2 0 1 3
    q.update("task1", -5)                       # 1 2 0 3
    q.update("task0", -7)                       # 0 1 2 3

    while not q.isEmpty():
        item = q.pop()
        if item != None:
            print(item)
    if q.isEmpty():                             
        q.itemrec.clear()                   
    
    list = [0,3,1,2,5,4,6,9,8,7,10]
    
    print("\nThe list before sorting is: ")
    print(list)
    
    print("\nThe list after sorting with the priority queue: ")
    print(PQSort(list))