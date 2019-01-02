# $language = "python"
# $interface = "1.0"

#################################
# Filename      - copy.py       #
# Author        - Joshua Gould  #
# Created       - 12-20-2018    #
# Last Modified - 12-28-2018    #
#################################

# Requirements  - This script runs on SECURE CRT terminals ONLY for CISCO devices
# Description   - Function definition for copying a running configuration of a switch to the clipboard.

# Using GetScriptTab() will make this script 'tab safe' in that all of the
# script's functionality will be carried out on the correct tab. From here
# on out we'll use the SCRIPT_TAB object instead of the crt object.
SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Synchronous = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():

	if not crt.Session.Connected:
		crt.Dialog.MessageBox(
			"No CRT terminal open or connected")
		return

	crt.Screen.Synchronous = True

	# We'll use a "SendExpect" function to easily send commands 
	# and wait for the remote device to be ready
	
	# Prompt for a password instead of embedding it in a script...
	
	passwd = crt.Dialog.Prompt("Enter password:", "Login", "", True)

        if not SendExpect("enable", "ssword:"):
		    return
	if not SendExpect(passwd, "#"):
		return

	
	# CaptureOutputOfCommand which takes as its first parameter 
	# the command to run, and as the 2nd parameter,
	# the text that indicates the command has completed
	data = CaptureOutputOfCommand("show run", "#")


	# Some Cisco devices send EOL as LFCR rather than CRLF.  If we find the
	# LFCR pattern, let's replace it with CRLF. (Credit to Vandyk Website)
	data = data.replace('\n\r', '\r\n')
	
	# Data has been captured for the output of each of the 'show' commands,
    #
	# send the data to the system clipboard.
    # format may need changing (SPACE BAR ENTRY IS RECORDED)
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data
	
	crt.Dialog.MessageBox(
		"Text is now in the clipboard: \n\n" + crt.Clipboard.Text)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CaptureOutputOfCommand(command, prompt):
	if not crt.Session.Connected:
		return "[ERROR: Not Connected.]"
	
	# First, send the command to the remote.
	SCRIPT_TAB.Screen.Send(command + '\r')
	
	# Second, wait for the carriage return to be echoed by the remote device.
	# This allows us to capture only the output of the command, not the line
	# on which the command was issued (which would include the prompt + cmd).
	# If you want to capture the command that was issued, simply comment out
	# the following line of code.
	SCRIPT_TAB.Screen.WaitForString('\r')
	
	# Now that the command has been sent, use Screen.ReadString to capture
	# all the data that is received up to the point at which the shell
	# prompt appears (the captured data does not include the shell prompt).
	return SCRIPT_TAB.Screen.ReadString(prompt)


main()
