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

def Main():

    # Detect the shell prompt by getting all the text to the left
    # of the cursor.

    SendExpect(chr(13), "Press RETURN to get started")
    #SendExpect("n" + chr(13), "? [yes/no]:")
    SendExpect("en" + chr(13), ">")
    StackSet()
    StackSet()
    StackSet()
    StackSet()
    StackSet()
    StackSet()
    StackSet()
    StackSet()
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash:","#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-2:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-3:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-4:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-5:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-6:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-7:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-8:", "#")
    SendExpect("copy usbflash0:cat3k_caa-universalk9.16.03.05b.SPA.bin flash-9:", "#")


def StackSet():
    SendExpect("show switch", "#")
    FlashStatusText("Needs switch number/priority and switch data!!!")
    numberset = crt.Dialog.Prompt("Enter the switch that you wish to address from the switch stack:", "Enter", "Done", False)
    stackvar = crt.Dialog.Prompt("Enter switch number of switch" + numberset + "in stack shown above:", "Enter", "", False)
    if stackvar == "1":
        priorityvar == "15"
        FlashStatusText("Priority Set to 15 for switch 1 !!")
        return
    elif stackvar == "2":
        priorityvar == "14"
        FlashStatusText("Priority Set to 14 for switch 2 !!")
        return
    elif stackvar == "3":
        priorityvar == "13"
        FlashStatusText("Priority Set to 13 for switch 3 !!")
        return
    elif stackvar == "4":
        priorityvar == "12"
        FlashStatusText("Priority Set to 12 for switch 4 !!")
        return
    elif stackvar == "5":
        priorityvar == "11"
        FlashStatusText("Priority Set to 11 for switch 5 !!")
        return
    elif stackvar == "6":
        priorityvar == "10"
        FlashStatusText("Priority Set to 10 for switch 6 !!")
        return
    elif stackvar == "7":
        priorityvar == "9"
        FlashStatusText("Priority Set to 9 for switch 7 !!")
        return
    elif stackvar == "8":
        priorityvar == "8"
        FlashStatusText("Priority Set to 8 for switch 8 !!")
        return
    elif stackvar == "9":
        priorityvar == "7"
        FlashStatusText("Priority Set to 7 for switch 9 !!")
        return
    else:
        FlashStatusText("Invalid Text!")
        return


    SendExpect("switch " + numberset + " renumber" + stackvar, "#")
    SendExpect("y", "?[y / n]")
    

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
def Browse(strMessage, strButtonCaption, strDefaultPath, strFilter):
    strPlatform = sys.platform
    # Windows version of SecureCRT allows FileOpenDialog to return
    # a path to a file that doesn't yet exist... But Linux/Mac versions
    # of FileOpenDialog() require an existing file. So, use the nicer
    # interface in Windows, and on Linux/Mac, simply present an input
    # box that will allow for path to be changed, if desired. If you
    # are on Linux/Mac, and don't like the default path, simply change
    # the value of the g_strMyDocs variable (globally defined) as well
    # the value of the strSavedConfigsFolder variable defined
    # in Main() above.
    if strPlatform == "win32":
        return crt.Dialog.FileOpenDialog(
            strMessage,
            strButtonCaption,
            strDefaultPath,
            strFilter)
    else:
        return crt.Dialog.Prompt(
            strMessage,
            strButtonCaption,
            strDefaultPath)
Main()