import mysql.connector
from helper import helper

class db_operations():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = mysql.connector.connect(host="localhost",
            user="root",
            #REPLACE WITH YOUR PASSWORD!!!
            password="insert_password",
            auth_plugin='mysql_native_password',
            database="Rideshare")
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        result = self.cursor.execute(query)
        return result.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()

    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    # function that creates table rider in our database
    def create_rider_table(self):
        query = '''
        CREATE TABLE rider(
            riderID INT NOT NULL PRIMARY KEY
        );
        '''
        self.cursor.execute(query)
        print('Rider Table Created')

    # function that creates table driver in our database
    def create_driver_table(self):
        query = '''
        CREATE TABLE driver(
            driverID INT NOT NULL PRIMARY KEY,
            driverMode BOOLEAN,
            avgRating FLOAT
        );
        '''
        self.cursor.execute(query)
        print('Driver Table Created')

    # function that creates table ride in our database
    def create_ride_table(self):
        query = '''
        CREATE TABLE ride(
            rideID INT NOT NULL PRIMARY KEY,
            pickupLocation VARCHAR(25),
            dropoffLocation VARCHAR(25),
            rating FLOAT,
            riderID INT,
            driverID INT

            FOREIGN KEY (riderID) REFERENCES Rider(riderID)
            FOREIGN KEY (driverID) REFERENCES Driver(driverID)
        );
        '''
        self.cursor.execute(query)
        print('Ride Table Created')

    # function that returns if rider table has records
    def is_rider_empty(self):
        #query to get count of riders in table
        query = '''
        SELECT COUNT(*)
        FROM rider;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function that returns if driver table has records
    def is_rider_empty(self):
        #query to get count of drivers in table
        query = '''
        SELECT COUNT(*)
        FROM driver;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function that returns if rider table has records
    def is_ride_empty(self):
        #query to get count of rides in table
        query = '''
        SELECT COUNT(*)
        FROM ride;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    ## CHANGE/FIX!!!!
    # function to populate rider table given some path
    # to a CSV containing records
    def populate_rider_table(self, filepath):
        if self.is_songs_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO songs VALUES("+placeholders+")"
            self.bulk_insert(query, data)

    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()
