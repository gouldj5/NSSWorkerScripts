#$language = "Python"
#$interface = "1.0"

import re
import datetime
import os
import platform
import shutil
import sys
import time
import subprocess

MsgBox = crt.Dialog.MessageBox
Prompt = crt.Dialog.Prompt
import time

global g_strConfigToSave
g_strConfigToSave = "running"
global g_strAdditionalArgs
g_strAdditionalArgs = ""

strHome = os.path.expanduser("~")
global g_strMyDocs
g_strMyDocs = strHome.replace("\\", "/") + "/Documents"

global objTab
objTab = crt.GetScriptTab()
objTab.Screen.Synchronous = True

SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True

def Main():

    # Detect the shell prompt by getting all the text to the left
    # of the cursor.

    #SendExpect(chr(13), "Press RETURN to get started")

    #crt.Screen.WaitForString("? [yes/no]:")
    #crt.Screen.Send("n" + chr(13))

    crt.Screen.WaitForString (">")
    crt.Screen.Send ("en" + chr(13))
    crt.Screen.WaitForString("#")
    crt.Screen.Send("show switch" + chr(13))
    delay(1)
    crt.Screen.Send(chr(13))


    NumberSet()
    crt.Screen.Send(chr(13))
    crt.Screen.Send("show switch" + chr(13))
    objTab.Session.SetStatusText("Stack changes made!")


    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash:","#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-2:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-3:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-4:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-5:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-6:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-7:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-8:", "#")
    #SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-9:", "#")


def delay(seconds):
        crt.Screen.WaitForString("#")
	return time.sleep(seconds)

def NumberSet():
    delay(1)
    numOswitch = crt.Dialog.Prompt("How many switches are in the stack? (1-9):", "Enter", "", False)
    intNum = int(numOswitch)

    for x in range(0,intNum):
        StackSet()

    return

def StackSet():
    # type: () -> object
    numberset = crt.Dialog.Prompt("Enter the switch that you wish to address from the switch stack command:", "Enter", "", False)
    stackvar = crt.Dialog.Prompt("Enter which switch number from " + numberset + " in stack you would like to change to:", "Enter", "", False)
    FlashStatusText("Set switch number/priority and switch data!!!")
    if stackvar == "1":
        priorityvar = "15"

        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to 15 for Switch 1 !!")
        return
    elif stackvar == "2":
        priorityvar = "14"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to 14 for Switch 2 !!")
        return
    elif stackvar == "3":
        priorityvar = "13"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to 13 for Switch 3 !!")
        return
    elif stackvar == "4":
        priorityvar = "12"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    elif stackvar == "5":
        priorityvar = "11"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    elif stackvar == "6":
        priorityvar = "10"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    elif stackvar == "7":
        priorityvar = "9"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    elif stackvar == "8":
        priorityvar = "8"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    elif stackvar == "9":
        priorityvar = "7"
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " renumber " + stackvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))
        crt.Screen.WaitForString("#")
        crt.Screen.Send("switch " + numberset + " priority " + priorityvar + chr(13))
        crt.Screen.WaitForString("[y/n]? [yes]:")
        crt.Screen.Send("y" + chr(13))

        FlashStatusText("Priority set to " + priorityvar + " for Switch " + numberset + "!!")
        return
    else:
        FlashStatusText("Continue...")
        return

    crt.Screen.WaitForString("#")
    crt.Screen.Send("switch " + numberset + " renumber" + stackvar)
    crt.Screen.WaitForString("?[y / n]")
    crt.Screen.Send("y")
    return

    

def SendExpect(send, expect):
	# Returns true if the text in 'send' was successfully sent and the
	# text in 'expect' was successfully found as a result.

	# If we're not connected, we can't possibly return true, or even
	# send/recv text
	if not SCRIPT_TAB.Session.Connected:
		return

	SCRIPT_TAB.Screen.Send(send + '\r')
	SCRIPT_TAB.Screen.WaitForString(expect)

	return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def GetHostname():
    strPrompt = GetTextLeftOfCursor()
    objMatch = re.match(r'^([0-9a-zA-Z\_\-\.]+)', strPrompt)
    if objMatch:
        return objMatch.group(1)
    else:
        FlashStatusText("No match on hostname pattern!")
        return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def GetTextLeftOfCursor():
    global objTab
    nRow = objTab.Screen.CurrentRow
    nCol = objTab.Screen.CurrentColumn - 1
    strTextLeftOfCursor = objTab.Screen.Get(nRow, 1, nRow, nCol)
    return strTextLeftOfCursor


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def FlashStatusText(strMsg):
    global objTab
    nShortPause = 200
    nLongPause = 400
    for i in range(1,5):
        objTab.Session.SetStatusText(strMsg)
        crt.Sleep(nLongPause)
        objTab.Session.SetStatusText("")
        crt.Sleep(nShortPause)

    objTab.Session.SetStatusText(strMsg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Main()
