# $language = "VBScript"
# $interface = "1.0"

' SendASCII(OrPaste)WithPauseOrCancelCapability.vbs
'   Last Modified: 20 Nov, 2017
'     - Allow for variables to be used for substitutions when sending a
'       command. For example, if $var_name1 shows up as part of a line
'       about to be sent, if $var_name1 is defined with a variable, the
'       value of the variable will be sent in place of the $var_name1.
'     - Automatically resize the UI window so that the text edit area
'       and the CUR_LINE field are always visible.
'
'   Last Modified: 21 Feb, 2017
'     - Format change to enhance visual appeal (spacing on left/right of UI
'       form).
'     - Now shows current line about to be sent in its own field, that can
'       be edited before being sent.
'     - [Send] and [Skip] buttons now allow for sending the currnet line or
'       skipping the current line.
'     - Added option whether or not to wait for line sent to be echo'd back
'       from the remote before moving forward with the next line (on by
'       default).
'
'   Last Modified: 30 Oct, 2012
'     - Initial revision
'
' DESCRIPTION:
'   A separate UI is displayed (built using Internet Explorer), offering a
'   window in which you can browse for a file to send, define substitution
'   variables, and then Send/Skip lines one by one.
'
'   It can also be used simply as a mechanism for reviewing/modifying what's
'   currently in the clipboard prior to it being sent to a remote machine.
'
'   Demonstrates one way of building a customized window/dialog using IE and
'   handling user interaction within the custom dialog (see the VBScript user
'   guide here:  http://www.vandyke.com/support/tips/scripting/index.html)

Dim g_objIE, g_shell, g_fso, g_strTitle
Set g_objIE = Nothing
Set g_shell = CreateObject("WScript.Shell")
Set g_fso   = CreateObject("Scripting.FileSystemObject")

Dim g_cVariables
Set g_cVariables = CreateObject("Scripting.Dictionary")

g_strTitle = "Send Data Line-by-Line"

g_strDefaultDataFile = g_shell.SpecialFolders("MyDocuments") & "\My_ASCII_Data_File.txt"

Sub Main()
    crt.Session.SetStatusText "Script running: Send ASCII Line-by-Line"

    DisplaySendASCIIControlWindow

    crt.Session.SetStatusText "Script completed."
    crt.Sleep 1000
    crt.Session.SetStatusText ""

