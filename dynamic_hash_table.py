from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.hash_table
        final_size = get_next_size()
        self.table_size = final_size
        if self.collision_type == "Chain":
            self.hash_table = [[] for i in range(final_size)]
            self.size = 0
            self.lst = []
            for i in range(len(old_table)):
                if old_table[i]:
                    for x in old_table[i]:
                        self.insert(x)
                        
        else:
            self.hash_table = [None]*(final_size)
            self.size = 0
            self.lst = []
            for key in old_table:
                if key != None:
                    self.insert(key)
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        old_table = self.hash_table
        final_size = get_next_size()
        self.table_size = final_size
        if self.collision_type == "Chain":
            self.hash_table = [[] for i in range(final_size)]
            self.size = 0
            self.lst = []
            for i in range(len(old_table)):
                if old_table[i]:
                    for x in old_table[i]:
                        self.insert(x)
        else:
            self.hash_table = [None]*(final_size)
            self.size = 0
            self.lst = []
            for key in old_table:
                if key != None:
                    self.insert(key)
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()