# NSSWorkerScripts
Scripts Used to Configure Switches within Rowan Directory

Directory lists scipts that were custom made or edited specifically for autonomous network deployment and are finished in development enough for public use

## Directory
- **stackconf.py**    : set stack order for initial switch configuration
- **wipe3560.py**     : wipe a CISCO 3560 (and some other models) from rommon and abuse password recovery
- **WipeAP.py**       : wipe Aruba AP to factory default from boot mode
- **wipecontrol.py**  : wiped configured and secured CISCO switch (most models)
- **EmailTac.gs**     : email TAC cisco for RMA phones
- **EmailSend.vb**    : takes first column of emails and sends the information of that row to each individual of column, matching duplicates

## Instuctions for Running scripts 

- Depending on the script you wish to run...
  - python scripts will run in SecureCRT's compiler as long as there is an active connection with Script > Run Script
  - google App Scripts will run in google's script editor (Tools > Script Editor)
  - visual basic scripts will run in Excel or other Microsoft application with the Developer tab enabled

*Psst...Helpful Links: https://www.vandyke.com/support/tips/*
