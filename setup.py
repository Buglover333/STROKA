import os
import getpass
import subprocess

user = getpass.getuser()

path = os.path.abspath('/home/' + user + '/.bashrc')
with open(path, 'a') as f:
    f.write("alias stroka='cd /home/" + user + "/Downloads/STROKA/ && python3 stroka.py $1'")
    print(path)

subprocess.run(['bash'])
print('alias "stroka"  have been created in your local .bashrc file.')
