''''''''''''''''''''''''''''''''''''''
' Author: Joshua Gould
' Filename: EmailSend.vb
' Function: 
' Email users in range A for process of Vulnerability management. 
' Takes the coloumn 'A' of the spreadsheet and sends a message with information provided
'
'
' First Created: 3-28-2019
' Last Updated: 4-08-2019
'
'''''''''''''''''''''''''''''''''''''' 



Sub SendEmail()
    Dim OutApp As Object
    Dim OutMail As Object
    Dim dict As Object 'keep the unique list of emails
    Dim cell As Range
    Dim cell2 As Range
    Dim rng As Range
    Dim i As Long
    Dim WS As Worksheet
    AutoCp = False

    Application.ScreenUpdating = False
    Set OutApp = CreateObject("Outlook.Application")
    Set dict = CreateObject("scripting.dictionary")
    Set WS = ThisWorkbook.Sheets("Monitoring") 'change the name of the sheet accordingly

    On Error GoTo cleanup
    
    
        For Each cell In WS.Columns("A").Cells.SpecialCells(xlCellTypeConstants)
        
        If AutoCp = False Then
        
        If cell.Value Like "?*@?*.?*" Then

            'check if this email address has been used to generate an outlook email or not
            If dict.exists(cell.Value) = False Then

                dict.Add cell.Value, "" 'add the new email address
                Set OutMail = OutApp.CreateItem(0)
                Set rng = WS.UsedRange.Rows(1)

                'find all of the rows with the same email and add it to the range
                For Each cell2 In WS.UsedRange.Columns(1).Cells
                    If cell2.Value = cell.Value Then
                        Set rng = Application.Union(rng, WS.UsedRange.Rows(cell2.Row))
                    End If
                Next cell2
                
                On Error Resume Next
                
                Select Case MsgBox("Would you like to send the email? Press 'No' to display" & vbCr & "Press 'Cancel' to Suppress this and AutoSend all", vbYesNoCancel + vbQuestion)
                Case vbYes
                    With OutMail
                        .To = cell.Value
                        .Subject = "Request for information for Vulnerability Management Project"
                        .HTMLBody = "Hello," & "<br>" & "<br>" _
                        & "In regards to the following Rowan applications:" & vbNewLine & vbNewLine & RangetoHTML(rng) & "<br>" _
                        & "Your application has been classified as a <b>private</b> application which will be monitored by our Vulnerability Management Log Correlation Engine (LCE), you have been identified as the administrator of this application." & "<br>" & "<br>" _
                        & "Can you identify the servers and their roles that host these applications?" & "<br>" & "(e.g. application/web server/database server)" _
                        & "<br>" & "<br>" & "If servers are hosted outside of Rowan, please note that as well." & "<br>" & "<br>" _
                        & "A link to update your information is provided " _
                        & "<a href=https://docs.google.com/spreadsheets/d/1qS0AlZXY0h4uQVxKuObIZWQ2gWQU-uiYlZZeQeAh4Tg/edit#gid=945653965>here:</a>" _
                        & "<br>" & "Please enter this information in Coloumn I - Server Role (File Server, Web Server, Database, etc)" & "<br>" & "<br>" & "Example of data that we need:" & "<br>" & "<br>" & "Server1.rowan.edu / Application server" & "<br>" & "Server2.rowan.edu / Web server" & "<br>" & "Server3.rowan.edu / database server" & "<br>" & "Server4.rowan.edu / Application server Hosted with Amazon 'AWS'"
                        .Send
                    End With
                    
                Case vbNo
                    With OutMail
                        .To = cell.Value
                        .Subject = "Request for information for Vulnerability Management Project"
                        .HTMLBody = "Hello," & "<br>" & "<br>" _
                        & "In regards to the following Rowan applications:" & vbNewLine & vbNewLine & RangetoHTML(rng) & "<br>" _
                        & "Your application has been classified as a <b>private</b> application which will be monitored by our Vulnerability Management Log Correlation Engine (LCE), you have been identified as the administrator of this application." & "<br>" & "<br>" _
                        & "Can you identify the servers and their roles that host these applications?" & "<br>" & "(e.g. application/web server/database server)" _
                        & "<br>" & "<br>" & "If servers are hosted outside of Rowan, please note that as well." & "<br>" & "<br>" _
                        & "A link to update your information is provided " _
                        & "<a href=https://docs.google.com/spreadsheets/d/1qS0AlZXY0h4uQVxKuObIZWQ2gWQU-uiYlZZeQeAh4Tg/edit#gid=945653965>here:</a>" _
                        & "<br>" & "Please enter this information in Coloumn I - Server Role (File Server, Web Server, Database, etc)" & "<br>" & "<br>" & "Example of data that we need:" & "<br>" & "<br>" & "Server1.rowan.edu / Application server" & "<br>" & "Server2.rowan.edu / Web server" & "<br>" & "Server3.rowan.edu / database server" & "<br>" & "Server4.rowan.edu / Application server Hosted with Amazon 'AWS'"
                        .Display
                    End With
                
                Case vbCancel
                    
                    AutoCp = True
                    
               End Select
               

                On Error GoTo 0
                Set OutMail = Nothing
            End If
        End If
        Else
            If cell.Value Like "?*@?*.?*" Then

            'check if this email address has been used to generate an outlook email or not
            If dict.exists(cell.Value) = False Then

                dict.Add cell.Value, "" 'add the new email address
                Set OutMail = OutApp.CreateItem(0)
                Set rng = WS.UsedRange.Rows(1)

                'find all of the rows with the same email and add it to the range
                For Each cell2 In WS.UsedRange.Columns(1).Cells
                    If cell2.Value = cell.Value Then
                        Set rng = Application.Union(rng, WS.UsedRange.Rows(cell2.Row))
                    End If
                Next cell2
                
                On Error Resume Next
                
                With OutMail
                        .To = cell.Value
                        .Subject = "Request for information for Vulnerability Management Project"
                        .HTMLBody = "Hello," & "<br>" & "<br>" _
                        & "In regards to the following Rowan applications:" & vbNewLine & vbNewLine & RangetoHTML(rng) & "<br>" _
                        & "Your application has been classified as a <b>private</b> application which will be monitored by our Vulnerability Management Log Correlation Engine (LCE), you have been identified as the administrator of this application." & "<br>" & "<br>" _
                        & "Can you identify the servers and their roles that host these applications?" & "<br>" & "(e.g. application/web server/database server)" _
                        & "<br>" & "<br>" & "If servers are hosted outside of Rowan, please note that as well." & "<br>" & "<br>" _
                        & "A link to update your information is provided " _
                        & "<a href=https://docs.google.com/spreadsheets/d/1qS0AlZXY0h4uQVxKuObIZWQ2gWQU-uiYlZZeQeAh4Tg/edit#gid=945653965>here:</a>" _
                        & "<br>" & "Please enter this information in Coloumn I - Server Role (File Server, Web Server, Database, etc)" & "<br>" & "<br>" & "Example of data that we need:" & "<br>" & "<br>" & "Server1.rowan.edu / Application server" & "<br>" & "Server2.rowan.edu / Web server" & "<br>" & "Server3.rowan.edu / database server" & "<br>" & "Server4.rowan.edu / Application server Hosted with Amazon 'AWS'"
                        .Send
                End With
              
               

                 On Error GoTo 0
                    Set OutMail = Nothing
                End If
            End If
         End If
        Next cell




