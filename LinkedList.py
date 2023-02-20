#_|        _|            _|                        _|  
#_|            _|_|_|    _|  _|      _|_|      _|_|_|  
#_|        _|  _|    _|  _|_|      _|_|_|_|  _|    _|  
#_|        _|  _|    _|  _|  _|    _|        _|    _|  
#_|_|_|_|  _|  _|    _|  _|    _|    _|_|_|    _|_|_|  
#
#_|        _|              _|      
#_|              _|_|_|  _|_|_|_|  
#_|        _|  _|_|        _|      
#_|        _|      _|_|    _|      
#_|_|_|_|  _|  _|_|_|        _|_|  

import string

class Node():
    def __init__(self, data=None, pos = 0):
        global index
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.end = None
        self.longest = 0
        self.longest_num = 2

    def add_end(self, data):
        self.node = Node(data)
        if self.end is not None:
            self.end.next = self.node
            self.node.prev = self.end
            if self.end == self.head:
                self.head.next = self.node
            self.end = self.node
        else:
            self.end = self.node
            self.head = self.node

    def add_head(self, data):
        self.node = Node(data)
        if self.head is not None:
            self.head.prev = self.node
            self.node.next = self.head
            if self.head == self.end:
                self.end.prev = self.node
        else:
            self.end = self.node
        self.head = self.node

    def pop_end(self):
        self.end.prev.next = None
        self.end = self.end.prev

    def pop_head(self):
        self.head.next.prev = None
        self.head = self.head.next

    def insert(self, data, pos):
        self.new_node = Node(data)
        llen = self.get_len()
        self.current_node = None
        if pos >= llen:
            self.add_end(self.new_node.data)
            return
        if pos <= 0:
            self.add_head(self.new_node.data)
            return
        if pos < llen // 2:
            self.current_node = self.head
            for i in range(pos):
                self.current_node = self.current_node.next
        else:
            self.current_node = self.end
            for i in range(llen - pos - 1):
                self.current_node = self.current_node.prev
        self.new_node.next = self.current_node
        if self.current_node.prev == None:
            self.add_head(' ')
        self.new_node.prev = self.current_node.prev                                                                                                 
        self.current_node.prev.next = self.new_node
        self.current_node.prev = self.new_node
    
    def pop(self, pos):
        llen = self.get_len()
        if pos <= 0:
            self.pop_head()
            return
        if pos >= llen:
            self.pop_end()
            return
        if pos < llen // 2:
            self.current_node = self.head
            for i in range(pos):
                self.current_node = self.current_node.next
        else:
            self.current_node = self.end
            for i in range(llen - pos):
                self.current_node = self.current_node.prev
        self.current_node.prev.next = self.current_node.next
        self.current_node.next.prev = self.current_node.prev
        self.current_node.prev = None
        self.current_node.next = None

    def print_forward(self):
        printable = self.head
        print(self.head.data.replace('\n', '*'))
        while True:
            try:
                printable = printable.next
                print(printable.data.replace('\n', '*'))
            except:
                break
    
    def print_reverse(self):
        printable = self.end
        print(self.end.data)
        while True:
            try:
                printable = printable.prev
                print(printable.data)
            except:
                break
    
    def get_len(self):
        self.current_node = self.head
        llen = 0
        while True:
            try:
                self.current_node = self.current_node.next
                llen += 1
            except:
                return llen
   
    def longest_node(self, node_index):
        try:
            cur_node_len = len(self.get_node(node_index).data)
        except:
            cur_node_len = 10
        if cur_node_len > self.longest:
            self.longest = cur_node_len
        return self.longest

    def get_str(self):
        self.clear_top()
        self.clear_bottom()
        data_str = ''
        self.current_node = self.head
        while True:
            try:
                data_str += self.current_node.data
                self.current_node = self.current_node.next
            except:
                return data_str

    def make_buffer(self, y, dispy,  maxy):
        self.longest = 0
        current_node = self.get_node(dispy)
        text = ''
        for _ in range(maxy):
            try:
                text += current_node.data
                if len(current_node.data) > self.longest:
                    self.longest = len(current_node.data)
                current_node = current_node.next
            except:
                pass
        return text

    def add_numbers(self, dispy, maxy):
        num_list = []
        current_node = self.get_node(dispy)
        for i in range(dispy, dispy + maxy):
            num_list.append(str(i) + '\n')
            if len(str(i)) + 1 > self.longest_num:
                self.longest_num = len(str(i)) + 1
        return num_list

    def get_node(self, node_index):
        llen = self.get_len()
        self.current_node = None
        if node_index < llen // 2:
            self.current_node = self.head
            for i in range(node_index):
                self.current_node = self.current_node.next
        else:
            self.current_node = self.end
            for i in range(llen - node_index - 1):
                self.current_node = self.current_node.prev
        return self.current_node
    
    def get_index(self, node):
        current_node = self.head
        index = 0
        if node != current_node:
            current_node = current_node.next
            index += 1
        return index
    
    def open_doc(self, doc):
        split_text = doc.split('\n')
        self.add_end(split_text[0])
        split_text.pop(0)
        for line in split_text:
            self.add_end(line + '\n')
            if len(line) > self.longest:
                self.longest = len(line)

    def insert_str(self, text, node_index, init_pos, limit = 20, bal = False):
        starting_node = self.get_node(node_index)
        try:
            cur_node_len = len(starting_node.data) 
        except:
            cur_node_len = 2
        if self.get_len() == 0:
            self.add_end('')
        chr_pos = init_pos
        self.current_node = self.get_node(node_index) 
        text = text[::-1]
        for char in text:
            if self.current_node == None:
                self.add_end
                self.current_node = self.end
            if char == '\n':
                temp_list = list(self.current_node.data)
                temp_list.insert(chr_pos, char)
                temp_str = ''.join(temp_list)
                temp_list = temp_str.split('\n')
                self.current_node.data = temp_list[0] + '\n'
                if len(temp_list) > 2:
                    for elem in range(len(temp_list) - 1):
                       temp_list[elem] += '\n'
                    temp_list.pop(0)
                    temp_str = ''.join(temp_list)
                else:
                    temp_str = temp_list[1]
                self.insert(temp_str, node_index + 1)
                chr_pos = 0
                self.current_node = self.get_node(node_index)
            else:
                temp_list = list(self.current_node.data)
                temp_list.insert(chr_pos, char)
                self.current_node.data = ''.join(temp_list)
                self.current_node = self.get_node(node_index)
                self.add_missing_newlines(self.get_node(node_index), limit)
                self.clear_bottom()
                self.remove_empty(starting_node, text.count('\n'))
                self.clear_top()
            #if bal:
            #    self.balance(self.current_node, limit)
            #    #self.add_missing_newlines(self.get_node(node_index), limit)
    
    def delete(self, node_index, chr_pos):
        current_node = self.get_node(node_index)
        node_empty = is_empty(current_node.data)
        if self.get_len() <= 1 and node_empty:
            return 0
        temp_list = list(current_node.data)
        if len(temp_list) > 0 and  chr_pos <= len(temp_list) - 1:
            if temp_list[chr_pos] == '\n' or node_empty:
                temp_list.pop(chr_pos)
                try:
                    nodelen = len(current_node.next.data)
                    if nodelen > 0 and current_node != self.head:
                        current_node.data = ''.join(temp_list) + current_node.next.data
                        self.pop(node_index + 2) 
                except:
                    pass
            else:
                temp_list.pop(chr_pos)
                current_node.data = ''.join(temp_list)

    def del_left(self, node_index, chr_pos):
        current_node = self.get_node(node_index)
        temp_list = list(current_node.data)[chr_pos::]
        current_node.data = ''.join(temp_list)
        if is_empty(current_node.data):
            try:
                self.pop(node_index + 1)
            except:
                pass

    def del_right(self, node_index, chr_pos):
        current_node = self.get_node(node_index)
        temp_list = list(current_node.data)[:chr_pos:]
        current_node.data = ''.join(temp_list)
        if is_empty(current_node.data):
            try:
                self.pop(node_index)
            except:
                pass

    def clear_bottom(self):
        current_node = self.end
        try:
            while current_node.data == None or is_empty(current_node.data):
                current_node = current_node.prev()
                self.pop_end()
        except:
            pass

    def balance(self, starting_node, limit):
        looping_node = starting_node
        looping_temp_list = list(looping_node.data)
        while len(looping_temp_list) >= limit:
            if looping_node.next is None:
                self.add_end('')
            if len(looping_temp_list) == limit:
                looping_node = looping_node.next
                looping_temp_list = list(looping_node.data)
            else:
                temp_list_next = list(looping_node.next.data)
                len_next = len(temp_list_next)
                insertable = looping_temp_list[-1]
                if insertable == '\n':
                    self.insert('\n', self.get_index(looping_node) + 1)
                    looping_temp_list.pop(-1)
                    looping_node.data = ''.join(looping_temp_list)
                elif len_next > 1 and temp_list_next[len_next - 1] == '\n' and len_next >= limit:                  
                    temp_list_next.insert(0, insertable)
                    looping_temp_list.pop(-1)
                    temp_list_next.pop(-1)
                    looping_node.data = ''.join(looping_temp_list)
                    looping_node.next.data = ''.join(temp_list_next)
                    self.insert('\n', self.get_index(looping_node) + 2)
                else:
                    temp_list_next.insert(0, insertable)
                    looping_temp_list.pop(-1)
                    looping_node.data = ''.join(looping_temp_list)
                    looping_node.next.data = ''.join(temp_list_next)
                 
    def add_missing_newlines(self, starting_node, limit):
        current_node = starting_node
        try:
            while len(current_node.data) > 0:
                if len(current_node.data) < limit - 3 and current_node.data[-1] != '\n':
                    current_node.data += '\n'
                current_node = current_node.next
        except:
            pass

    def remove_empty(self, changed_node, buffer_size):
        node_index = self.get_index(changed_node)
        index = node_index - 10
        current_node = self.get_node(index)
        for i in range(buffer_size):
            try:
                if current_node.data == None or current_node.data == '' or is_empty(current_node.data):
                    current_node = current_node.next
                    self.pop(index + i)
            except:
                pass

    def clear_top(self):
        current_node = self.head
        try:
            while is_empty(current_node.data):
                current_node = current_node.next
                self.pop(self.get_index(current_node.prev))
        except:
            pass

def is_empty(text):
    extra = 0
    for char in text:
        if char not in string.ascii_letters:
            extra += 1
    if extra == len(text):
        return True
    return False
