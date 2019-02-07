#$language = "Python"
#$interface = "1.0"
# interpreter for SecureCRT terminal

###################################
# Author:       Joshua Gould
# Organization: Rowan University
# Created:      Jan. 31, 2019
# Updated:      Deb. 7, 2019
###################################
#
# Description
# Sets stack configuration for switch to organize the stack
#
# INSTRUCTIONS
#
# 1. In SecureCRT or a like Console terminal, open Scripts > Run
# 2. Navigate in file manager to select scripts
# 3. Reach initial condition in connected terminal
# 4. Address number of switches in stack into prompt
# 5. Fill prompt with the number of the switch from the "show switch" command that you wish to address
# 6. Fill next prompt with switch number change
# 7. Priority and order is populated.


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

global objTab
objTab = crt.GetScriptTab()
objTab.Screen.Synchronous = True

SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True

def Main():

    crt.Screen.WaitForString (">")                       #initial condition statements to approach enable state
    crt.Screen.Send ("en" + chr(13))                     #and enter show switch command for user
    crt.Screen.WaitForString("#")
    crt.Screen.Send("show switch" + chr(13))

    delay(.1)                                            #function to show switch before prompt (delays 100ms)

    crt.Screen.Send(chr(13))
    NumberSet()                                          #function that sets number of times to run StackSet()

    crt.Screen.Send(chr(13))
    crt.Screen.Send("show switch" + chr(13))
    objTab.Session.SetStatusText("Stack changes made!")

    reloadsw()




def reloadsw():
    crt.Screen.WaitForString("#")
    crt.Screen.Send("reload" + chr(13))
    crt.Screen.WaitForString("[confirm]")
    crt.Screen.Send(chr(13))

    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def delay(seconds):
        crt.Screen.WaitForString("#")
	return time.sleep(seconds)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def NumberSet():            #runs command for number of switches provided in stack
    #possible improvements can read output of sh sw, address VER mismatch, and determine num of switches
    delay(1)
    numOswitch = crt.Dialog.Prompt("How many switches are in the stack? (1-9):", "Enter", "", False)


    intNum = int(numOswitch)

    if numOswitch == [1, 9]:

    for x in range(0,intNum):
        StackSet()

    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
