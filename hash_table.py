from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        # O(table_size)
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        if collision_type == "Chain":
            self.z,self.table_size = params
            self.hash_table = [[] for i in range(self.table_size)]
        elif collision_type == "Linear":
            self.z,self.table_size = params
            self.hash_table = [None]*(self.table_size)
        else:
            self.z,self.z2,self.c2,self.table_size = params
            self.hash_table = [None]*(self.table_size)
        self.size = 0
        self.lst = []
    
    def char_mapping(self,char):
        if 'a'<=char<='z':
            return ord(char) - ord('a')
        elif 'A'<=char<='Z':
            return ord(char) - ord('A') + 26
        return -1

    def modmul(self,a,b,n):
        return ((a%n)*(b%n))%n

    def modadd(self,a,b,n):
        return ((a%n)+(b%n))%n

    def hash1(self,key):
        ans = 0
        z_i = 1
        n = len(key)
        for i in range(n):
            temp = self.char_mapping(key[i])
            temp1 = self.modmul(z_i,temp,self.table_size)
            ans = self.modadd(temp1,ans,self.table_size)
            # print(ans)
            z_i = self.modmul(z_i,self.z,self.table_size)
        return ans
    
    def hash2(self,z,c2,key):
        ans = 0
        z_i = 1
        n = len(key)
        for i in range(n):
            temp = self.char_mapping(key[i])
            temp1 = self.modmul(z_i,temp,c2)
            ans = self.modadd(temp1,ans,c2)
            z_i = self.modmul(z_i,z,c2)
        ans = c2 - ans
        return ans

    def get_slot(self,key):
        return self.hash1(key)
    
    def get_load(self):
        return self.size/(self.table_size)
    
    def length(self):
        return self.size

    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
class HashSet(HashTable):
    # (key)
    def insert(self, key):
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if len(self.hash_table[slot]) == 0:
                self.hash_table[slot].append(key)
                self.size += 1
                self.lst.append(key)
            else:
                if key not in self.hash_table[slot]:
                    self.hash_table[slot].append(key)
                    self.size += 1
                    self.lst.append(key)
        elif self.collision_type == "Linear":
            # traverse the slot and if empty found not found and if the element is found ignore
            if self.size == self.table_size:
                raise Exception("Table is full")
            cnt = 0
            s = slot
            while self.hash_table[s]!=key and self.hash_table[s] != None :
                s = (s+1)%(self.table_size)
            if self.hash_table[s] == None:
                self.hash_table[s] = key
                self.size += 1
                self.lst.append(key)
        else:
            s = slot
            if self.size == self.table_size:
                raise Exception("Table is full")
            h2 = self.hash2(self.z2,self.c2,key)
            while self.hash_table[s]!=key and self.hash_table[s] != None :
                s = (s + h2)%(self.table_size)
                if s == slot:
                    raise Exception("Table is full")
            if self.hash_table[s] == None:
                self.hash_table[s] = key
                self.size += 1
                self.lst.append(key)
    
    def find(self, key):
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            return (key in self.hash_table[slot])

        elif self.collision_type == "Linear":
            # traverse the slot and if empty found not found and if the element is found ignore
            s = slot
            while self.hash_table[s] != None :
                if self.hash_table[s] == key:
                    return True
                s = (s+1)%(self.table_size)
                if s == slot:
                    return False
            return False
        else:
            h2 = self.hash2(self.z2,self.c2,key)
            s = slot
            while self.hash_table[s] != None :
                if self.hash_table[s] == key:
                    return True
                s = (s + h2) % self.table_size
                if s == slot:
                    break
            return False
    
    def __str__(self):
        ans = []
        if self.collision_type == "Chain":
            for key in self.hash_table:
                if not key:
                    ans.append("<EMPTY>") 
                else:
                    ans.append(" ; ".join(str(x) for x in key))
            return " | ".join(ans)
        else:
            for key in self.hash_table:
                if not key:
                    ans.append("<EMPTY>") 
                else:
                    ans.append(str(key))
            return " | ".join(ans)

    def get_list(self):
        ans = []
        if self.collision_type == "Chain":
            for i in range(len(self.hash_table)):
                if self.hash_table[i]:
                    for x in self.hash_table[i]:
                        ans.append(x)

        else:
            for x in self.hash_table:
                if x != None:
                    ans.append(x)
        return ans

    
class HashMap(HashTable):
    # (key,value) - unique value
    def insert(self, x):
        slot = self.get_slot(x[0])
        if self.collision_type == "Chain":
            if len(self.hash_table[slot]) == 0:
                self.hash_table[slot].append(x)
                self.size += 1
                self.lst.append(x)
            else:
                for y in self.hash_table[slot]:
                    if y[0] == x[0]:
                        return
                # key not there
                self.hash_table[slot].append(x)
                self.size += 1
                self.lst.append(x)

        elif self.collision_type == "Linear":
            # traverse the slot and if empty found not found and if the element is found ignore
            if self.size == self.table_size:
                raise Exception("Table is full")
            s = slot
            while self.hash_table[s] != None and self.hash_table[s][0]!=x[0]:
                s = (s+1)%(self.table_size)
            if self.hash_table[s] == None:
                self.hash_table[s] = x
                self.size += 1
                self.lst.append(x)
        else:
            s = slot
            if self.size == self.table_size:
                raise Exception("Table is full")
            h2 = self.hash2(self.z2,self.c2,x[0])
            s = slot
            while self.hash_table[s] != None and self.hash_table[s][0]!=x[0]:
                s = (s + h2)%(self.table_size)
                if s == slot:
                    raise Exception("Table is full")
            if self.hash_table[s] == None:
                self.hash_table[s] = x
                self.size += 1
                self.lst.append(x)
    
    def find(self, key):
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            for x in self.hash_table[slot]:
                if x[0] == key:
                    return x[1]
            return None

        elif self.collision_type == "Linear":
            s = slot
            while self.hash_table[s] is not None:
                if self.hash_table[s][0] == key:
                    return self.hash_table[s][1]
                s = (s+1) % self.table_size
                if s == slot:
                    return None
            return None
        else:
            h2 = self.hash2(self.z2, self.c2, key)
            s = slot
            while self.hash_table[s] is not None:
                if self.hash_table[s][0] == key:
                    return self.hash_table[s][1]
                s = (s + h2) % self.table_size
                if s == slot:
                    break
            return None

    def get_list(self):
        ans = []
        if self.collision_type == "Chain":
            for i in range(len(self.hash_table)):
                if self.hash_table[i]:
                    for x in self.hash_table[i]:
                        ans.append(x)

        else:
            for x in self.hash_table:
                if x != None:
                    ans.append(x)
        return ans

    def __str__(self):
        ans = []
        if self.collision_type == "Chain":
            for key in self.hash_table:
                if not key:
                    ans.append("<EMPTY>") 
                else:
                    ans.append(" ; ".join(f"({k},{v})" for k,v in key))
        else:
            for key in self.hash_table:
                if not key:
                    ans.append("<EMPTY>") 
                else:
                    ans.append(f"({key[0]},{key[1]})")
        return " | ".join(ans)