# $language = "python"
# $interface = "1.0"

# JumpHost-HandleSecondaryHostConnectionAttempts.py
#
#   - NOTE: SecureCRT must currently be connected to a gateway machine or  
#     jump host on which commands can be issued to connect to secondary hosts 
#     (eg: 'ssh hostb', 'telnet hostc', etc.)

import SecureCRT

crt.Screen.Synchronous = True

def main():
    vHosts = [\
        "10.34.120.1"]
    # The order of elements in this array should be in the order of: 
    #  - Expected login prompts (eg: "-->", "#", etc.)
    #  - Special cases (accept host key, enter pwd, enter username, etc.)
    #  - Fail/Bail cases (wrong pwd/login, hostname not found, time out, etc.)
    vPossibleResponses = [\
        "-->",
        "$",
        "ogin:",
        "ame:",
        "(yes/no)?",
        "sword:",
        "Permission denied",
        "incorrect",
        "not known",
        "timed out"]
    
    nIndex = 0
    strJumpHostPrompt = "-->"
    user = crt.Dialog.Prompt("Specify Username:", "Login", "", False)
    while nIndex <= len(vHosts):
        strCommand = "ssh " + vHosts[nIndex]
        crt.Screen.Send(strCommand + "\r")
        
        # Wait for our command to be echoed back to us so we know that it has been
        # received before we attempt to wait for all possible responses.
        crt.Screen.WaitForString(strCommand + "\r\n")
        
        # Start an inner Do..Loop that looks for all defined possible responses to
        # the Telnet... or SSH... command we just sent.
        
        while True:
            crt.Screen.WaitForStrings(vPossibleResponses)
            if crt.Screen.MatchIndex > 0:
                strStringFound = vPossibleResponses[crt.Screen.MatchIndex - 1]
                
            if crt.Screen.MatchIndex == 1 or crt.Screen.MatchIndex == 2:
                # Found "-->" or "$" which in our example indicate successful
                # authentications.
                
                # Do work we need to complete on host including sending the exit
                # command which will disconnect us from the secondary host
                # allowing us to loop up to the top and connect to the next
                # host. Note that the strStringFound variable currently contains  
                # the "Secondary Host Prompt" if needed.
                # .
                # .
                # .
                
                # Now that we have done the necessary work (including waiting
                # for an indication that the last command we sent above has
                # completed, send "exit" to disconnect from secondary host.
                crt.Screen.Send("exit\r")
                
               # Wait for an indication that the exit command was successful
                # before attempting to connect to next host.
                crt.Screen.WaitForString(strJumpHostPrompt)
                
                # Exit the inner loop since we are done with the success case.
                break
                    
            elif crt.Screen.MatchIndex == 3 or crt.Screen.MatchIndex == 4:
                # Found "ogin" or "ame" which means waiting for user account.
                crt.Screen.Send(strUsername + "\r")

                # Fall through to the top of the inner loop to continue
                # waiting for strings until all possibilities are exhausted.
                
            elif crt.Screen.MatchIndex == 5:
                # Found new hostkey prompt.  This indicates that this is the
                # first time we have connected to the remote machine, and we
                # need to accept the hostkey.    
                crt.Screen.Send("yes\r")
                
                # Fall through to the top of the inner loop to continue
                # waiting for strings until all possibilities are exhausted.

            elif crt.Screen.MatchIndex == 6:
                # We are being prompted for a password.  Send it.
                crt.Screen.Send(strPassword + "\r")

                # Fall through to the top of the inner loop to continue
                # waiting for strings until all possibilities are exhausted.

            elif crt.Screen.MatchIndex == 7:
                # SSH Password was denied or login was incorrect.  Exit this   
                # inner loop and move on to the next host.
                
                # First cancel the current authentication attempt to the
                # secondary host.
                crt.Screen.SendKeys("^c")
                
                # Wait for an indication that the Ctrl+C was successful before
                # attempting to connect to next host.
                crt.Screen.WaitForString(strJumpHostPrompt)

                # Exit the inner loop and move to next host.
                break
                    
            elif crt.Screen.MatchIndex == 8:
                # Telnet login or password was incorrect.  Exit this inner  
                # loop and move on to the next host.
                
                # First cancel the current authentication attempt to the
                # secondary host.
                crt.Screen.SendKeys("^]")
                crt.Screen.WaitForString("telnet>")
                crt.Screen.Send("quit\r")
                
                # Wait for an indication that the Ctrl+C was successful before
                # attempting to connect to next host.
                crt.Screen.WaitForString(strJumpHostPrompt)
                
                # Exit the inner loop and move to next host.
                break
                    
            elif crt.Screen.MatchIndex == 9 or crt.Screen.MatchIndex == 10:
                # Not able to reach secondary host.  Connection timed out.  
                # Wait for primary host prompt before exiting inner Do..Loop.
                crt.Screen.WaitForString(strJumpHostPrompt)
                
                # Exit the inner loop and move to next host.
                break
                    
            else:
                # Let user know that there is an unhandled case
                crt.Session.SetStatusText("Unhandled " + strStringFound)
                # Yikes... Never expect to be here, but if we got here, it's
                # probably a programming error you've introduced with the
                # 'vPossibleResponses' variable that you'll need to fix
                crt.Dialog.MessageBox("Yikes!\r\n\r\n"
                    "We never expect to get here. if you see this, you\r\n"
                    "have probably introduced a programming error into\r\n"
                    "your script code which will you will need to fix.\r\n\r\n"
                    "Chances are you added a string to vPossibleResponses\r\n"
                    "but you haven't added the code to handle\r\n"
                    "what to do when that special string was found:\r\n\r\n" 
                    "\t" + strStringFound)
                crt.Screen.SendSpecial("MENU_SCRIPT_CANCEL")
        
        nIndex = nIndex + 1
        
main()