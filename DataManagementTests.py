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
    usernameAvailable = new_user(first_name, last_name, username, password)
    while not usernameAvailable:
        print("That username is taken please choose another.")
        username = input("Username: ")
        password = input("Password: ")
        usernameAvailable = new_user(first_name, last_name, username, password)
        if usernameAvailable:
            break


# login test
def login_test():
    print("Login Test: ")
    username = input("Username: ")
    password = input("Password: ")

    login_success = login(username, password)

    while not login_success:
        print("Incorrect Username or Password. Try Again.")
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
('36c984dc-5b3d-4733-9c20-b638765b7657', 'william', 'culver', 'willlynx', '$pbkdf2-sha256$29000$E4IQwjiHUEpJae0do9Qaww$xBDNUFsX3G6yVnNlsqpTZzPp0YQ26cCZxWnKqBv3PZg')
Login Test: 
Username: willlynx
Password: password
Incorrect Username or Password. Try Again.
Username: will
Password: pa$$word
Incorrect Username or Password. Try Again.
Username: willlynx
Password: pa$$word
Login Success
Add Request Test: 
Kind: URL
Value: https://www.google.com
Get All Requests Test: 
(UUID, User ID, Kind, Value, Download Status, File Location, Date)
('4a9d96e8-3ec4-40cc-983a-bd92bc05fab9', '36c984dc-5b3d-4733-9c20-b638765b7657', 'URL', 'https://www.google.com', 'False', None, datetime.datetime(2019, 4, 2, 19, 55, 42, 785000))
Update Request Test: 
Done
Get All Requests Test: 
(UUID, User ID, Kind, Value, Download Status, File Location, Date)
('4a9d96e8-3ec4-40cc-983a-bd92bc05fab9', '36c984dc-5b3d-4733-9c20-b638765b7657', 'URL', 'https://www.google.com', 'True', 'C:\\\\Users\\william\\Downloads\\File1', datetime.datetime(2019, 4, 2, 19, 55, 42, 785000))
New User Test: 
First Name: 
Last Name: 
Username: Willlynx
Password: pass
That username is taken please choose another.
Username: BillyBob
Password: pass
User Table: 
(ID, First Name, Last Name, Username, Password)
('6f2f477a-e7c7-4fca-bec4-414ba0d0b579', 'william', 'culver', 'willlynx', '$pbkdf2-sha256$29000$0tq7N2ZsjdEag1AKoTTG2A$GHUQSW5Hd9SvTSmI3flnCCqa924ftCI9iCufSsh1gKg')
('a9be6453-5d34-4599-bb7e-8e44c52fbb2e', '', '', 'billybob', '$pbkdf2-sha256$29000$vdeac661thYixLhXqlVqDQ$zHziXsJVwLDsPdo25FQmy3V6UiFqG4XQr5Sccy0qr70')
'''
