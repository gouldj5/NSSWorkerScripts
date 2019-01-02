# $language = "Python"
# $interface = "1.0"

# Cisco-SaveDeviceConfigToFile.py
#
#   Last Modified:
#      06 Apr, 2018
#         - Added support for additional Cisco command line args to be
#           specified as part of the button configuration so that one
#           can issue a wider variety of such commands, for example:
#              Cisco cmd                        SCRT button args
#              --------------------------------------------------------
#              sh run all   --------------->    running all
#              sh run interface Vlan 1 ---->    running int Vlan 1
#              sh start linenum ----------->    startup linenum
#
#      27 Jun, 2017
#         - Remove cross-platform code that relies on 'import platform'
#           and related functions (Windows XP is no longer a supported
#           platform, and CentOS 5 is old enough to be outside of the 80%
#           case).
#         - Use 'more system:running-config' form of the command instead
#           of 'show running-config' for ASA devices so that the resulting
#           output isn't masked (thanks to mike1572 in forum thread 12738
#           for the tip: https://forums.vandyke.com/showthread.php?t=12738).
#
#      06 Sep, 2016
#         - Handle ASA device's unique way of doing term things:
#              > Detect when we're in the ASA case (by output of
#                'sh term' using "Width = \d+," instead of Width:)
#              > Use [term pager 0], instead of [term len 0]
#              > Capture all output after sh run... or sh start...
#
#      29 Aug, 2016
#         - Account for shell prompts on ASA devices having a
#           space character after the # and where the cursor
#           ends up.
#         - Account for situations where the initial 'sh term'
#           command generates more output than can be displayed
#           on the current terminal size, resulting in a --more--
#           prompt that will need to be handled.
#
#      11 Apr, 2016
#         - Change GetHostname() function to have a regular
#           expression that allows digits and dots in the
#           host name. Prior versions didn't properly detect
#           hostnames with digits or dots in them.
#
#      19 Jan, 2016
#         - Initial version
#
# Description
#   Ever wanted to save a copy of your Cisco router's
#   running-config or startup-config so that you could have
#   something to compare against or restore to? If so, this
#   script is an example you can start with.
#
# Usage:
#   This same script saves either the running-config or the
#   startup-config, depending on the script argument that
#   is passed in.
#     - If there's no script argument at all, or if the
#       script argument is "running", the running-config is
#       saved.
#     - If script argument is "startup", the startup-config
#       is saved.
#
#   1) Map a button to run this script. Make sure the argument
#      field has "running" if you desire to save the running-
#      config, or "startup" if you desire to save the startup-
#      config.
#
#      If you aren't yet familiar with SecureCRT's button bar,
#      you can learn about it here:
#        https://www.vandyke.com/support/tips/button_bar.html
#
#      Watch the You Tube video about SecureCRT's button bar:
#        https://www.youtube.com/watch?v=olyCcUWRimI
#
#   2) Connect to your Cisco device and make sure you're in
#      enabled/privileged mode (the script makes a valiant
#      effort to detect this and provide a warning, if you're
#      not in privileged mode).
#
#
# Notes:
#   --> This script was tested on a Cisco 881W, a 2900 router,
#       a 2960 switch, and an ASA5510. Your mileage may vary on
#       other devices.
#   --> On all but ASA-type devices, the script sets term
#       length and width to allow for the entire config to
#       be displayed w/o any "more" prompts, then it
#       restores the pre-script term length and width
#       values. On ASA-type devices, the script uses the
#       'term pager 0' command instead of 'term len 0'.
#   --> Config files are saved to the user's Documents
#       folder, in a sub-folder named "Config-Saves".
#   --> Config files are named according to the following
#       pattern...
#
#          SessionName_RemoteAddress_TYPE-config_YYYYmmdd_HHMMSS.ttt.txt
#          ---------------------------------------------------------------------
#          ...where...
#          SessionName: Is the name of the session that's currently
#                       connected.
#        RemoteAddress: Is the IP address of the remote device to which
#                       you're connected.
#                 TYPE: Is either "running" or "startup", depending on
#                       the script argument you're passing in.
#                 YYYY: 4-digit year
#                   mm: 2-digit month
#                   dd: 2-digit day
#                   HH: 2-digit hours
#                   MM: 2-digit minutes
#                   SS: 2-digit seconds
#                  ttt: 3-digit milliseconds
#
#   --> If you're running this script on Windows, you'll see
#       a dialog prompting you to change (if desired) the name
#       and location of the file to be saved, followed by the
#       appearance of a Windows explorer that will appear once
#       the save is complete, with the file containing the
#       configuration selected in the Windows explorer view.

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Main():
    global g_strConfigToSave
    if crt.Arguments.Count > 0:
        strArg = str(crt.Arguments.GetArg(0)).lower()
    else:
        strArg = g_strConfigToSave

    if not (strArg == "running" or strArg == "startup"):
        MsgBox(
            "Unrecognized config type: '" + strArg + "'\r\n" +
            "Expected either 'running' or 'startup'.\r\n\r\n" +
            "Exiting.")
        return

    g_strConfigToSave = strArg

    global g_strAdditionalArgs
    if crt.Arguments.Count > 1:
        for nArgIndex in range(1, crt.Arguments.Count):
            strAddArg = str(crt.Arguments.GetArg(nArgIndex))
            if g_strAdditionalArgs == "":
                g_strAdditionalArgs = strAddArg
            else:
                g_strAdditionalArgs = "{0} {1}".format(g_strAdditionalArgs, strAddArg)

    if not objTab.Session.Connected:
        strMessage = "Connect and log into a terminal to run this script!"
        #FlashStatusText(strMessage)
        MsgBox(strMessage)
        return

    # Detect the shell prompt by getting all the text to the left
    # of the cursor.
    strPrompt = GetTextLeftOfCursor()
    if len(strPrompt) < 1:
        objTab.Screen.Send("\r")
        while objTab.Screen.WaitForCursor(1):
            objTab.Session.SetStatusText("Waiting for prompt...")

        strPrompt = GetTextLeftOfCursor()
        if len(strPrompt) < 1:
            FlashStatusText("No prompt detected! Press Enter first.")
            return

    # Attempt to check if we're in privileged/enable mode:
    if strPrompt.rstrip()[-1] != '#':
        FlashStatusText("Must  'enable'  first!")
        crt.Screen.Send("enable" + chr(13))
        crt.Screen.WaitForString("ssword:")
        passwd = crt.Dialog.Prompt("Enter password:", "Login", "", True)
        crt.Screen.Send(passwd + chr(13))
        return

    # Attempt to ensure we're not in (config) mode - bad place to
    # be in if running this script, right?
    strHostname = GetHostname()
    if "config)" in strPrompt:
        FlashStatusText("Not in priv EXEC mode... exiting.")
        crt.Screen.Send("exit" + chr(13))
        return


    bIsASADevice = False
    nColsOrig = crt.Session.Config.GetOption("Cols")

    objTab.Session.SetStatusText("Getting term info...")
    # Get Term size info
    objTab.Screen.Send("sh term\r")
    objTab.Screen.WaitForString("sh term")
    while True:
        objTab.Screen.WaitForStrings([strPrompt,
            "Width: ",
            "Length: ",
            "Width = ",
            "--More--", "-- More --", "--more--", "-- more --"])
        if objTab.Screen.MatchIndex == 1:
            # Found strPrompt. We're done looping
            break

        elif objTab.Screen.MatchIndex == 2:
            # Found "Width: "
            nCols = objTab.Screen.ReadString(" columns")

        elif objTab.Screen.MatchIndex == 3:
            # Found "Length: "
            nRows = objTab.Screen.ReadString(" lines")

        elif objTab.Screen.MatchIndex == 4:
            # Found "Width = ". This means we're on an ASA device
            bIsASADevice = True
            # Read the number of cols up to the ',' character
            nCols = objTab.Screen.ReadString(",")

        elif objTab.Screen.MatchIndex > 4:
            # This means that anything *but* the first 4
            # elements of vWaitFors was seen, so we need
            # to press SPACE to continue receiving output.
            objTab.Screen.Send(" ")
            continue

    if bIsASADevice:
        # ASA devices appear not to support modifying columns/width, so we'll
        # just turn off the pager...
        objTab.Session.SetStatusText("Setting term pager 0...")
        objTab.Screen.Send("term pager 0\r")
        objTab.Screen.WaitForString("term pager 0\r")
        objTab.Screen.WaitForString(strPrompt)

        objTab.Session.SetStatusText("Getting " + g_strConfigToSave + "-config...")

        # Then, we'll run the 'show ...' command...
        strCmd = "more system:{0}-config\r".format(g_strConfigToSave)
        objTab.Screen.Send(strCmd)

        # Also, ASA devices seem to ouput the config w/o extraneous data like
        # size, etc., so all we have to do is read up to where the prompt
        # appears... First, wait for the command we sent to appear as echo'd
        # from the remote...
        objTab.Screen.WaitForString(strCmd)
        objTab.Screen.WaitForString("\n")
        # Now, Let's read/capture up to the point where the shell prompt appears...
        objTab.Session.SetStatusText("Reading " + g_strConfigToSave + "-config...")
        strConfig = objTab.Screen.ReadString(strPrompt)

        # Restore the pager... Well, set it to what SecureCRT has as rows...
        objTab.Session.SetStatusText("Setting pager back to full rows...")
        objTab.Screen.Send("term pager {0}\r".format(objTab.Screen.Rows))
        objTab.Screen.WaitForString(strPrompt)
    else:
        # Cisco 881W, etc. case
        objTab.Session.SetStatusText("Setting term len 0...")
        if int(nRows) > 0:
            objTab.Screen.Send("term len 0\r")
            objTab.Screen.WaitForString(strPrompt)
        if int(nCols) < 132:
            objTab.Session.Config.SetOption("Cols", 132)
            objTab.Screen.Send("term width 132\r")
            objTab.Screen.WaitForString(strPrompt)

        objTab.Session.SetStatusText("Getting " + g_strConfigToSave + "-config...")
        # Cmd will either be 'show running-config' or 'show startup-config':
        strCmd = "show " + g_strConfigToSave + "-config"

        # Accommodate any additional args to the sh startup-config or sh running-config
        # that were passed in as arguments to the script (as in: the button bar setup
        # has additional arguments after the "running"). For example:
        #    running all
        #    running brief
        #    running interface dialer 1
        #    startup linenum)
        if g_strAdditionalArgs == "":
            strCmd += "\r"
        else:
            strCmd += " " + g_strAdditionalArgs + "\r"

        objTab.Screen.Send(strCmd)

        if g_strConfigToSave == "running":
            objTab.Screen.WaitForStrings(["Current configuration", "Invalid input"])
            if objTab.Screen.MatchIndex > 1:
                FlashStatusText("Invalid command")
                return
            nBytes = objTab.Screen.ReadString("\r\n")
        elif g_strConfigToSave == "startup":
            objTab.Screen.WaitForStrings(["Using", "Invalid input"])
            if objTab.Screen.MatchIndex > 1:
                FlashStatusText("Invalid command")
                return
            nBytes = objTab.Screen.ReadString(" out of ")
            objTab.Screen.WaitForString("bytes\r\n")
        else:
            MsgBox("Unknown config type: '" + g_strConfigToSave + "'. Exiting.")
            return

        strConfig = objTab.Screen.ReadString(strPrompt)
        objTab.Session.SetStatusText("Restoring original terminal size...")
        objTab.Screen.Send("term len " + nRows + "\r")
        objTab.Screen.WaitForString(strPrompt)
        objTab.Session.Config.SetOption("Cols", nColsOrig)
        objTab.Screen.Send("term width " + nCols + "\r")
        objTab.Screen.WaitForString(strPrompt)

    objTab.Session.SetStatusText("Saving configuration to local file system...")
    strDateTimeTag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")[:19]
    strSessionPath = objTab.Session.Path
    strSessionPath = strSessionPath.replace("\\", "/")
    objMatch = re.match(r'(.*)[/]([^/]+)$', strSessionPath)
    strSessionName = strSessionPath
    strSavedConfigsFolder = "Config-Saves/"
    if objMatch:
        strSavedConfigsFolder += objMatch.group(1)
        strSessionName = objMatch.group(2)

    if strSavedConfigsFolder[-1] != "/":
        strSavedConfigsFolder += "/"

    strActualFolder = g_strMyDocs + "/" + strSavedConfigsFolder
    if not os.path.exists(strActualFolder):
        # create folder tree for config file we're about to save.
        os.makedirs(strActualFolder)

    if strActualFolder[-1] != "/":
        strActualFolder += "/"

    strActualFilePath = strActualFolder + strSessionName + "_" + \
        objTab.Session.RemoteAddress + "_" + g_strConfigToSave + \
            "-config_" + strDateTimeTag + ".txt"

    strFilename = Browse(
        "Choose where to save your " + g_strConfigToSave + "-config",
        "Save",
        strActualFilePath,
        "Text Files (*.txt)|*.txt||")

    if strFilename <> "":
        with open(strFilename, "wb") as objFile:
            objFile.write(strConfig)
        # If on Windows platform, bring up explorer with the file selected...
        if sys.platform == "win32":
            subprocess.call("explorer /e,/select,\"" + strFilename + "\"")

        FlashStatusText("Script Completed")
    else:
        FlashStatusText("Script Cancelled")

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Main()

