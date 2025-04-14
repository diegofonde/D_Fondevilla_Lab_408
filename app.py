#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("Rideshare.db") # Connect to database 

#functions
def startScreen():
    print("Welcome to your Ride Share app!")

    #db_ops.create_rider_table()
    #db_ops.create_driver_table()
    #db_ops.create_ride_table()

    print('''Do you have an existing account?:
          1. Yes
          2. No''')
    existing = helper.get_choice([1,2])
    if existing == 1:
        login()
    elif existing == 2:
        createAccount()
    else: 
        print("Invalid input. Select option 1 or 2.")

def createAccount():
    print('''Choose a rider account or driver account:
              1. rider
              2. driver''')
    account = helper.get_choice([1,2])
    if account == 1:
        query = '''
        SELECT *
        FROM rider
        '''
        length = len(db_ops.select_query(query)) + 1

        query = '''
        INSERT INTO rider(riderID)
        VALUES(:newID)
        '''
        newID = {"newID": length}
        db_ops.modify_query_params(query, newID)
        print("Account has successfully been created! Your riderID is ", length)
    elif account == 2: 
        query = '''
        SELECT *
        FROM driver
        '''
        length = len(db_ops.select_query(query)) + 1

        query = '''
        INSERT INTO driver(driverID, driverMode, avgRating)
        VALUES(newID, TRUE, null))
        '''
        newID = {"newID": length}
        db_ops.modify_query_params(query, newID)
        print("Account has successfully been created! Your driverID is ", length)
    else:
        print("Invalid input. Select option 1 or 2.")

def login():
    print('''Are you logging into a rider account or driver account?:
              1. rider
              2. driver''')
    account = helper.get_choice([1,2])
    if account == 1:
        #riderLog()
        print("rider log")
    else:
        driverLog()

# for driver users
def driverLog():
    ID = input("Please enter your driverID: ")
    while True:
        print('''Select from the following options:
              1. View rating
              2. View rides
              3. Activate/Deactivate Driver Mode
              4. Exit''')
        option = helper.get_choice([1,2,3,4])
        if option == 1:
            query = '''
            SELECT avgRating
            FROM driver
            WHERE driverID =:driveID
            '''
            driverID = {"driveID":ID}
            ratings = db_ops.select_query_params(query, driverID)

            if ratings[0][0] is None:
                print("You do not have a rating.")
            else:
                print("Your rating is ", ratings[0][0])
        elif option == 2:
            query = '''
            SELECT * 
            FROM driver
            INNER JOIN ride
            ON driver.driverID = ride.driverID
            WHERE driver.driverID =:driveID
            '''
            driverID = {"driveID":ID}
            ride_list = db_ops.select_query_params(query, driverID)

            for row in ride_list:
                print(row)

        elif option == 3:
            print('''Do you want to activate or deactivate your account?:
              1. Activate
              2. Deactivate
            ''')
            option = helper.get_choice([1,2])
            if option == 1:
                query = '''
                UPDATE driver
                SET driverMode = TRUE
                WHERE driverID =:driveID
                '''
                driverID = {"driveID":ID}
                db_ops.modify_query_params(query, driverID)
            else: 
                query = '''
                UPDATE driver
                SET driverMode = FALSE
                WHERE driverID =:driveID
                '''
                driverID = {"driveID":ID}
                db_ops.modify_query_params(query, driverID)
        elif option == 4:
            print("Goodbye!")
            break

# for rider users 
# def riderLog():
#     ID = input("Please enter your driverID: ")
#     while True:
#         print('''Select from the following options:
#               1. View rides
#               2. Find an active driver
#               3. Exit''')
#         option = helper.get_choice([1,2,3])
        
#         # 1. view rides
#         if option == 1:
#             query = '''
#                 SELECT *
#                 FROM ride
#                 WHERE riderID = %s
#             '''
#             driverID = {"driverID": ID}
#             rides = db_ops.select_query_params(query, driverID)
#             if rides:
#                 print("Your Ride History:")
#                 helper.pretty_print(rides)
#             else:
#                 print("No previous rides found.")
#         # 2. find an active driver
#         elif option == 2:
#             query = '''
#                 SELECT driverID
#                 FROM driver
#                 WHERE driverMode = TRUE
#             '''
#             drivers = db_ops.select_query(query)
#             if not drivers:
#                 print("No drivers available at the moment.")
#             driverID = drivers[0][0]
#             pickup = input("Enter pick-up location: ")
#             dropoff = input("Enter drop-off location: ")

#             query = '''
#                 INSERT INTO ride(rideID, pickupLocation, dropoffLocation, rating, riderID, driverID)
#                 VALUES(%s, %s, %s, %s, %s, %s)
#             '''
#             # fix
#             params = (rideID, pickup, dropoff, None, riderID, driverID)
#             db_ops.modify_query_params(query, params)
#         # 3. exit
#         elif option == 3:
#             print("Return to options...")
#             break

# main method 
startScreen()
