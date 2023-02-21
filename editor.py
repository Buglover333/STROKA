import custom_windows as cw
import curses
import os

#getting screen dimentions
def get_dimentions(stdscr):
    winy, winx = stdscr.getmaxyx()
    return winy, winx
winy, winx = curses.wrapper(get_dimentions)

import curses
from curses.textpad import Textbox, rectangle


#input filename
def fninput(stdscr):
    curses.curs_set(1)
    stdscr.addstr(winy // 2 - 3, winx // 2 - 18 , "Enter filename: (hit Ctrl-G to send)")
    editwin = curses.newwin(2,30, winy // 2 - 2, winx // 2 - 15)
    stdscr.refresh()
    box = Textbox(editwin)
    box.edit()
    message = box.gather()
    return message

#settings
config = []
with open('conf.txt') as file:
    file = file.read()
    config = file.split('\n')

DIRECTORY = config[0][10::]
TEXT_COLOR = config[1][11::]
HEADER_COLOR = config[2][13::]
README = config[3][7::]
SHADDOW = config[4][8::]
if SHADDOW == 1:
    SHADDOW = True
else:
    SHADDOW = False

#readme
with open('initmessage.txt') as file:
    file = file.read()
    y = winy - winy // 10
    if int(README) == 1:
        cw.text(y, winx, 1, winx // 2 - 37, file, 0, True, 0)

name = ''
filename = 0
longest  = 0
def edit():
    global name, redacted, DIRECTORY, filename, longest
    #choosing/creating a file
    ls_list = os.listdir(DIRECTORY)
    for elem in ls_list:
        if len(elem) > longest:
            longest = len(elem)
    ls_list.insert(0, 'NEW')
    filename = cw.optionsscrl(winy // 2, winy // 4, winx // 2 - longest, '~|choose a file:|~', ls_list, True) 
    name = filename
    newname = None
    if filename == 'NEW':
        while newname == None:
            newname = curses.wrapper(fninput) 
            try:
                f = open(DIRECTORY + newname, 'x')
                f.close()
                name = newname
            except:
                cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'file already exists, press Enter to retry', True)
                newname = None
    
    #editing the document
    redacted = cw.editor(30, winx - 12, 4, 5, DIRECTORY + name, True, name, True, False)
  

    #triggering the menu
    if redacted == 'menu':
        return 'menu'

    #writing to a file
    with open(DIRECTORY + name, 'w') as doc:
        cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'do you want to write out?', True)
        doc.truncate(0)
        doc.write(redacted)
    return 'written'

state = 'edit'
while state != 'menu':
    state = edit()

print(DIRECTORY + name)
#print(redacted)
#print(DIRECTORY + name)
    


