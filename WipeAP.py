#$language = "python"
#$interface = "1.0"

crt.Screen.Synchronous = True

def Main():
	crt.Screen.WaitForString ("Hit <Enter>")
        crt.Screen.Send (chr(13))
        crt.Screen.WaitForString ("apboot>")
        crt.Screen.Send ("factory" + chr(13))
	crt.Screen.WaitForString ("apboot>")
	crt.Screen.Send ("purge" + chr(13))
	crt.Screen.WaitForString ("apboot>")
	crt.Screen.Send (chr(13))
	crt.Screen.WaitForString ("apboot>")
	crt.Screen.Send ("reset" + chr(13))
Main()
