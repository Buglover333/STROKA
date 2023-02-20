#                                _|                                
#  _|_|_|  _|    _|    _|_|_|  _|_|_|_|    _|_|    _|_|_|  _|_|    
#_|        _|    _|  _|_|        _|      _|    _|  _|    _|    _|  
#_|        _|    _|      _|_|    _|      _|    _|  _|    _|    _|  
#  _|_|_|    _|_|_|  _|_|_|        _|_|    _|_|    _|    _|    _|  
#                                                                  
#                    _|                  _|                                          
#_|      _|      _|      _|_|_|      _|_|_|    _|_|    _|      _|      _|    _|_|_|  
#_|      _|      _|  _|  _|    _|  _|    _|  _|    _|  _|      _|      _|  _|_|      
#  _|  _|  _|  _|    _|  _|    _|  _|    _|  _|    _|    _|  _|  _|  _|        _|_|  
#    _|      _|      _|  _|    _|    _|_|_|    _|_|        _|      _|      _|_|_|    
#



import curses
import pyperclip
import LinkedList as ll

#global variables
llist = ll.LinkedList()
pad = None
cursor = None
Win = None
bg = None
shaddow = None
header = None
header_shad = None
header_wid = 0
filler = ''
filler_h = ''
numbers = None
num_pad = None
num_list = []


class Window():
    def __init__(self, y, x, ygap, xgap):
        self.win = curses.newwin(y, x, ygap, xgap)
        self.ygap = ygap
        self.xgap = xgap
        
class Cursor():

    def __init__(self, Win, balance):
        self.maxy, self.maxx = Win.win.getmaxyx()
        self.y = 0
        self.x = 0
        self.dispx = 0
        self.dispy = 0
        self.balance = balance

    def right(self):
        current_node = llist.get_node(self.y + self.dispy)
        nodelen = len(current_node.data)
        if self.x < self.maxx - 1 and self.x < nodelen:
            self.x += 1
        elif self.balance == False and self.x + self.dispx < nodelen:
            self.dispx += 1
        else:
            try:
                nodelen > 0
                self.down()
                self.x = 0
            except:
                pass

    def left(self):
        current_node = llist.get_node(self.y + self.dispy)
        nodelen = len(current_node.data)
        if self.x > 0:
            self.x -= 1
        else:
            if self.dispx > 0:
                self.dispx -= 1
            else:
                self.x = nodelen % self.maxx
                self.up()

    def up(self):
        if self.y > 0:
            self.y -= 1
            current_node = llist.get_node(self.y + self.dispy)
            nodelen = len(current_node.data)
            try:
                if nodelen > 0:
                    self.dispx = nodelen // self.maxx * self.maxx
                    self.x = nodelen % self.maxx - 1
            except:
                self.x = nodelen
        elif len(llist.get_node(self.y + self.dispy).data) > 0 and self.dispy > 0:
            self.dispy -= 1
            self.x = 0
            self.dispx = 0

    def down(self):
        global llist
        if self.y < self.maxy - 1 and llist.get_len() - 1 > self.y and self.y + self.dispy < llist.get_len():
            self.y += 1
            current_node = llist.get_node(self.y + self.dispy)
            nodelen = len(current_node.data)
            try:
                if nodelen <= self.maxx and nodelen > 0:
                    self.x = nodelen - 1
                    self.dispx = 0
                else:
                    self.dispx = nodelen // self.maxx * self.maxx
                    self.x = nodelen % self.maxx
                    if self.x > 0:
                        self.x -= 1
            except:
                pass
        elif llist.get_len() > self.y and self.y + self.dispy < llist.get_len():
            self.dispy += 1
            self.dispx = 0
            try:
                self.x = nodelen - 1
            except:
                self.x = 0

##################################
#       editor functions         #
##################################

def insert(char, winx, balance):
    global llist, cursor
    try:
        char = chr(char)
    except:
        pass
    llist.insert_str(char, cursor.y + cursor.dispy, cursor.x + cursor.dispx, winx, balance)
    if char == '\n':
        cursor.down()
    else:    
        cursor.right()
    
