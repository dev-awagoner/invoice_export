# Google Sheets export to MySQL
A project to export a known Google Spreadsheet to a known MySQL database

The assumption is that none of the USERIDs, passwords, connections will be hard-coded, but will use environment variables on the local system.

##Requirements
The current requirements are:
1.  Python 3.7+ (earlier 3.x code may work, but has not been tested).
2.  [Sheetfu](https://github.com/socialpoint-labs/sheetfu) - A very nice library for connecting to Google Sheets using to Python.