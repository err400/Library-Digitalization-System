import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass

class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def merge(self,lst1,lst2):
        ans = []
        l = 0
        r = 0
        while l<len(lst1) and r<len(lst2):
            if lst1[l]<lst2[r]:
                ans.append(lst1[l])
                l += 1
            else:
                ans.append(lst2[r])
                r += 1
        while l<len(lst1):
            ans.append(lst1[l])
            l += 1
        while r<len(lst2):
            ans.append(lst2[r])
            r += 1
        return ans

    def merge_sort(self,lst):
        n = len(lst)
        if n <= 1:
            return lst
        mid = n//2
        lst1 = lst[:mid]
        lst2 = lst[mid:]
        lst1 = self.merge_sort(lst1)
        lst2 = self.merge_sort(lst2)
        return self.merge(lst1,lst2)

    def __init__(self, book_titles, texts):
        # O(kwlogw + klogk)
        books = []                             # tuple of (book_title,sorted_texts)   - wlogw
        for i in range(len(book_titles)):
            if not texts[i]:
                books.append((book_titles[i],[]))
            sorted_text = self.merge_sort(texts[i])
            lst = []                           # contains sorted unique words
            lst.append(sorted_text[0])
            for j in range(1,len(sorted_text)):
                if sorted_text[j-1] != sorted_text[j]:
                    lst.append(sorted_text[j])
            books.append((book_titles[i],lst))      

        self.books = books                     # length - k  - contains tuples(book_title,unique_sorted_texts)
        
        self.book_titles = self.merge_sort(book_titles)
        
        books_list = [0]*(len(book_titles))
        # for each book store it in the list
        for x in self.books:
            # do binary search on book_titles and find the index
            # insert into books_lst at that index - x[1]
            i = self.binary_search(self.book_titles,x[0])
            books_list[i] = x[1]
        self.books_list = books_list

    def binary_search(self,lst,target):
        n = len(lst)
        lo = 0
        hi = n-1
        while lo<=hi:
            mid = (lo+hi)//2
            if lst[mid] == target:
                return mid
            elif lst[mid]<target:
                lo = mid+1
            else:
                hi = mid-1
        return -1

    def distinct_words(self, book_title):
        # O(d+logk)
        # perform binary search to get the index of book_title and then go to the index of books_list and return 
        index = self.binary_search(self.book_titles,book_title)
        return self.books_list[index]
    
    def count_distinct_words(self, book_title):
        index = self.binary_search(self.book_titles,book_title)
        return len(self.books_list[index])
    
    def search_keyword(self, keyword):
        ans = []
        for i in range(len(self.book_titles)):
            index = self.binary_search(self.books_list[i],keyword)
            if index != -1:
                ans.append(self.book_titles[i])
        return ans
    
    def print_books(self):
        ans = ""
        for i in range(len(self.book_titles)):
            stri = ""
            stri += self.book_titles[i] + ": "
            for dword in self.books_list[i]:
                stri += dword
                stri += " | "
            ans += stri[:-3]
            ans += "\n"
        print(ans[:-1])

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    # two hash tables - one global
    # one for each table - stores only distinct words
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.params = params
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        else:
            self.collision_type = "Double"
        self.global_hash = ht.HashMap(self.collision_type,params)
        # global_hash : key - book_title   value - hash map of the words
    
    def add_book(self, book_title, text):
        # O(w+table_size)
        # create a hashset of words with the same parameters and collision_type
        temp_book_hash = ht.HashSet(self.collision_type,self.params)  # stores only distinct words
        for word in text:
            temp_book_hash.insert(word)
        self.global_hash.insert((book_title,temp_book_hash))
        
    def distinct_words(self, book_title):
        x = self.global_hash.find(book_title)
        if x != None:
            return x.get_list()
        else:
            return []
    
    def count_distinct_words(self, book_title):
        x = self.global_hash.find(book_title)
        return x.size
    
    def search_keyword(self, keyword):
        # O(k)
        ans = []
        for x in self.global_hash.lst:
            flag = x[1].find(keyword)
            if flag:
                ans.append(x[0])
        return ans

    def print_books(self):
        ans = ""
        if self.collision_type == "Chain":
            for book in self.global_hash.lst:
                stri = ""
                stri += book[0] + ": "
                stri += book[1].__str__()
                ans += stri
                ans += "\n"
        else:
            for book in self.global_hash.lst:
                stri = ""
                stri += book[0] + ": "
                stri += book[1].__str__()
                ans += stri
                ans += "\n"
        print(ans[:-1])
        