End Sub

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function DisplaySendASCIIControlWindow()
    InitIE

    Dim strHTMLBody
    strHTMLBody = _
        "<table>" & _
        "<tr><td width='10%'></td><td width='80%'>" & _
        "<input type=radio name='SEND_WHAT' value='Clipboard' AccessKey='C' " & _
            "checked onClick=document.all('ButtonHandler').value='SEND_CLIPBOARD';>" & _
            "Send <u>C</u>lipboard data<br>" & _
        "<input type=radio name='SEND_WHAT' value='FILE' Accesskey='F' " & _
            "onClick=document.all('ButtonHandler').value='SEND_FILE';>" & _
            "Send ASCII <u>F</u>ile<br>" & _
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" & _
            "<input name='ASCII_FILE_PATH' size='71' maxlength='512' AccessKey='f' " & _
            "onkeydown=if(window.event.keyCode==13)" & _
            "{document.all('ButtonHandler').value='ASCII_FILE_PATH_UPDATE';};>" & _
        "&nbsp;&nbsp;&nbsp;" & _
        "<button name='BROWSE_BTN' accesskey='.' " & _
            "onClick=document.all('ButtonHandler').value='BROWSE_BTN';>...</button>" & _
            "&nbsp;&nbsp;&nbsp;" & _
        "<br>" & _
        "<hr>" & _
        "<table width='98%'>" & _
        "<tr>" & _
            "<u>V</u>ariables:" & "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" & _
            "<font size=-1>Define variables below (one per line), using the pattern <i>$var_name</i>:=<i>var_value</i></font>" & _
            "<br>" & _
            "<TextArea rows=4 cols=90 id='VARIABLES' name='VARIABLES' AccessKey='v' " & _
                "onkeydown=""document.all('ButtonHandler').value='UPDATE_VARIABLES';"">" & _
            "$var_name1:=example value for variable" & vbcrlf & _
            "$var_name2:=another example of a variable being set" & _
            "</TextArea>" & _
        "</tr>" & _
        "</table>" & _
        "<br>" & _
        "<hr>" & _
        "<table width='98%'>" & _
        "<tr>" & _
            "Cur Li<u>n</u>e:<br>" & _
            "<TextArea rows=1 cols=90 id='CUR_LINE' name='CUR_LINE' AccessKey='n' " & _
                "onkeydown=if(window.event.keyCode==13)" & _
                "{document.all('ButtonHandler').value='SEND_BTN';};>" & _
            "</TextArea>" & _
        "</tr>" & _
        "<tr><td align='left'>" & _
                "<button id='SEND_BTN' name='SEND_BTN' accesskey='s' style='width:70px' " & _
                    "onclick=document.all('ButtonHandler').value='SEND_BTN';>" & _
                    "<u>S</u>end</button>" & _
            "<td align='left'>" & _
                "<button id='SKIP_BTN' name='SKIP_BTN' accesskey='k' style='width:70px' " & _
                    "onclick=document.all('ButtonHandler').value='SKIP_BTN';>" & _
                    "S<u>k</u>ip</button>" & _
            "<td align='right'>" & _
                "<button id='CLOSE_BTN' name='CLOSE_BTN' accesskey='l' style='width:70px' " & _
                    "onclick=document.all('ButtonHandler').value='CLOSE_BTN';>" & _
                    "  C<u>l</u>ose  </button>" & _
            "</tr></table>" & _
        "<br>" & _
        "<input type=checkbox id='WAIT_FOR_TEXT_BOOL' name='WAIT_FOR_TEXT_BOOL' " & _
            "accesskey='W' " & _
            "onclick=document.all('ButtonHandler').value='WAIT_FOR_TEXT_BOOL';>" & _
            "<u>W</u>ait for each line to be received before allowing subsequent lines to be sent.</input>" & _
        "<br><br><hr>" & _
        "<b>Te<u>x</u>t left to send:</b><br>" & _
        "<TextArea accesskey='x' rows=12 cols=90 id='DATA_TO_SEND' name='DATA_TO_SEND'  onkeydown=" & _
                "document.all('ButtonHandler').value='DATA_AREA_EDIT';>" & _
            "</TextArea>" & _
        "<input name='ButtonHandler' type='hidden' " & _
            "value='Nothing Clicked Yet'></input>" & _
        "</td><td width='10%'></td></tr></table>" & _
        ""
    g_objIE.Document.Body.InnerHTML = strHTMLBody

    Do
        crt.Sleep 100
    Loop While g_objIE.Busy

    ' Get references to the control objects for easier coding later on
    Set objButtonHandler = g_objIE.Document.All("ButtonHandler")
    Set objClipOrFileRadio = g_objIE.Document.All("SEND_WHAT")
    Set objBrowseButton = g_objIE.Document.All("BROWSE_BTN")
    Set objASCIIFileEntry = g_objIE.Document.All("ASCII_FILE_PATH")
    Set objWaitForTextCheck = g_objIE.Document.All("WAIT_FOR_TEXT_BOOL")
    Set objCurLineEntry = g_objIE.Document.All("CUR_LINE")
    Set objSendButton = g_objIE.Document.All("SEND_BTN")
    Set objCloseButton = g_objIE.Document.All("CLOSE_BTN")
    Set objDataToSendTextArea = g_objIE.Document.All("DATA_TO_SEND")
    Set objVariablesTextArea = g_objIE.Document.All("VARIABLES")
    objWaitForTextCheck.checked = True

    Set reVars = New RegExp
    reVars.IgnoreCase = True
    reVars.MultiLine = True
    reVars.Global = True
    reVars.Pattern = "^\s*(\$[^\$\s]+)\:\=([^\r\n]+)$"

    ' Variables used for detecting if the IE window is resized.
    ' Setting these to zero values allows the width and height
    ' of the text area to be resized to fill the available real
    ' estate of the IE window.
    nLastWidth = 0
    nLastHeight = 0

    ' Loop handling activity within the IE window that was just displayed
    bSkip = False
    nSleepMS = 10
    nOrigSleepMS = nSleepMS
    Do
        On Error Resume Next
        nCurWidth = g_objIE.Width
        nCurHeight = g_objIE.Height
        strActionIndicator = objButtonHandler.Value
        If Err.Number <> 0 Then Exit Function
        On Error Goto 0

        Select Case strActionIndicator
            Case "Nothing Clicked Yet"
                If g_fso.FileExists(g_strDefaultDataFile) Then
                    objClipOrFileRadio(1).Checked = True
                    objASCIIFileEntry.Value = g_strDefaultDataFile
                    objButtonHandler.Value = "ASCII_FILE_PATH_UPDATE"
                Else
                    objClipOrFileRadio(0).Checked = True
                    objDataToSendTextArea.Value = crt.Clipboard.Text
                    objCurLineEntry.Value = GetTextAreaFirstLine(objDataToSendTextArea)
                End If

            Case "UPDATE_VARIABLES"
                strOrig = objDataToSendTextArea.Value
                objDataToSendTextArea.Value = "[updating variables...]"
                g_cVariables.RemoveAll
                strVariableData = objVariablesTextArea.Value
                If reVars.Test(strVariableData) Then
                    Set objMatches = reVars.Execute(strVariableData)
                    For Each objMatch In objMatches
                        strVarName = objMatch.SubMatches(0)
                        strVarValue = objMatch.SubMatches(1)
                        If g_cVariables.Exists(strVarName) Then
                            g_cVariables(strVarName) = strVarValue
                        Else
                            g_cVariables.Add strVarName, strVarValue
                        End If
                    Next
                    objDataToSendTextArea.Value = "[" & g_cVariables.Count & " variables are ready for application.]"
                    crt.Sleep(100)
                Else
                    objDataToSendTextArea.Value = "[No variables could be found matching pattern: $varname:=variable value]"
                    crt.Sleep(300)
                End If

                objDataToSendTextArea.Value = strOrig

                objButtonHandler.Value = "DATA_AREA_EDIT"

            Case "ASCII_FILE_PATH_UPDATE"
                strFilePath = objASCIIFileEntry.Value
                If g_fso.FileExists(strFilePath) Then
                    Set objFile = g_fso.OpenTextFile(strFilePath, 1, False)
                    objDataToSendTextArea.Value = "Reading file contents (" & strFilePath & ")..."
                    strFileContents = objFile.ReadAll
                    objFile.Close
                    objDataToSendTextArea.Value = "Finished reading in " & Len(strFileContents) & " bytes. Now populating this view..."
                    objDataToSendTextArea.Value = strFileContents
                    objClipOrFileRadio(1).Checked = True
                    objClipOrFileRadio(0).Checked = False
                    objButtonHandler.Value = "UPDATE_VARIABLES"
                Else
                    crt.Dialog.MessageBox("File not found: " & strFilePath)
                    g_shell.AppActivate g_strTitle
                    objButtonHandler.Value = ""
                End If

            Case "SEND_CLIPBOARD"
                objClipOrFileRadio(0).Checked = True
                objDataToSendTextArea.Value = crt.Clipboard.Text
                objCurLineEntry.Value = GetTextAreaFirstLine(objDataToSendTextArea)

                objButtonHandler.Value = "UPDATE_VARIABLES"

            Case "SEND_FILE"
                objClipOrFileRadio(1).Checked = True
                If objASCIIFileEntry.Value <> "" Then
                    objButtonHandler.Value = "ASCII_FILE_PATH_UPDATE"
                End If

            Case "BROWSE_BTN"
                strOrigText = objDataToSendTextArea.Value
                objDataToSendTextArea.Value = "Browsing for file to send..."
                g_objIE.Visible = False
                strFilePath = crt.Dialog.FileOpenDialog(_
                    "Select ASCII File to Send", _
                    "Open", _
                    g_strDefaultDataFile, _
                    "Text Files (*.txt)|*.txt||")

                g_objIE.Visible = True
                g_shell.AppActivate g_strTitle

                If strFilePath <> "" Then
                    objASCIIFileEntry.Value = strFilePath
                    objButtonHandler.Value = "ASCII_FILE_PATH_UPDATE"
                Else
                    objButtonHandler.Value = ""
                    objDataToSendTextArea.Value = "...Browse cancelled."
                    crt.Sleep 300
                    objDataToSendTextArea.Value = ""
                End If

            Case "CLOSE_BTN"
                g_objIE.Quit
                Exit Function

            Case "SEND_BTN"
                strData = objDataToSendTextArea.Value
                strActionVerb = "send"
                If strData <> "" Then
                    strCurLine = objCurLineEntry.Value
                    If bSkip = False Then
                        crt.Session.SetStatusText "Sending: " & Left(strCurLine, 15) & "..."
                        If objWaitForTextCheck.checked = True Then
                            bOrig = crt.Screen.Synchronous
                            If Not crt.Screen.Synchronous Then
                                crt.Screen.Synchronous = True
                            End If
                            crt.Screen.Send strCurLine & vbcr
                            crt.Session.SetStatusText "WFS: " & Left(strCurLine, 15) & "..."
                            crt.Screen.WaitForString strCurLine, 10
                            crt.Session.SetStatusText ""
                            objCurLineEntry.Value = ""
                            crt.Screen.WaitForStrings Array(vbcr, vblf), 10
                            crt.Screen.Synchronous = bOrig
                        Else
                            crt.Screen.Send strCurLine & vbcr
                        End If
                        crt.Session.SetStatusText ""
                    Else
                        strActionVerb = "skip"
                        bSkip = False
                        nSleepMS = nOrigSleepMS
                    End If

                    vLines = GetArrayOfLinesFromTextArea(objDataToSendTextArea)
                    strNewData = ""
                    For i = 1 to UBound(vLines)
                        If i < UBound(vLines) Then
                            strNewData = strNewData & vLines(i) & vbcrlf
                        Else
                            strNewData = strNewData & vLines(i)
                        End if
                    Next

                    If strNewData <> "" Then
                        objDataToSendTextArea.Value = strNewData
                        objCurLineEntry.Value = GetTextAreaFirstLine(objDataToSendTextArea)
                    Else
                        objCurLineEntry.Value = ""
                        objDataToSendTextArea.Value = ""
                    End If
                Else
                    If bSkip Then
                        objDataToSendTextArea.Value = "[Nothing to skip]"
                        bSkip = False
                    Else
                        objDataToSendTextArea.Value = "[Nothing to " & strActionVerb & "]"
                    End If
                    crt.Sleep 1000
                    objDataToSendTextArea.Value = ""
                End If

                objButtonHandler.Value = ""

            Case "SKIP_BTN"
                ' Really just a wrapper around SEND_BTN (same functionality,
                ' but w/o actually sending the data.
                ' Set Skip bool to true
                bSkip = True
                ' Don't sleep this iteraction (immediately go to "SEND_BTN" state)
                nSleepMS = 0
                objButtonHandler.Value = "SEND_BTN"

            Case "DATA_AREA_EDIT"
                ' Need to update the CurLine above, if possible
                strFirstLine = GetTextAreaFirstLine(objDataToSendTextArea)
                If strFirstLine <> objCurLineEntry.Value Then
                    objCurLineEntry.Value = strFirstLine
                End If

                objButtonHandler.Value = ""

        End Select

        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '   Code for resizing text area to match IE Window size
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ' Check for the window being resized, and adjust the width of our
        ' TextAreas to adjust for resizing the main IE window.
        If nLastWidth <> nCurWidth Then
            ' Adjust current columns by 10 at first (so it's faster)
            ' Then, later on when we're "close", we'll adjust by one col at
            ' a time to narrow it down further.
            Do
                If nLastWidth < nCurWidth Then
                    objDataToSendTextArea.Cols = objDataToSendTextArea.Cols + 10
                    If objDataToSendTextArea.clientWidth >= nCurWidth - 80 _
                        Then Exit Do
                Else
                    objDataToSendTextArea.Cols = objDataToSendTextArea.Cols - 10
                    If objDataToSendTextArea.clientWidth <= nCurWidth - 80 _
                        Then Exit Do
                End If
            Loop

            If objDataToSendTextArea.clientWidth > (nCurWidth - 80) Then
                Do
                    objDataToSendTextArea.cols = objDataToSendTextArea.Cols - 1
                    If objDataToSendTextArea.clientWidth <= nCurWidth - 80 _
                        Then Exit Do
                Loop
            ElseIf objDataToSendTextArea.clientWidth < (nCurWidth - 100) Then
                Do
                    objDataToSendTextArea.cols = objDataToSendTextArea.Cols + 1
                    If objDataToSendTextArea.clientWidth >= nCurWidth - 80 _
                        Then Exit Do
                Loop
            End If

            ' Reset the last known width so we can detect when this changes
            ' again
            nLastWidth = nCurWidth
            ResizeWindowToFitAllElements()
            nLastHeight = g_objIE.Height
            nLastWidth = g_objIE.Width
        End If

        If nLastHeight <> nCurHeight Then
            nHeightBuffer = 320
            Do
                If nLastHeight < nCurHeight Then
                    objDataToSendTextArea.Rows = objDataToSendTextArea.Rows + 5
                    If (objDataToSendTextArea.clientHeight + _
                        objDataToSendTextArea.clientTop) >= _
                        nCurHeight - nHeightBuffer Then Exit Do
                Else
                    objDataToSendTextArea.Rows = objDataToSendTextArea.Rows - 5
                    If (objDataToSendTextArea.clientHeight + _
                        objDataToSendTextArea.clientTop) <= _
                        nCurHeight - nHeightBuffer Then Exit Do
                End If
            Loop

            If (objDataToSendTextArea.clientHeight + _
                objDataToSendTextArea.clientTop) > _
                nCurHeight - nHeightBuffer Then
                Do
                    objDataToSendTextArea.Rows = objDataToSendTextArea.Rows - 1
                    If (objDataToSendTextArea.clientHeight + _
                        objDataToSendTextArea.clientTop) <= _
                        (nCurHeight - nHeightBuffer) Then
                        Exit Do
                    End If
                Loop
            ElseIf (objDataToSendTextArea.clientHeight + _
                    objDataToSendTextArea.clientTop) < _
                    nCurHeight - nHeightBuffer Then
                Do
                    objDataToSendTextArea.Rows = objDataToSendTextArea.Rows + 1
                    If (objDataToSendTextArea.clientHeight + _
                        objDataToSendTextArea.clientTop) >= _
                        (nCurHeight - nHeightBuffer) Then
                        Exit Do
                    End If
                Loop
            End If

            ' Reset the last known height so we can detect when the window size
            ' changes again
            nLastHeight = nCurHeight
            ResizeWindowToFitAllElements()
            nLastHeight = g_objIE.Height
            nLastWidth = g_objIE.Width
        End If

        If nSleepMS > 0 Then
            crt.Sleep nSleepMS
        End If
    Loop

