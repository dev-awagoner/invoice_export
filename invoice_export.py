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
#    - Service account credentials (JSON) downloaded to a known directory
#    - Service User email created in above step is given access (via Sharing) to the Sheet 
#  
# ENVIRONMENT VARIABLES
#    SPREADSHEET_ID
#    SERVICE_ACCESS_FILE
#    MYSQL_HOST
#    MYSQL_DATABASE
#    MYSQL_UID
#    MYSQL_PWD

import datetime
import os
import sys
from sheetfu import SpreadsheetApp
import mysql.connector
from mysql.connector import Error

class DatabaseConnect:
    def __init__(self, config: dict):
        self.configuration = config

    def __enter__(self) -> 'cursor':
        # Connect to database and create a DB cursor.
        # Return the database cursor to the context manager.
        
        try:
            print("Connecting to MySQL..", end=".")
            self.connection = mysql.connector.connect(**self.configuration)
            
            if self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.configuration)
                self.cursor = self.connection.cursor()
                print("CONNECTED")
                return self.cursor

        except Error as e:
            print("Error while connecting to MySQL", e)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Destroy the cursor as well as the connection (after committing).
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("MySQL connection...CLOSED")

# Setting the expected ENVIRONMENT VARIABLES
env_vars = {
    'sheet_id': 'SPREADSHEET_ID',
    'service_access_file': 'SERVICE_ACCESS_FILE',
    'host': 'MYSQL_HOST',
    'database': 'MYSQL_DATABASE',
    'user': 'MYSQL_UID',
    'password': 'MYSQL_PWD'
}

# Checking existence of ENVIRONMENT VARIABLES and updating the dictionary
print("Checking environment variables..", end='.')

missing = set(env_vars.values()) - set(os.environ)
if missing:
    print("\nEnvironment variables that are not set: %s" % missing)
    sys.exit()
else:
    try:
        env_vars = {k: os.environ.get(v) for k, v in env_vars.items() if v in os.environ}
        
    except KeyError:  
        print("A problem with one or more of the environment variables exists...EXITING")
        sys.exit()

# Create a dictionary subset of ENV_CONFIG for just the MySQL parameters
db_config = {k: env_vars[k] for k in env_vars.keys() & {'host', 'database', 'user', 'password'}}
print("COMPLETE")

# Add try block to handle case where SERVICE_ACCESS_FILE or SPREADSHEET_ID do not exist, or are incorrect?  
# Add a fileExists check for SERVICE_ACCESS_FILE ?
# Add HttpError if spreadsheet does not exist ?

print("Connecting to Spreadsheet..", end='.')
spreadsheet = SpreadsheetApp(env_vars.get('service_access_file')).open_by_id(env_vars.get('sheet_id'))
print("CONNECTED")

# If necessary to iterate through spreadsheet
#sheets = spreadsheet.get_sheets()
#for entries in sheets:print(entries)

# Deliberately hardcoding the Invoice sheet name
# Invoice Sheet
invoice_sheet = spreadsheet.get_sheet_by_name('Invoice')
invoice_sheet_range = invoice_sheet.get_data_range()
invoice_values = invoice_sheet_range.get_values()   # returns a 2d matrix of lists

# Faster than a slice (invoice_values[2:-1]).  It's necessary to remove the 3 header columns.
invoice_values.pop(0); invoice_values.pop(0); invoice_values.pop(0)

# Change INVOICE DATEs format (DD/MM?YYY -> YYYY/MM/DD) to import into MySQL date column
for row in invoice_values:
    row[1] = datetime.datetime.strptime(row[1], '%d/%m/%Y').strftime('%Y/%m/%d')

# Deliberately hardcoding the Customer sheet name 
# Customer_Info Sheet
customer_sheet = spreadsheet.get_sheet_by_name('Customer_Info')
customer_sheet_range = customer_sheet.get_data_range()
customer_values = customer_sheet_range.get_values()

# Faster than a slice (customer_values[2:-1]).  It's necessary to remove the 3 header columns.
customer_values.pop(0); customer_values.pop(0); customer_values.pop(0)

# Change CUSTOMER DATEs format (DD/MM?YYY -> YYYY/MM/DD) to import into MySQL date column
for row in customer_values:
    row[1] = datetime.datetime.strptime(row[1], '%d/%m/%Y').strftime('%Y/%m/%d')
    row[2] = datetime.datetime.strptime(row[2], '%d/%m/%Y').strftime('%Y/%m/%d')

# Deliberately hardcoding the Settings sheet name 
# Settings Sheet
settings_sheet = spreadsheet.get_sheet_by_name('Settings')
settings_sheet_range = settings_sheet.get_data_range()
settings_values = settings_sheet_range.get_values()

# Faster than a slice (invoice_values[1:-1]).  It's necessary to remove the single header column.
settings_values.pop(0)

# DEBUG Code to verify *_values
#print("\n==========================")
#print(invoice_values)
#print("\n==========================")
#print(customer_values)
#print("\n==========================\n")
#print(settings_values)


with DatabaseConnect(db_config) as cursor:
    # Insert SETTINGS data
    print("Inserting Settings data..", end=".")
    Item_Insert_Query = "INSERT INTO settings(description, id) VALUES(%s,%s)"

    # Technically don't need to use result unless it's necessary to check
    # the results of cursor.executemany()
    result = cursor.executemany(Item_Insert_Query, settings_values)
    print("COMPLETE")

    # Insert CUSTOMER data
    print("Inserting Customer data..", end=".")
    Customer_Insert_Query = "INSERT INTO customer(cycle, start_date, end_date, item, price, " \
                                "iva, total, customer_id, business_name, business_id, contact, address, " \
                                "city, province, postcode, email, phone, phone2) " \
                                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    result = cursor.executemany(Customer_Insert_Query, customer_values)
    print("COMPLETE")

    # Insert INVOICE data
    print("Inserting Invoice data...", end=".")
    Invoice_Insert_Query = "INSERT INTO invoice(invoice_number, date, item, price, iva, total, " \
                               "customer_id, business_name, business_id, contact, address, city, " \
                               "province, postcode, email, phone, phone2) " \
                               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    result = cursor.executemany(Invoice_Insert_Query, invoice_values)
    print("COMPLETE")
