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
def fninput(stdscr, message = '(hit Ctrl-G to send)'):
    curses.curs_set(1)
    stdscr.addstr(winy // 2 - 4, winx // 2 - 14 , message)
    bgwin = curses.newwin(5,32, winy // 2 - 4, winx // 2 - 20)
    bgwin.border()
    bgwin.refresh()
    editwin = curses.newwin(3,29, winy // 2 - 3, winx // 2 - 18)
    stdscr.refresh()
    box = Textbox(editwin)
    box.edit()
    message = box.gather()
    return message

######################
#      settings      #    
######################

config = []
with open('conf.txt') as file:
    file = file.read()
    config = file.split('\n')


DIRECTORY = None
TEXT_COLOR = None
HEADER_COLOR = None
BORDER_COLOR = None
SHADDOW_COLOR = None
NUM_COLOR = None
README = None
SHADDOW = None

def configure():
    global DIRECTORY, TEXT_COLOR, HEADER_COLOR, BORDER_COLOR, SHADDOW_COLOR, NUM_COLOR, README, SHADDOW 
    DIRECTORY = config[0][10::]
    TEXT_COLOR = int(config[1][11::])
    HEADER_COLOR = int(config[2][13::])
    BORDER_COLOR = int(config[3][13::]) 
    SHADDOW_COLOR = int(config[4][14::]) 
    NUM_COLOR = int(config[5][10::]) 
    README = int(config[6][7::])
    SHADDOW = int(config[7][8::])

configure()

settings = []
def change_setting(prefix1, prefix2, variable, pos1, pos2, limit):
    if variable < limit:
        variable += 1
    else:
        variable = 0
    settings[pos1] = prefix1 + str(variable)
    with open('conf.txt', '+r') as file:
        file_str = file.read()
    os.remove('conf.txt')
    with open('conf.txt', '+x') as file:
        file_list = file_str.split('\n')
        file_list[pos2] = prefix2 + str(variable)
        file.write('\n'.join(file_list))
    return variable

cur_path = DIRECTORY
def change_directory(path):
    global cur_path
    while path == None:
        path = curses.wrapper(fninput)
        try:
            f = open(path + 'tmp.txt', 'x')
            f.close()
            os.remove(path + 'tmp.txt')
            with open('conf.txt', '+r') as file:
                file_str = file.read()
            os.remove('conf.txt')
            with open('conf.txt', '+x') as file:
                file_list = file_str.split('\n')
                file_list[0] = 'DIRECTORY=' + path[:len(path) - 2:]
                file_str = '\n'.join(file_list)
                file.write(file_str)
            return path
        except:
            ch = cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'the path is incorrect, press Enter to retry', True)
            if ch:
                path = None
            else:
                return cur_path 
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
    global winx, winy, name, redacted, DIRECTORY, filename, longest, TEXT_COLOR, HEADER_COLOR, BORDER_COLOR, SHADDOW_COLOR, NUM_COLOR, README, SHADDOW, settings 
    
    ##################################
    #    choosing/creating a file    #
    ##################################
    
    ls_list = os.listdir(DIRECTORY)
    for elem in ls_list:
        if len(elem) > longest:
            longest = len(elem)
    ls_list.insert(0, 'NEW')
    choosing = True
    while choosing:
        filename = cw.optionsscrl(winy // 2, winy // 4, winx // 2 - longest // 2 - 3, '~|choose a file:|~', ls_list, True) 
        name = filename
        newname = None
        if filename == 'NEW':
            while newname == None:
                newname = curses.wrapper(fninput) 
                newname = newname.split('\n')
                newname = ''.join(newname)
                print(newname)
                try:
                    f = open(DIRECTORY + newname, '+x')
                    f.close()
                    name = newname
                    choosing = False
                except:
                    cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'file already exists, press Enter to retry', True)
        choosing = False
    active = True
    while active:
        configure()
        options = ['BACK', 'open', 'settings', 'save and quit ', 'just quit']
        longest_option = 0
        for option in options:
            if len(option) > longest_option:
                longest_option = len(option)
        settings = ['BACK', '> show readme on start: ' + str(README), '> shadow: ' + str(SHADDOW), '> directory: ' + str(DIRECTORY), 
                '> text color: ' + str(TEXT_COLOR), '> header color: ' + str(HEADER_COLOR), '> border color: ' + str(BORDER_COLOR), 
                '> shadow color: ' + str(SHADDOW_COLOR), '> numbers color: ' + str(NUM_COLOR)] 
        longest_setting = 0
        for setting in settings:
            if len(setting) > longest_setting:
                longest_setting = len(setting)
        
        #################################
        #     editing the document      #
        #################################
        
        path = DIRECTORY + name
        redacted, state, active, save = cw.editor(winy  - 6, winx - 12, 4, 5, path, True, name, True, SHADDOW, TEXT_COLOR, BORDER_COLOR, HEADER_COLOR, SHADDOW_COLOR, NUM_COLOR)
        
        ################################################################
        #    the menu (sorry for the nooddle code, I'm lazy (-_-) )    #
        ################################################################
        
        action = ''
        if state == 'menu':
            action = cw.optionsscrl(winy // 2, winy // 4, winx // 2 - longest_option // 2 - 3, 'options', options, True)
            if action == 'BACK':
                action = ''
                state = 'edit'
            elif action == 'open':
                newname = None
                while newname == None:
                    filename = cw.optionsscrl(winy // 2, winy // 4, winx // 2 - longest // 2 - 4, '~|choose a file:|~', ls_list, True) 
                    if filename == 'NEW':
                        while newname == None:
                            newname = curses.wrapper(fninput)
                            newname = newname.split('\n')
                            newname = ''.join(newname)
                            try:
                                f = open(DIRECTORY + newname, 'x')
                                f.close()
                                filename = newname
                            except:
                                cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'file already exists, press Enter to retry', True)
                                newname = None
                    else:
                        name = filename
                        break
            
            ########################
            #       settings       # 
            ########################
            
            elif action == 'save and quit ':
                save = True
                active = False
            elif action == 'just quit':
                active = False
                save = False
            elif action == 'settings':
                sett_state = True
                while sett_state:
                    action = cw.optionsscrl(winy // 2, winy // 4, winx // 2 - longest_setting // 2 - 3, 'settings', settings, True)
                    if action == 'BACK':
                        action = ''
                        sett_state = False
                    elif action ==  '> show readme on start: ' + str(README):
                        README = change_setting('> show readme on start: ', 'README=', README, 1, 6, 1)
                    elif action == '> shadow: ' + str(SHADDOW):
                        SHADDOW = change_setting('> shadow: ', 'SHADDOW=', SHADDOW, 2, 7, 1)                     
                    elif action == '> text color: ' + str(TEXT_COLOR):
                        TEXT_COLOR = change_setting('> text color: ','TEXT_COLOR=', TEXT_COLOR, 4, 1, 5)
                    elif action == '> header color: ' + str(HEADER_COLOR):
                        HEADER_COLOR = change_setting('> header color: ','HEADER_COLOR=', HEADER_COLOR, 5, 2, 5)
                    elif action == '> border color: ' + str(BORDER_COLOR):
                        BORDER_COLOR = change_setting('> border color: ','BORDER_COLOR=', BORDER_COLOR, 6, 3, 5)
                    elif action == '> shadow color: ' + str(SHADDOW_COLOR):
                        SHADDOW_COLOR = change_setting('> shadow color: ','SHADDOW_COLOR=', SHADDOW_COLOR, 7, 4, 5)
                    elif action == '> numbers color: ' + str(NUM_COLOR):
                        NUM_COLOR = change_setting('> numbers color: ','NUM_COLOR=', NUM_COLOR, 8, 5, 5)
                    elif action == '> directory: ' + str(DIRECTORY):
                        DIRECTORY = None
                        DIRECTORY = change_directory(DIRECTORY)

        ################################
        #       writing to a file      #
        ################################
        
        ch = ''
        if save == True:
            if action == 'save and quit ':
                ch = True
            else:
                ch = cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'do you want to save? (Enter/any key)', True)
            with open(DIRECTORY + name, 'w') as doc:
                if ch:
                    doc.truncate(0)
                    doc.write(redacted)
                if action != 'save and quit ':
                    ch = cw.alert(4, 43, winy // 2 - 3, winx // 2 - 21, 'saved.', True) 
            print('saved at: ' + path)

##################################
#             body               #
##################################
edit()
    


