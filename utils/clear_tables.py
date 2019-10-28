# CLEAR_TABLES
# Clearing data from MySQL CLEAR_TABLES

# ASSUMPTIONS
# * We only want to clear the data, not drop the tables
# * Table names are Invoice, Customer, and Settings
# * Any IDs, Passwords, etc. will be stored in ENVIRONMENT VARIABLES
# * Python packages will be previously installed:
#    - mysql-connector-python
#  
# ENVIRONMENT VARIABLES
#   MYSQL_HOST
#   MYSQL_DATABASE
#   MYSQL_UID
#   MYSQL_PWD

from datetime import datetime
import os
import sys
import mysql.connector
from mysql.connector import Error

env_vars = ['MYSQL_HOST', 'MYSQL_DATABASE', 'MYSQL_UID', 'MYSQL_PWD']

# Check and Assign ENVIRONMENT VARIABLES
print("Checking if all environment variables are set..", end='.')

missing = set(env_vars) - set(os.environ)
if missing:
    print("\nEnvironment variables that do not exist: %s" % missing)
    sys.exit()
else:
    print("OK.")
    try: 
        MYSQL_HOST = os.environ['MYSQL_HOST']
        MYSQL_DATABASE = os.environ['MYSQL_DATABASE']
        MYSQL_ID = os.environ['MYSQL_UID']
        MYSQL_PWD = os.environ['MYSQL_PWD']

    except KeyError:  
        print("A problem with one of the environment variables exists.")
        print("Exiting")
        sys.exit()

# MySQL Connection
try:
    connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DATABASE, user=MYSQL_ID, password=MYSQL_PWD)

    if connection.is_connected():
        cursor = connection.cursor()

        print("Clearing Settings data...", end=".")
        cursor.execute("DELETE from Settings;")
        connection.commit()
        print("COMPLETE [", datetime.now(), "]")

        print("Clearing Customer data...", end=".")
        cursor.execute("DELETE from Customer;")
        connection.commit()
        print("COMPLETE [", datetime.now(), "]")

        print("Clearing Invoice data...", end=".")
        cursor.execute("DELETE from Invoice;")
        connection.commit()
        print("COMPLETE [", datetime.now(), "]")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
