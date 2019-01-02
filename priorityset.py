# $language = "python"
# $interface = "1.0"

#################################
# Filename      - priorityset.py#
# Author        - Joshua Gould  #
# Created       - 12-20-2018    #
# Last Modified - 12-28-2018    #
#################################

# Requirements  - This script runs on SECURE CRT terminals ONLY for CISCO devices
# Description   - Function definition for setting a CISCO switch to priority. Switch order MUST be pre-defined.
def priorityset():
	crt.Screen.Synchronous = True
	crt.Screen.Send("sh sw" + chr(13))
	crt.Screen.WaitForString("#")
	crt.Screen.Send("conf t" + chr(13))
	crt.Screen.WaitForString("#")
	crt.Screen.Send("sw 1 priority 15" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 2 priority 14" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 3 priority 13" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 4 priority 12" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 5 priority 11" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 6 priority 10" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 7 priority 9" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 8 priority 8" + chr(13))
	crt.Screen.WaitForString("#")
        crt.Screen.Send("sw 9 priority 7" + chr(13))
	crt.Screen.WaitForString("#")
	crt.Screen.Send("exit" + chr(13))
	crt.Screen.WaitForString("#")
	crt.Screen.Send("wr mem" + chr(13))

wipecontrol()

