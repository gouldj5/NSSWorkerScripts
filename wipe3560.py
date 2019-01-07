﻿#$language = "python"
#$interface = "1.0"

crt.Screen.Synchronous = True

def Main():
	crt.Screen.Send ("flash_init" + chr(13))
	crt.Screen.WaitForString ("switch:")
	crt.Screen.Send ("rename flash:config.text flash:config.old" + chr(13))
	crt.Screen.WaitForString ("switch:")
	crt.Screen.Send ("boot" + chr(13))
        crt.Screen.WaitForString ("Press RETURN to get started!")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("? [yes/no]:")
	crt.Screen.Send ("n" + chr(13))
	crt.Screen.WaitForString (">")
	crt.Screen.Send ("en" + chr(13))
	crt.Screen.WaitForString ("#")
	crt.Screen.Send ("wr er" + chr(13))
	crt.Screen.WaitForString ("confirm]")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("Switch#")
	crt.Screen.Send ("delete vlan.dat" + chr(13))
	crt.Screen.WaitForString ("Delete filename [vlan.dat]?")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("Delete flash:vlan.dat? [confirm]")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("Switch#")
	crt.Screen.Send ("delete flash:config.old" + chr(13))
	crt.Screen.WaitForString ("config.old]?")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("confirm]")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("Switch#")
	crt.Screen.Send ("reload" + chr(13))
	crt.Screen.WaitForString ("nfirm]")
	crt.Screen.Send (chr(13))
Main()
