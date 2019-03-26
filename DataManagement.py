import psycopg2
import datetime
from request import request
from user import user

# connect to the database
connection = psycopg2.connect(
    host = "",  # depends on host
    database = "internetdata",
    user = "postgres",
    password = "",
    port = "5432"
)

current_user = user(None, None, None, None)


def add_request(kind, value, user):
    # cursor
    cursor = connection.cursor()
    now = datetime.datetime.now()
    # create a request object and add data to database
    user_request = request(kind, value, user, now)
    cursor.execute("INSERT INTO requests VALUES (%s, %s, %s, %s)", (user_request.kind, user_request.value,
                                                                    user_request.user.ID, now))
    # make changes and close the cursor
    connection.commit()
    cursor.close()


def get_all_requests():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()
    cursor.close()
    # returns a tuple where the first index is the row and the second index is the column
    return rows


# I added the user_request parameter so you have to specify which request to update
def update_request(user_request, status, location):
    user_request.set_downloaded_status(status)
    user_request.set_file_location(location)


# I added this function
# This creates a new user from the user object and inserts the data into the users table
# postgreSQL throws an error if a username is already taken so I didn't add anther check here for now
def new_user(first_name, last_name, username, password):
    cursor = connection.cursor()
    current_user = user(first_name, last_name, username, password)
    cursor.execute("INSERT INTO users (\"First Name\", \"Last Name\", \"Username\", \"Password\") "
                   "VALUES (%s, %s, %s, %s)",
                   (current_user.first_name, current_user.last_name, current_user.username, current_user.password))
    connection.commit()
    cursor.close()


# I added this function
# This checks if the username and password are correct in order to login
# It then creates a new user which can be used throughout the program for different purposes
def login():
    cursor = connection.cursor()
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute(f"SELECT * FROM users WHERE \"Username\" = \'{username}\'")
    rows = cursor.fetchall()
    if rows[0][4] == password:
        print("Login Success")
        ID = rows[0][0]
        create_user_object(ID)
        cursor.close()
        return True
    else:
        print("Incorrect Password. Try Again.")
        return False


# Creates a user object for the current user so that their data can be accessed easily
def create_user_object(id_num):
    global current_user
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE \"ID\" = %s", str(id_num))
    rows = cursor.fetchall()
    current_user.ID = rows[0][0]
    current_user.first_name = rows[0][1]
    current_user.last_name = rows[0][2]
    current_user.username = rows[0][3]
    current_user.password = rows[0][4]
    cursor.close()


# Login loop for testing purposes

login_success = login()

while not login_success:
    login_success = login()
    if login_success:
        break

# # more testing stuff
# fn = input("Enter your first name: ")
# ln = input("Enter your last name: ")
# un = input("Enter a username: ")
# pw = input("Enter a password: ")
#
# new_user(fn, ln, un, pw)


# closes database connection
connection.close()
