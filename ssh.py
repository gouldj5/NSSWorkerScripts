# $language = "python"
# $interface = "1.0"

# Connect to an SSH server using the SSH2 protocol. Specify the
# username and password and hostname on the command line as well as
# some SSH2 protocol specific options.

user = crt.Dialog.Prompt("Enter username:", "Login", "", False)
passwd = crt.Dialog.Prompt("Enter password for this host", "Login", "", True)
host = crt.Dialog.Prompt("Enter Hostname IP:", "Login", "",False)

def ssh():

	# Build a command-line string to pass to the Connect method.
	sha1 = "/SSH2 /L %s /PASSWORD %s /C 3DES /M sha2-256 %s" % (user, passwd, host)
	crt.Session.Connect(sha1)
      
ssh()

