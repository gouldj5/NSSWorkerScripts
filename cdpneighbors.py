#$language = "python"
#$interface = "1.0"

crt.Screen.Synchronous = True
passwd = crt.Dialog.Prompt("Enter password:", "Login", "", True)
def cdp():
	crt.Screen.WaitForString(">")
	crt.Screen.Send("en" + chr(13))
	crt.Screen.WaitForString("Password: ")
	crt.Screen.Send(passwd + chr(13))
	crt.Screen.WaitForString("#")
	crt.Screen.Send("sh cdp ne" + chr(9) + " det" + chr(9) + chr(13))

cdp()
