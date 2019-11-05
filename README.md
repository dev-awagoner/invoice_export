# Google Sheets export to MySQL
A project to export sheets from a known Google Spreadsheet to a known MySQL database.

The assumption is that none of the USERIDs, passwords, connections will be hard-coded.  The code will use environment variables on the local system.

## Requirements
The current requirements are:
1.  Python 3.7+ (earlier 3.x code may work, but has not been tested).
2.  [Sheetfu](https://github.com/socialpoint-labs/sheetfu) - A very nice library for connecting to Google Sheets using to Python.

## Workflow
The code works in the following manner:
1.  Setup the various ENVIRONMENT VARIABLES and map those to a dictionary
2.  Connecting to a specified Google Spreadsheet using the following dictionary keys:
    1.  SPREADSHEET_ID
    2.  SERVICE_ACCESS_FILE
3.  Gather ranges (in the form of a list of lists) from the **Invoice**, **Customer_Info**, and **Settings** sheets
    1.  Modify **date** fields in the lists to conform to MySQL format (YYYY/MM/DD)
    2.  The date columns in the sheets are **TEXT** fields, and not numbers
4.  Connect to the MySQL database using the db_config dictionary with the following keys:
    1.  MYSQL_HOST
    2.  MYSQL_DATABASE
    3.  MYSQL_UID
    4.  MYSQL_PWD
5.  The list of lists data (ranges) are then inserted into **existing** and **empty** database tables:
    1.  Settings
    2.  Customer
    3.  Invoice

## Exceptions and Errors
This first pass of the code is not hardened for the myriad errors that can occur when connecting to Google Sheets or a MySQL database.  When something does fail, the error is normally straightforward.  If it's not
readily apparent where the error lies, there are several **debug print** statements throughout the code to aid in problem detection.