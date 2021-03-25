
import psycopg2
from psycopg2 import Error
import os

def create_connection():
    connection = None
    try:
        # Connect to an existing database
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        connection = psycopg2.connect(
                     dbname=dbname,
                     user=user,
                     password=password,
                     host=host,
                     port=port
                     )


        # connection = psycopg2.connect(user="postgres", password="juandaxdd", host="127.0.0.1",port="5432", dbname="postgres")
        # print(connection)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    
    return connection


#PRODUCTION

# import psycopg2
# import urllib.parse as urlparse
# import os

#PROD
# url = urlparse.urlparse(os.environ['DATABASE_URL'])
# dbname = url.path[1:]
# user = url.username
# password = url.password
# host = url.hostname
# port = url.port

# con = psycopg2.connect(
#             dbname=dbname,
#             user=user,
#             password=password,
#             host=host,
#             port=port
#             )

