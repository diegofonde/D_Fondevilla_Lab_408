#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("Rideshare.db") # Connect to database 

def startScreen():
    print("Welcome to your RideShare app!")

    print('''Do you have an existing account?:
          1. Yes
          2. No''')
    existing = helper.get_choice([1,2])
    if existing == 2:
        createAccount()
    else: 
        logIn()

def createAccount():
    print('''Do you want a rider account or driver account?:
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
    else: 
        query = '''
        SELECT *
        FROM driver
        '''
        length = len(db_ops.select_query(query)) + 1

        query = '''
        INSERT INTO driver(driverID, driver_mode, avg_rating, num_ratings)
        VALUES(:newID, TRUE, null, 0)
        '''
        newID = {"newID": length}
        db_ops.modify_query_params(query, newID)
        print("Account has successfully been created! Your driverID is ", length)

def logIn():
    print('''Are you logging into a rider account or driver account?:
              1. rider
              2. driver''')
    account = helper.get_choice([1,2])
    if account == 1:
        print("rider log in")
    else:
        driverLog()

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
            SELECT avg_rating
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
                SET driver_mode = TRUE
                WHERE driverID =:driveID
                '''
                driverID = {"driveID":ID}
                db_ops.modify_query_params(query, driverID)
            else: 
                query = '''
                UPDATE driver
                SET driver_mode = FALSE
                WHERE driverID =:driveID
                '''
                driverID = {"driveID":ID}
                db_ops.modify_query_params(query, driverID)
        elif option == 4:
            print("Goodbye!")
            break
    
startScreen()
