from pydblite.pydblite import Base


class MemoryQueue(object):
    
    def __init__(self, name = "", col_names = ['col']):
        self.db = Base(name, save_to_file = False)
        self.db.create(*col_names)
        self.st = 0
        self.en = 0

    def pop(self):

        if(self.st == self.en):
            print('Queue Empty')

        ret = self.db[self.st]

        del self.db[self.st]
        self.st += 1

        return ret

    def top(self):

        if(self.st == self.en):
            print('Queue Empty')

        ret = self.db[self.st]

        return ret

    def push(self, arg = ['']):
        
        self.db.insert(*arg)
        self.en += 1

    def print_queue(self):

        for r in self.db:
            print(r)

    def is_empty(self):
        return self.st == self.en


class MemoryDict(object):

    def __init__(self, name = "", key = "", value = ['col']):

        self.db = Base(name, save_to_file = False)
        self.db.create(key, *value)
        self.db.create_index(key)
        self.key = key

    def insert(self, key = "", value = [""]):
        self.db.insert(key, *value)

    def give_me_elem(self, key):
        return eval('self.db._' + self.key + '[key]')

    def is_in(self, key):
        return self.give_me_elem(key) > 0

    def print_all(self):

        for r in self.db:
            print(r)