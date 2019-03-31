import psycopg2
import datetime
from passlib.hash import pbkdf2_sha256
from request import Request
from user import user

current_user = user(None, None, None, None)
user_request = Request(None, None, None, None)


def connect():
    global connection
    # connect to the database
    connection = psycopg2.connect(
        host="127.0.0.1",  # depends on host
        database="internetdata",
        user="postgres",
        password="uD4ph2stu",
        port="5432"
    )


def add_request(kind, value, user):
    global user_request
    connect()
    # cursor for database
    cursor = connection.cursor()
    now = datetime.datetime.now()
    # create a request object and add data to database
    user_request.__init__(kind, value, user, now)
    cursor.execute("INSERT INTO requests (\"UUID\", \"User ID\", \"Kind\", \"Value\", \"Download Status\", \"Date\")"
                   "VALUES (%s, %s, %s, %s, \'False\', %s)",
                   (user_request.uuid, user_request.user.ID, user_request.kind, user_request.value, now))
    # make changes and close the cursor
    connection.commit()
    cursor.close()
    connection.close()


def get_all_requests():
    connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    # returns a tuple where the first index is the row and the second index is the column
    return rows


# I added the user_request parameter so you have to specify which request to update
def update_request(current_request, status, location):
    connect()
    current_request.set_downloaded_status(status)
    current_request.set_file_location(location)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE requests SET \"Download Status\" = \'{current_request.downloaded_status}\', "
                   f"\"File Location\" = \'{current_request.file_location}\' WHERE \"UUID\" = \'{current_request.uuid}\'")
    connection.commit()
    cursor.close()
    connection.close()


# I added this function
# This creates a new user from the user object and inserts the data into the users table
# postgreSQL throws an error if a username is already taken so I didn't add anther check here for now
def new_user(first_name, last_name, username, password):
    global hash
    connect()
    cursor = connection.cursor()
    # password is hashed
    hash = pbkdf2_sha256.encrypt(password)
    current_user = user(first_name, last_name, username, hash)
    # first name, last name, and username converted to lowercase so logging in is not case sensitive
    cursor.execute(f"INSERT INTO users (\"ID\", \"First Name\", \"Last Name\", \"Username\", \"Password\") "
                   f"VALUES (\'{current_user.ID}\', \'{current_user.first_name.lower()}\', "
                   f"\'{current_user.last_name.lower()}\', \'{current_user.username.lower()}\', \'{current_user.password}\')")
    connection.commit()
    cursor.close()
    connection.close()


# I added this function
# This checks if the username and password are correct in order to login
# It then creates a new user object which can be used throughout the program for different purposes
def login(username, password):
    connect()
    cursor = connection.cursor()
    # entered username is converted to lower case to match what is in the database
    cursor.execute(f"SELECT * FROM users WHERE \"Username\" = \'{username.lower()}\'")
    rows = cursor.fetchall()
    hash = rows[0][4]
    cursor.close()
    connection.close()
    # the entered password is compared to the database password using the hash and encryption algorithm
    if pbkdf2_sha256.verify(password, hash):
        ID = str(rows[0][0])
        create_user_object(ID)
        return True
    else:
        return False


# Creates a user object for the current user so that their data can be accessed easily
def create_user_object(uuid_num):
    global current_user
    connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE \"ID\" = \'{uuid_num}\'")
    rows = cursor.fetchall()
    current_user.ID = rows[0][0]
    current_user.first_name = rows[0][1]
    current_user.last_name = rows[0][2]
    current_user.username = rows[0][3]
    current_user.password = rows[0][4]
    cursor.close()
    connection.close()
