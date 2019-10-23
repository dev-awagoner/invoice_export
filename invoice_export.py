# INVOICE_EXPORT
# Google Sheets export to MySQL

# ASSUMPTIONS
# * MySQL Database and Tables are already configured and running on a server
# * Source sheet names are Invoice, Customer_Info, and Settings
# * Any IDs, Passwords, etc. will be stored in ENVIRONMENT VARIABLES
# * Python packages will be previously installed:
#    * mysql-connector-python
#    * Sheetfu
#
# * Proper credentials and access has been done on the Google side:
#    * https://console.developers.google.com (creation of Service account)
#    * Service User email created in above step is given access (via Sharing) to the Sheet 
#  
# ENVIRONMENT VARIABLES
#    SPREADSHEET_ID
#    SERVICE_ACCESS_FILE
#    MYSQL_HOST
#    MYSQL_UID
#    MYSQL_PWD

import os
from sheetfu import SpreadsheetApp
import mysql.connector
from mysql.connector import Error

# Assign all ENVIRONMENT VARIABLES
try: 
    #print("Checking ENVIRONMENT variables...") 
    SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
    SERVICE_ACCESS_FILE = os.environ['SERVICE_ACCESS_FILE']
    MYSQL_HOST = os.environ['MYSQL_HOST']
    MYSQL_DATABASE = os.environ['MYSQL_DATABASE']
    MYSQL_ID = os.environ['MYSQL_UID']
    MYSQL_PWD = os.environ['MYSQL_PWD']
    #Dummy environment variable
    #MTEST = os.environ['MTEST']
    #print("All environment variables are set.")
except KeyError:  
    print("One or more Environment variables do not exist")

# Debug to make sure the ENVIRONMENT variables are set.

#print(SPREADSHEET_ID)
#print(SERVICE_ACCESS_FILE)
#print(MYSQL_HOST)
#print(MYSQL_DATABASE)
#print(MYSQL_ID)
#print(MYSQL_PWD)

spreadsheet = SpreadsheetApp(SERVICE_ACCESS_FILE).open_by_id(SPREADSHEET_ID)

# If necessary to iterate through spreadsheet
#sheets = spreadsheet.get_sheets()
#for entries in sheets:print(entries)

# Deliberately hardcoding the sheet names and ranges
invoice_sheet = spreadsheet.get_sheet_by_name('Invoice')
invoice_data_range = invoice_sheet.get_range_from_a1(a1_notification='A4:R14')

customer_sheet = spreadsheet.get_sheet_by_name('Customer_Info')
customer_data_range = customer_sheet.get_range_from_a1('A4:R10')

settings_sheet = spreadsheet.get_sheet_by_name('Settings')
settings_data_range = settings_sheet.get_range_from_a1('A2:B10')

# Obtain values from ranges
invoice_values = invoice_data_range.get_values()              # returns a 2D matrix of values
customer_values = customer_data_range.get_values()
settings_values = settings_data_range.get_values()

'''
print("\n==========================")
print(invoice_values)

print("\n==========================")
print(customer_values)

print("\n==========================\n")
print(settings_values)
'''

# MySQL Connection
try:
    connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DATABASE, user=MYSQL_ID, password=MYSQL_PWD)

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version: ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You are connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")