# INVOICE_EXPORT
# Google Sheets export to MySQL

# ASSUMPTIONS
# * MySQL Database and Tables are already configured and running on a server
# * Source sheet names are Invoice, Customer_Info, and Settings
# * Any IDs, Passwords, etc. will be stored in ENVIRONMENT VARIABLES
# * Python packages will be previously installed:
#    - mysql-connector-python
#    - Sheetfu
#
# * Proper credentials and access has been done on the Google side:
#    - https://console.developers.google.com (creation of Service account)
#    - Service User email created in above step is given access (via Sharing) to the Sheet 
#  
# ENVIRONMENT VARIABLES
#    SPREADSHEET_ID
#    SERVICE_ACCESS_FILE
#    MYSQL_HOST
#    MYSQL_UID
#    MYSQL_PWD

import datetime
import os
import sys
from sheetfu import SpreadsheetApp
import mysql.connector
from mysql.connector import Error

env_vars = ['SPREADSHEET_ID', 'SERVICE_ACCESS_FILE', 'MYSQL_HOST', 'MYSQL_DATABASE',
            'MYSQL_UID', 'MYSQL_PWD']

# Check and Assign ENVIRONMENT VARIABLES
print("Checking if all environment variables are set..", end='.')

missing = set(env_vars) - set(os.environ)
if missing:
    print("\nEnvironment variables that do not exist: %s" % missing)
    sys.exit()
else:
    print("COMPLETE")
    try: 
        SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
        SERVICE_ACCESS_FILE = os.environ['SERVICE_ACCESS_FILE']
        MYSQL_HOST = os.environ['MYSQL_HOST']
        MYSQL_DATABASE = os.environ['MYSQL_DATABASE']
        MYSQL_ID = os.environ['MYSQL_UID']
        MYSQL_PWD = os.environ['MYSQL_PWD']

    except KeyError:  
        print("A problem with one of the environment variables exists.")
        print("Exiting")
        sys.exit()

# Add try block to handle case where SERVICE_ACCESS_FILE or SPREADSHEET_ID
# do not exist, or incorrect.  
# Add a fileExists check for SERVICE_ACCESS_FILE ?
# Add HttpError if spreadsheet does not exist ?
spreadsheet = SpreadsheetApp(SERVICE_ACCESS_FILE).open_by_id(SPREADSHEET_ID)

# If necessary to iterate through spreadsheet
#sheets = spreadsheet.get_sheets()
#for entries in sheets:print(entries)

# Deliberately hardcoding the Invoice sheet name and ranges (NEED TO DETERMINE RANGE)
# Invoice Sheet
invoice_sheet = spreadsheet.get_sheet_by_name('Invoice')
invoice_data_range = invoice_sheet.get_range_from_a1('A4:Q14')
invoice_values = invoice_data_range.get_values()    # returns a 2D matrix of values
data_range = invoice_sheet.get_data_range()

print(data_range.get_values())
#inv_data_range = 