cleanup:
    Set OutApp = Nothing
    Application.ScreenUpdating = True
End Sub

Function RangetoHTML(rng As Range)
' coded by Ron de Bruin 28-Oct-2006
' Working in Office 2000-2016
    Dim fso As Object
    Dim ts As Object
    Dim TempFile As String
    Dim TempWB As Workbook

    TempFile = Environ$("temp") & "\" & Format(Now, "dd-mm-yy h-mm-ss") & ".htm"

    'Copy the range and create a new workbook to past the data in
    rng.Copy
    Set TempWB = Workbooks.Add(1)
    With TempWB.Sheets(1)
        .Cells(1).PasteSpecial Paste:=8
        .Cells(1).PasteSpecial xlPasteValues, , False, False 'Paste values of row
        .Cells(1).PasteSpecial xlPasteFormats, , False, False 'Paste formats of row
        .Cells(1).Select
        Application.CutCopyMode = False
        On Error Resume Next
        .DrawingObjects.Visible = True
        .DrawingObjects.Delete
        On Error GoTo 0
    End With

    'Publish the sheet to a htm file
    With TempWB.PublishObjects.Add( _
         SourceType:=xlSourceRange, _
         Filename:=TempFile, _
         Sheet:=TempWB.Sheets(1).Name, _
         Source:=TempWB.Sheets(1).UsedRange.Address, _
         HtmlType:=xlHtmlStatic)
        .Publish (True)
    End With

    'Read all data from the htm file into RangetoHTML
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.GetFile(TempFile).OpenAsTextStream(1, -2)
    RangetoHTML = ts.readall
    ts.Close
    RangetoHTML = Replace(RangetoHTML, "align=center x:publishsource=", _
                          "align=left x:publishsource=")

    'Close TempWB
    TempWB.Close savechanges:=False

    'Delete the htm file we used in this function
    Kill TempFile

    Set ts = Nothing
    Set fso = Nothing
    Set TempWB = Nothing
End Function