End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetTextAreaFirstLine(byRef objTextArea)
    strLine = ""
    On Error Resume Next
    vLines = GetArrayOfLinesFromTextArea(objTextArea)
    strLine = vLines(0)
    On Error Goto 0
    ' Make sure we consider substitutions that might be present
    For Each strVariable In g_cVariables.Keys()
        strLine = Replace(strLine, strVariable, g_cVariables(strVariable))
    Next

    GetTextAreaFirstLine = strLine
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetArrayOfLinesFromTextArea(objTextArea)
    strData = objTextArea.Value
    If strData <> "" Then
        If Instr(strData, vbcrlf) > 0 Then
            vLines = Split(strData, vbcrlf)
        ElseIf Instr(strData, vbcr) > 0 Then
            vLines = Split(strData, vbcr)
        ElseIf Instr(strData, vblf) > 0 Then
            vLines = Split(strData, vblf)
        Else
            ' Must only be a single non-empty line w/o any EOL
            vLines = Array(strData)
        End If

        GetArrayOfLinesFromTextArea = vLines
    Else
        GetArrayOfLinesFromTextArea = Nothing
    End If
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function InitIE()
    If g_objIE Is Nothing Then
        Set g_objIE = CreateObject("InternetExplorer.Application")
        g_objIE.Offline = True
        g_objIE.Navigate "about:blank"
    End If

    Do
        crt.Sleep 100
    Loop While g_objIE.Busy

    g_objIE.Document.body.Style.FontFamily = "Sans-Serif"

    g_objIE.MenuBar = False
    g_objIE.StatusBar = True
    g_objIE.AddressBar = False
    g_objIE.Toolbar = False
    g_objIE.Height = 700
    g_objIE.Width = 800
    g_objIE.Document.Title = g_strTitle

    g_objIE.Visible = True

    Do
        crt.Sleep 100
    Loop While g_objIE.Busy

    ' Try and activate/focus the new window
    Set objShell = CreateObject("WScript.Shell")
    objShell.AppActivate g_objIE.Document.Title

