
*** Settings ***
Library   OperatingSystem
Library   tests/DbTestUtils.py
Test Setup    Create db 
Test Teardown    Drop all



*** Keywords ***
Initializing the app for user
  [Arguments]           ${username} 
  Setup app             ${username}
  Name should be        ${username}
  Created at should be less than a second ago

  
*** Test Cases ***
Setup the app Jane
  Initializing the app for user    Jane



