__author__ = "Ricard Lado"
__copyright__ = "Copyright 2020, Lado"
__credits__ = ["Ricard Lado"]
__license__ = "GPLv3"


class looping_list:
    '''
    List of fixed size that appends over the oldest element in the list.
    '''
    def __init__(self,length):
        self.list=[0]*length
        self.idx=0
    
    def __len__(self):
        return len(self.list)
    
    def append(self,item):
        if self.idx>len(self)-1:
            self.idx=0
        self.list[self.idx]=item
        self.idx+=1