End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function RevealNonPrintingCharacters(strText)
' Makes non-printing characters "visible" by replacing them with reasonable
' short-character substitutions.
    Set colCharNames = CreateObject("Scripting.Dictionary")
    colCharNames.Add 0, "[NUL]"
    colCharNames.Add 1, "[SOH]"
    colCharNames.Add 2, "[STX]"
    colCharNames.Add 3, "[ETX]"
    colCharNames.Add 4, "[EOT]"
    colCharNames.Add 5, "[ENQ]"
    colCharNames.Add 6, "[ACK]"
    colCharNames.Add 7, "[BEL]"
    colCharNames.Add 8, "[BS]"
    colCharNames.Add 9, "[HT]"
    colCharNames.Add 10, "[LF]"
    colCharNames.Add 11, "[VT]"
    colCharNames.Add 12, "[FF]"
    colCharNames.Add 13, "[CR]"
    colCharNames.Add 14, "[SO]"
    colCharNames.Add 15, "[SI]"
    colCharNames.Add 16, "[DLE]"
    colCharNames.Add 17, "[DC1]"
    colCharNames.Add 18, "[DC2]"
    colCharNames.Add 19, "[DC3]"
    colCharNames.Add 20, "[DC4]"
    colCharNames.Add 21, "[NAK]"
    colCharNames.Add 22, "[SYN]"
    colCharNames.Add 23, "[ETB]"
    colCharNames.Add 24, "[CAN]"
    colCharNames.Add 25, "[EM]"
    colCharNames.Add 26, "[SUB]"
    colCharNames.Add 27, "[ESC]"
    colCharNames.Add 28, "[FS]"
    colCharNames.Add 29, "[GS]"
    colCharNames.Add 30, "[RS]"
    colCharNames.Add 31, "[US]"
    For nIndex = 32 To 126
        colCharNames.Add nIndex, chr(nIndex)
    Next
    colCharNames.Add 127, "[DEL]"

    strRevealingText = ""
    For nPos = 1 To Len(strText)
        ' Get the current character (we're working left->right from the first
        ' character of the string to the last charcter of the string):
        strCurrentChar = Mid(strText, nPos, 1)

        ' Map the current character to a printable sequence (using either the
        ' actual character (if printable), or a substitute as defined in the
        ' colCharNames collection above:
        strRevealingText = strRevealingText & colCharNames(ASC(strCurrentChar))
    Next

    ' Tidy things up a bit so that they'll appear more "normalized" in the
    ' messagebox
    strRevealingText = Replace(strRevealingText, "[CR][LF]", "[CRLF]" & vbcrlf)
    strRevealingText = Replace(strRevealingText, "[CR]", "[CR]" & vbcr)
    strRevealingText = Replace(strRevealingText, "[LF]", "[LF]" & vblf)
    strRevealingText = Replace(strRevealingText, "[HT]", "[HT]" & vbtab)

    RevealNonPrintingCharacters = strRevealingText
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sub ResizeWindowToFitAllElements()
    If Not g_objIE.Visible Then g_objIE.Visible = True

    Do While g_objIe.Busy
        crt.Sleep 1
    Loop

    nHorizOffset = GetHorizontalOffsetForElementVisibility("DATA_TO_SEND")
    if nHorizOffset = 0 Then
        nHorizOffset = GetHorizontalOffsetForElementVisibility("CUR_LINE")
    end if
    g_objIE.Width = g_objIE.Width + nHorizOffset

    Do While g_objIe.Busy
        crt.Sleep 1
    Loop

    nVertOffset = GetVerticalOffsetForElementVisibility("DATA_TO_SEND")
    g_objIE.Height = g_objIE.Height + nVertOffset

    Do While g_objIe.Busy
        crt.Sleep 1
    Loop

    crt.Session.SetStatusText "H:" & nHorizOffset & ", V:" & Round(nVertOffset)
End Sub

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetVerticalOffsetForElementVisibility(strElementID)
    On Error Resume Next
    Set objElement = g_objIE.Document.GetElementById(strElementID)
    Set rect = objElement.getBoundingClientRect()
    windowHeight = g_objIE.Document.documentElement.clientHeight
    GetVerticalOffsetForElementVisibility = (rect.top + rect.height + 10) - windowHeight
    On Error Goto 0
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetHorizontalOffsetForElementVisibility(strElementID)
    On Error Resume Next
    Set objElement = g_objIE.Document.GetElementById(strElementID)
    Set rect = objElement.getBoundingClientRect()
    windowWidth  = g_objIE.Document.documentElement.clientWidth
    GetHorizontalOffsetForElementVisibility = (rect.left + rect.width + 10) - windowWidth
    On Error Goto 0
End Function
