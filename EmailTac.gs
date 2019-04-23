////////////////////////////////////////////////////////////////////////////
// Author: Joshua Gould | contact: 856-246-9352 | joshtree51@gmail.com
//
// FileName: emailTac.gs
//
// Function: 
// Email TAC for RMA process of a product. 
// Takes the last line in the NSS inventory spreadsheet - page 'RMA INV'
// 
// Requirements: 
// Needs name, number, and email of person sending the RMA email.
// Needs data to be previously entered
//
// First Created: 3-28-2019
// Last Updated: 3-28-2019
//
////////////////////////////////////////////////////////////////////////////


function emailTac() {
  var ui = SpreadsheetApp.getUi(); // Same variations
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('RMA INV'); // or whatever is the name of the sheet 
  
  var nextRow = sheet.getLastRow() + 1;
  var lastRow = sheet.getLastRow()  // get last row in spread sheet. Possible improvement in adding rows. See nextRow for inspiration
  
  
  var phoneName = sheet.getRange(lastRow,2); // gets coloumn B of the last row
  var textPH = phoneName.getValue();
  
  var SN = sheet.getRange(lastRow,3); // gets coloumn C (serial number) of the last row
  var textSN = SN.getValue();
  
  var result = ui.alert(
     'WARNING',
     'Is all information entered into "RMA INV" spreadsheet on the last row?',
      ui.ButtonSet.YES_NO);

  // Process the user's response.
  if (result == ui.Button.YES) {
    // User clicked "Yes".
  
     
  var Nresult = ui.prompt(
    'Required Information',
    'Enter Name:',
      ui.ButtonSet.OK_CANCEL); // enter your name prompt
  var Eresult = ui.prompt(
    'Required Information',
    'Enter Email for Contact:',
      ui.ButtonSet.OK_CANCEL); // enter your email prompt
  var BRresult = ui.prompt(
    'Required Information',
    'Enter Phone Number for Contact',
      ui.ButtonSet.OK_CANCEL); // enter your phone number prompt
  var ISresult = ui.prompt(
    'Required Information',
    'What is the issue with the phone?',
      ui.ButtonSet.OK_CANCEL); // issue with the phone
  
  // button set-up
  var buttonN = Nresult.getSelectedButton();
  var name = Nresult.getResponseText();
  var buttonE = Eresult.getSelectedButton();
  var email = Eresult.getResponseText();
  var buttonBR = BRresult.getSelectedButton();
  var number = BRresult.getResponseText();
  var buttonIS = ISresult.getSelectedButton();
  var Issue = ISresult.getResponseText();
  // outputs the text entered to InfoBl below to format contact information that tac@cisco needs
  
 
  var sepBl = ('\n---------------------------------------------------------\n\n')
  var InfoBl = (sepBl + 'Company name: Rowan University\n\nAddress: 201 Mullica Hill Road, Glassboro NJ, 08028; Memorial Hall Room 187' 
                + '\n\nSite contact name: '+ name 
                + '\n\nSite contact phone #: '+ number 
                + '\n\nSite contact email (if applicable): '+ email 
                + '\n\nInternal ticket # (if applicable): N/A');
  
  //formats the email stuff
  var emailAddress = 'tac@cisco.com';
  var subject = 'RMA Email';
  var phoneInfo = 'Model#\n\n'+ textPH + '\n\nSN#\n\n' + textSN + '\n\n' + 'Issue:  '+ Issue;
  var message = 'Model#\n\n'+ textPH + '\n\nSN#\n\n' + textSN + '\n\n' + 'Issue:  '+ Issue +'\n\n\n' + InfoBl;
  var boolAdd = 1;
  var j = 1;
  
  for (boolAdd = 1; boolAdd < 10; boolAdd++) {
      var addPhone = ui.alert(
      'Add a phone?',
      phoneInfo + '\n\n' + sepBl +'Do you want to add a phone to this list',
      ui.ButtonSet.YES_NO);
      
      if (addPhone == ui.Button.YES) {
      // User clicked "Yes".
    
        var nextRow = sheet.getLastRow() - j;
        var phoneNameAdd = sheet.getRange(nextRow,2); // gets coloumn B of the last row
        var textPHadd = phoneNameAdd.getValue();
        var SNadd = sheet.getRange(nextRow,3); // gets coloumn C (serial number) of the last row
        var textSNadd = SNadd.getValue();
        j = j + 1;
        
        var phoneInfo = phoneInfo + sepBl + 'Model#\n\n'+ textPHadd + '\n\nSN#\n\n' + textSNadd + '\n\n' + 'Issue:  '+ Issue;
    
      } else {
        // User clicked "No" or X in the title bar.
        ui.alert('No phone added');
        
        boolAdd = 10;
        var message = phoneInfo + '\n\n\n' + InfoBl
      }
      
  }
    
   
    
  //makes sure you actually want to send the email
  var result = ui.alert(
      'Send this email?',
      message,
      ui.ButtonSet.YES_NO);
 
  // Process the user's response.
  if (result == ui.Button.YES) {
    // User clicked "Yes".
    
    MailApp.sendEmail(emailAddress, subject, message);
    ui.alert('Email Sent');
    
  } else {
    // User clicked "No" or X in the title bar.
    ui.alert('No Email Sent');
  }

  


  } else {
    // User clicked "No" or X in the title bar.
    ui.alert('Please enter all information and have a nice day :) ');
  }

  
  
 
  
}
