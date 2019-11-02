# Google Sheets export to MySQL
A project to export a known Google Spreadsheet to a known MySQL database

The assumption is that none of the USERIDs, passwords, connections will be hard-coded, but will use environment variables on the local system.

## Requirements
The current requirements are:
1.  Python 3.7+ (earlier 3.x code may work, but has not been tested).
2.  [Sheetfu](https://github.com/socialpoint-labs/sheetfu) - A very nice library for connecting to Google Sheets using to Python.

## Workflow
The code works in the following manner:
0.  Setup the various ENVIRONMENT VARIABLES and map those to python variables
1.  Connecting to a specified Google Spreadsheet using the following environment variables:
..1.1.  SPREADSHEET_ID
..1.2.  SERVICE_ACCESS_FILE
2.  Gather ranges (in the form of a list of lists) from the **Invoice**, **Customer_Info**, and **Settings** sheets
2.1.   Modify **date** fields in the lists to conform to MySQL format (YYYY/MM/DD)
2.1.1.  The date columns in the sheets are **TEXT** fields, and not numbers
3.  Connect to the MySQL database using environment variables:
3.1.  MYSQL_HOST
3.2.  MYSQL_DATABASE
3.3.  MYSQL_UID
3.4.  MYSQL_PWD
4.  The list of lists data (ranges) are then inserted into **existing** and **empty** database tables:
4.1.  Settings
4.2.  Customer
4.3.  Invoice

## Exceptions and Errors
This first pass of the code is not hardened for the myriad errors that can occur when connecting to Google Sheets or a MySQL database.  When something does fail, the error is normally straightforward.  If it's not
readily apparent where the error lies, there are several **debug print** statements throughout the code to aid in problem detection.