def delete():
    global llist, cursor
    current_node = llist.get_node(cursor.y + cursor.dispy)
    llist.delete(cursor.y + cursor.dispy, cursor.x + cursor.dispx - 1)
    cursor.left()
    if ll.is_empty(llist.head.data) and cursor.y + cursor.dispy == 0:
        cursor.x = 0

#global for get_input
first_iter = True
second_iter = False
moving = False

#alt functions and more

down = ord('j')
up = ord('k')
right = ord('l')
left = ord('h')
tb = ord('\t')
def tab():
    for _ in range(4):
        insert(' ', winx, balance)

alt = 27
def ALT():
    ch = Win.win.getch()
    if ch == ord('s'):
        return llist.get_str()
    elif ch == ord('m'):
        return 'menu'
    try:
        fdict[ch]()
    except:
        pass

a = ord('a')
def ALTa():
    cursor.x = 0
    cursor.dispx = 0

q = ord('q')
def ALTq():
    cursor.dispy = 0
    cursor.y = 0
    cursor.x = len(llist.get_node(cursor.y + cursor.dispy).data) % cursor.maxx
    cursor.dispx = len(llist.get_node(cursor.y + cursor.dispy).data) // cursor.maxx * cursor.maxx

w = ord('w')
def ALTw():
    cursor.dispy = llist.get_len() - 1
    cursor.y = 0
    cursor.x = len(llist.get_node(cursor.y + cursor.dispy).data) % cursor.maxx
    cursor.dispx = len(llist.get_node(cursor.y + cursor.dispy).data) // cursor.maxx * cursor.maxx

o = ord('o')
def ALTo():
    llist.del_left(cursor.y + cursor.dispy, cursor.x + cursor.dispx)
    cursor.dispx = 0
    cursor.x = 0

p = ord('p')
def ALTp():
    llist.del_right(cursor.y + cursor.dispy, cursor.x + cursor.dispx)
    current_node = llist.get_node(cursor.y + cursor.dispy)
    if ll.is_empty(current_node.data):
        cursor.up()

v = ord('v')
def ALTv():
    clipboard_content = pyperclip.paste()
    for ch in clipboard_content:
        insert((ch), winx, balance) 
    char = ''

scl = ord('.')
def ALTscl():
    for _ in range(10):
        cursor.right()

scr = ord(',')
def ALTscr():
    for _ in range(10):
        cursor.left()

#global variables
#all the functions are collected in fdict. The fdcit is assembled in prep_editor()
action_ch = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN, alt, curses.KEY_BACKSPACE]
fdict = {}
char = None
ch = None
def get_input(stdscr, winy, winx, ygap, xgap, file_name, balance, add_header,add_numbers,  header_text, add_shaddow, text_color, border_color, header_color, num_color):
    global pad, cursor, bg, llist, shaddow, header, filler, first_iter, second_iter, numbers, num_pad, num_list, char, ch, fdict, action_ch
    bg.win.border()
    Win.win.keypad(True)
    if first_iter:
        char = ' '
        first_iter = False
        second_iter = True
    elif second_iter:
        #read document
        if file_name != None:
            with open(file_name, 'r+') as file:
                text = file.read()
                llist.open_doc(text)
        char = ' '
        second_iter = False
    else:    
        char = Win.win.getch()
    if char in action_ch:
        func = fdict[char]()
        if func != None:
            return func
    else: 
        insert(char, winx, balance)
    #buffer
    text = llist.make_buffer(cursor.y, cursor.dispy,cursor.maxy)
    padlen = llist.longest + 2
    buffersize = cursor.maxy + 2
    pad = curses.newpad(buffersize, padlen)
    longest = llist.longest
    pad.addstr(text, curses.color_pair(text_color))
    #shaddow
    if add_shaddow:
        init_shaddow(add_header)
    #header
    if add_header:
        init_header(header_text, header_color) 
    #refreshing everything
    bg.win.refresh()
    Win.win.refresh()
    pad.refresh(0, cursor.dispx, ygap, xgap, winy + ygap - 1, winx + xgap - 1)
    Win.win.move(cursor.y, cursor.x)
    #stdscr.refresh()
    pad.erase()
    #numbers
    if add_numbers: 
        num_list = llist.add_numbers(cursor.dispy, cursor.maxy)
        num_pad = curses.newpad(winy + 9, llist.longest_num)
        num_str = ''.join(num_list)
        num_pad.addstr(num_str, curses.color_pair(num_color))
        num_pad.refresh(0, 0, ygap, winx + xgap + 1, ygap + winy - 1, winx + xgap + llist.longest_num)
        num_pad.erase()

