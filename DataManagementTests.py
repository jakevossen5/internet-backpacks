import psycopg2
from DataManagement import *


# add_request test
def add_request_test():
    print("Add Request Test: ")
    kind = input("Kind: ")
    value = input("Value: ")
    add_request(kind, value, current_user)


# get_all_requests test
def get_all_requests_test():
    print("Get All Requests Test: ")
    rows = get_all_requests()
    print("(UUID, User ID, Kind, Value, Download Status, File Location, Date)")
    for r in rows:
        print(r)


# update_request test
def update_request_test():
    print("Update Request Test: ")
    update_request(user_request, True, "C:\\\\Users\\william\\Downloads\\File1")
    print("Done")


# new_user test
def new_user_test():
    print("New User Test: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    username = input("Username: ")
    password = input("Password: ")
    new_user(first_name, last_name, username, password)


# login test
def login_test():
    print("Login Test: ")
    username = input("Username: ")
    password = input("Password: ")

    login_success = login(username, password)

    while not login_success:
        print("Incorrect Password. Try Again.")
        username = input("Username: ")
        password = input("Password: ")
        login_success = login(username, password)
        if login_success:
            break

    print("Login Success")


# to print the current user table from the database
def print_user_table():
    connection = psycopg2.connect(
        database="internetdata",
        host="127.0.0.1",
        user="postgres",
        password="uD4ph2stu",
        port="5432"
    )
    print("User Table: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("(ID, First Name, Last Name, Username, Password)")
    for r in rows:
        print(r)
    cursor.close()
    connection.close()


# tests to test all functionality for the data management subsystem
new_user_test()
print_user_table()
login_test()
add_request_test()
get_all_requests_test()
update_request_test()
get_all_requests_test()
print_user_table()
new_user_test()
print_user_table()


# sample test output starting from a blank database
'''
New User Test: 
First Name: William
Last Name: Culver
Username: Willlynx
Password: pa$$word
User Table: 
(ID, First Name, Last Name, Username, Password)
('7e12e697-d7fc-43b8-bd51-9d1825a3eead', 'william', 'culver', 'willlynx', '$pbkdf2-sha256$29000$.1/L.f/fe29tjbF2zhkDAA$OzfEyFc9521q8JMf.tV5fR6g6XLjtCE/sm1JHJ4n7aA')
Login Test: 
Username: willlynx
Password: password
Incorrect Password. Try Again.
Username: willlynx
Password: pa$$word
Login Success
Add Request Test: 
Kind: URL
Value: https://www.google.com
Get All Requests Test: 
(UUID, User ID, Kind, Value, Download Status, File Location, Date)
('a38844ef-4dd0-40c2-b831-69148b19b1ed', '7e12e697-d7fc-43b8-bd51-9d1825a3eead', 'URL', 'https://www.google.com', 'False', None, datetime.datetime(2019, 3, 31, 15, 50, 3, 353700))
Update Request Test: 
Done
Get All Requests Test: 
(UUID, User ID, Kind, Value, Download Status, File Location, Date)
('a38844ef-4dd0-40c2-b831-69148b19b1ed', '7e12e697-d7fc-43b8-bd51-9d1825a3eead', 'URL', 'https://www.google.com', 'True', 'C:\\\\Users\\william\\Downloads\\File1', datetime.datetime(2019, 3, 31, 15, 50, 3, 353700))
User Table: 
(ID, First Name, Last Name, Username, Password)
('7e12e697-d7fc-43b8-bd51-9d1825a3eead', 'william', 'culver', 'willlynx', '$pbkdf2-sha256$29000$.1/L.f/fe29tjbF2zhkDAA$OzfEyFc9521q8JMf.tV5fR6g6XLjtCE/sm1JHJ4n7aA')
New User Test: 
First Name: Billy
Last Name: Bob
Username: bBob1
Password: wordpass
User Table: 
(ID, First Name, Last Name, Username, Password)
('7e12e697-d7fc-43b8-bd51-9d1825a3eead', 'william', 'culver', 'willlynx', '$pbkdf2-sha256$29000$.1/L.f/fe29tjbF2zhkDAA$OzfEyFc9521q8JMf.tV5fR6g6XLjtCE/sm1JHJ4n7aA')
('3b7dfc34-08d4-43be-9d6b-1dcb54b92849', 'billy', 'bob', 'bbob1', '$pbkdf2-sha256$29000$F8L4P.ecc84ZwzjHmLNWCg$q7e8zgEhcPqsVR.6Kd005tERzD2L7tEvRbZ3l8socaI')
'''
