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
    print("OK.")
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

# Deliberately hardcoding the sheet names and ranges
invoice_sheet = spreadsheet.get_sheet_by_name('Invoice')
invoice_data_range = invoice_sheet.get_range_from_a1('A4:R14')

customer_sheet = spreadsheet.get_sheet_by_name('Customer_Info')
customer_data_range = customer_sheet.get_range_from_a1('A4:R10')

settings_sheet = spreadsheet.get_sheet_by_name('Settings')
settings_data_range = settings_sheet.get_range_from_a1('A2:B9')

# Obtain values from ranges
invoice_values = invoice_data_range.get_values()        # returns a 2D matrix of values
customer_values = customer_data_range.get_values()
settings_values = settings_data_range.get_values()

print("\n==========================")
print(invoice_values)

print("\n==========================")
print(customer_values)

print("\n==========================\n")
print(settings_values)


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

        mySql_Item_Insert_Query = "INSERT INTO Item(description, id) VALUES(%s,%s)"
        cursor = connection.cursor()
        result = cursor.executemany(mySql_Item_Insert_Query, settings_values)
        connection.commit()
        print("Record inserted successfully into Item table")
        cursor.close()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


'''
def main():
   # books = [('Harry Potter And The Order Of The Phoenix', '9780439358071'),
   #      ('Gone with the Wind', '9780446675536'),
   #          ('Pride and Prejudice (Modern Library Classics)', '9780679783268')]
    insert_item(settings_values)

if __name__ == '__main__':
    main()

def insert_item(description, id):
    query = "INSERT INTO books(description, id) " \
            "VALUES(%s,%s)"
    args = (description, id)
'''