def prep_editor(stdscr, winy, winx, ygap, xgap, add_header, header_text, add_shaddow, text_color, border_color, shaddow_color,  balance):
    global pad, cursor, Win, bg, shaddow, header, header_wid, header_shad, filler, filler_h, llist, first_iter, fdict
    stdscr.erase()
    curses.curs_set(1)
    #bg fillers
    filler = ''
    filler_h = ''
    for _ in range(winy * (winx + 2)):
        filler += '█'
    for _ in range(3 * (winx + 2)):
        filler_h += '█'
    #adding a shaddo
    if add_shaddow:
        shaddow = Window(winy + 2, winx + 2, ygap + 2, xgap - 4)
        shaddow.win.bkgdset(' ', curses.color_pair(shaddow_color))
        header_shad = Window(4, winx + 2, ygap - 2, xgap - 4)
        header_shad.win.bkgdset(' ', curses.color_pair(shaddow_color))
    #adding a header
    if add_header:
        header = Window(3, winx + 2, ygap - 4, xgap - 1)
        header_wid = (winx // 2) - (len(header_text) // 2)
        header.win.bkgdset(' ', curses.color_pair(border_color))        
    #creating curses objects
    bg = Window(winy + 2, winx + 2, ygap - 1, xgap - 1)
    bg.win.bkgdset(' ', curses.color_pair(border_color))
    bg.win.idlok(False)
    bg.win.idcok(False)
    Win = Window(winy, winx, ygap, xgap)
    Win.win.bkgdset(' ', curses.color_pair(text_color))
    Win.win.idlok(False)
    bg.win.idcok(False)
    cursor = Cursor(Win, balance)
    colors(stdscr)
    fdict = {left: cursor.left, right: cursor.right, up: cursor.up, down: cursor.down, curses.KEY_RIGHT: cursor.right, curses.KEY_LEFT: cursor.left,
            curses.KEY_DOWN: cursor.down, curses.KEY_UP: cursor.up, curses.KEY_BACKSPACE: delete, tb: tab, q: ALTq, o: ALTo, p: ALTp, w: ALTw, v: ALTv, a: ALTa, scl: ALTscl, scr: ALTscr, alt: ALT}

###########################################
#       colors and customization          #
###########################################

def colors(scr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_RED)

def init_shaddow(add_header):
    shaddow.win.addstr(0, 0, filler)
    shaddow.win.noutrefresh()
    if add_header:
        header_shad.win.addstr(0, 0, filler_h)
        header_shad.win.noutrefresh()

def init_header(text, color):
    global header_wid, first_iter
    header.win.border() 
    header.win.addstr(1, header_wid, text, curses.color_pair(color))
    header.win.refresh()

####################################
#    custom window functions       #
####################################

def prep_alert(stdscr, winy, winx, ygap, xgap, message,  add_shaddow, shaddow_color, text_color):
    global Win, shaddow, filler
    filler = ''
    stdscr.erase()
    curses.start_color()
    colors(stdscr)
    curses.curs_set(0)
    Win = Window(winy, winx, ygap, xgap)
    Win.win.bkgdset(' ', curses.color_pair(text_color))
    Win.win.border()
    msg_x = winx // 2 - len(message) // 2
    Win.win.addstr(winy//2, msg_x, message)
    #shaddow
    for _ in range((winy - 1) * winx):
        filler += '█'
    if add_shaddow:
        shaddow = Window(winy, winx, ygap + 2, xgap - 3)
        shaddow.win.bkgdset(' ', curses.color_pair(shaddow_color))
        init_shaddow(False)
    Win.win.keypad(True)
    #input
    while True:
        ch = Win.win.getch()
        if ch == ord('\n'):
            break

option = 0
def prep_option(stdscr, ygap, xgap, header_text, options, add_shaddow, shaddow_color, text_color1, text_color2, header_color):
    global Win, shaddow, filler, option, header, header_shad, header_wid, filler_h
    filler = ''
    filler_h = ''
    stdscr.erase()
    curses.start_color()
    colors(stdscr)
    curses.curs_set(0)
    #window dimentions
    winy = len(options) + 2
    winx = 0
    for elem in options:
        if len(elem) > winx:
            winx = len(elem)
    if len(header_text) > winx:
        winx = len(header_text)
    winx += 2
    Win = Window(winy, winx, ygap, xgap)
    Win.win.bkgdset(' ', curses.color_pair(text_color1))
    Win.win.border()
    i = 0
    for elem in options:
        if i == option:
            color = text_color2
        else:
            color = text_color1
        Win.win.addstr(i + 1, 1, elem, curses.color_pair(color))
        i += 1
    #shaddow
    for _ in range((winy - 1) * (winx + 1)):
        filler += '█'
    for _ in range(3 * winx):
        filler_h += '█'
    if add_shaddow:
        shaddow = Window(winy - 1, winx + 2, ygap + 2, xgap - 2)
        shaddow.win.bkgdset(' ', curses.color_pair(shaddow_color))
        header_shad = Window(3, winx + 1, ygap - 2, xgap - 2)
        header_shad.win.bkgdset(' ', curses.color_pair(shaddow_color))
        init_shaddow(True)
    #header
    header = Window(3, winx, ygap - 3, xgap)
    header_wid = (winx // 2) - (len(header_text) // 2)
    header.win.bkgdset(' ', curses.color_pair(header_color))
    init_header(header_text, header_color)
    #input
    curses.noecho()
    Win.win.keypad(True)
    char = Win.win.getch()
    if char == curses.KEY_DOWN and option < (len(options) - 1):
        option += 1
    elif char == curses.KEY_UP and option > 0:
        option -= 1
    elif char == ord('\n'):
        return option

txt_dispy = 0
def prep_text(stdscr, winy, winx, ygap, xgap, text, text_color, add_shaddow, shaddow_color):
    global pad, Win, filler, shaddow, txt_dispy
    stdscr.erase()
    curses.start_color()
    colors(stdscr)
    curses.curs_set(0)
    longest = 0
    str_list = text.split('\n')
    for elem in str_list:
        elem += '\n'
        if len(elem) > longest:
            longest = len(elem)
    #shaddow
    for _ in range((winy - 1) * longest):
        filler += '█'
    if add_shaddow:
        shaddow = Window(winy, longest, ygap + 2, xgap - 3)
        shaddow.win.bkgdset(' ', curses.color_pair(shaddow_color))
        init_shaddow(False)
    Win = Window(winy, longest, ygap, xgap)
    Win.win.bkgdset(' ', curses.color_pair(text_color))
    Win.win.border()
    pad = curses.newpad(len(str_list), longest)
    pad.addstr(text)
    Win.win.refresh()
    pad.refresh(txt_dispy, 0, ygap + 1, xgap + 1, ygap + winy - 2, xgap + longest - 2)
    Win.win.keypad(True)
    pad.erase()
    filler = ''
    ch = Win.win.getch()
    if ch == curses.KEY_DOWN and txt_dispy < len(str_list) - winy + 1:
        txt_dispy += 1
    elif ch == curses.KEY_UP and txt_dispy > 0:
        txt_dispy -= 1
    elif ch == ord('q'):
        return False
    return True

curs_pos = 0
list_start = 0
def prep_optionsscrl(stdscr, winy, ygap, xgap, header_text, options, add_shaddow, shaddow_color, text_color1, text_color2, header_color):
    global Win, pad, header, filler, filler_h, shaddow, curs_pos, list_start,  header_shad, header_wid
    filler = ''
    filler_h = ''
    stdscr.erase()
    curses.start_color()
    colors(stdscr)
    curses.curs_set(0)
    longest = 0
    for elem in options:
        if len(elem) > longest:
            longest = len(elem)
    if len(header_text) > longest:
        longest = len(header_text)
    for _ in range((winy - 1) * (longest + 2)):
        filler += '█'
    for _ in range(3 * longest):
        filler_h += '█'
    pad = curses.newpad(len(options) + 3, longest + 3)
    for i in range(len(options)):
        if i == curs_pos + list_start:
            pad.addstr(options[i], curses.color_pair(text_color2))
            if options[i][-1] != '\n':
                pad.addstr('\n')
        else:
            pad.addstr(options[i], curses.color_pair(text_color1))
            if options[i][-1] != '\n':
                pad.addstr('\n')
    if add_shaddow:
        shaddow = Window(winy, longest + 2, ygap + 3, xgap - 2)
        shaddow.win.bkgdset(' ', curses.color_pair(shaddow_color))
        header_shad = Window(3, longest + 1, ygap - 2, xgap - 2)
        header_shad.win.bkgdset(' ', curses.color_pair(shaddow_color))
        init_shaddow(True)
    #header
    header = Window(3, longest + 2, ygap - 3, xgap)
    header_wid = (longest // 2) - (len(header_text) // 2) + 1
    header.win.bkgdset(' ', curses.color_pair(header_color))
    init_header(header_text, header_color)
    Win = Window(winy + 1, longest + 2, ygap, xgap)
    Win.win.bkgdset(' ', curses.color_pair(text_color1))
    Win.win.border()
    Win.win.noutrefresh()
    pad.refresh(list_start, 0, ygap + 1, xgap + 1, ygap + winy - 1, xgap + longest - 1)
    pad.erase()
    Win.win.keypad(True)
    ch = Win.win.getch()
    if ch == curses.KEY_UP:
        if curs_pos == 0 and list_start > 0:
            list_start -= 1
        elif curs_pos >= 1:
            curs_pos -= 1
    elif ch == curses.KEY_DOWN and list_start + curs_pos < len(options) - 1:
        if curs_pos == winy - 2:
            list_start += 1
        else:
            curs_pos += 1
    elif ch == ord('\n'):
        return options[list_start + curs_pos]


 
####################################
#         main functions           #
####################################

def editor(winy, winx, ygap, xgap, file_name=None, add_header=False, header_text='', add_numbers=False, add_shaddow=False, text_color=0, border_color=0, header_color=0, shaddow_color=0, num_color=3, balance=False, buffersize=300, buffersize_y=5000):
    curses.wrapper(prep_editor, winy, winx, ygap, xgap,  add_header, header_text, add_shaddow, text_color, border_color, shaddow_color, balance)
    e = None
    while e == None:
        e = curses.wrapper(get_input, winy, winx, ygap, xgap, file_name, balance, add_header, add_numbers, header_text, add_shaddow, text_color, border_color, header_color, num_color)
    return e

def alert(winy, winx, ygap, xgap, message,  add_shaddow=False, shaddow_color=0, text_color=0):
    curses.wrapper(prep_alert, winy, winx, ygap, xgap, message,  add_shaddow, shaddow_color, text_color)

def options(ygap, xgap, header='poll', options=['1', '2', '3'], add_shaddow=False, shaddow_color=0, text_color1=0, text_color2=1, header_color=0):    
    e = None
    while e == None:
        e = curses.wrapper(prep_option, ygap, xgap, header, options, add_shaddow, shaddow_color, text_color1, text_color2, header_color)
    return e

def text(winy, winx, ygap, xgap, text='', text_color=0, add_shaddow=False, shaddow_color=0):
    active = True
    while active:
        active = curses.wrapper(prep_text, winy, winx, ygap, xgap, text, text_color, add_shaddow, shaddow_color)

def optionsscrl(winy, ygap, xgap, header_text='', options=['11111', '22222', '333333333'], add_shaddow=False, shaddow_color=0, text_color1=0, text_color2=1, header_color=0):
    e = None
    while e == None:
        e = curses.wrapper(prep_optionsscrl, winy, ygap, xgap, header_text, options, add_shaddow, shaddow_color, text_color1, text_color2, header_color)
    return e
       

