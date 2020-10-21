import sqlite3
from datetime import datetime
from server import jobsDBLogic, initializationDb
from server.jobsDBLogic import get_first_job_id

database_path = initializationDb.database_path

def check_if_user_exist_in_db(msg):
    print("in check_if_user_exist_in_db")
    user_id=str(msg["chat"]["id"])
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt="SELECT * FROM Users WHERE userId='"+ user_id+"'"
        c.execute(stmt)
        # Check if the user already exist in the system:
        if c.fetchone() is None:
            # Register new user:
            insert_new_user_to_db(msg)

def insert_new_user_to_db(msg):
    user_id=str(msg["chat"]["id"])
    # user_name=str(msg["chat"]["username"])
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Users VALUES(:userId,:userName,:lastJobThatTheUserViewed,:totalJobThatTheUserViewed,:mail,:affiliation,:lastLogin,:joinDate)",
                  {'userId': user_id ,'userName':  "testt" ,'lastJobThatTheUserViewed':str(jobsDBLogic.get_first_job_id()-1),
                   'totalJobThatTheUserViewed':"0",'mail':"NULL",'affiliation':"NULL" ,'lastLogin':datetime.now().strftime("%x"+" %X")
                    ,'joinDate':datetime.now().strftime("%x")})
        print(c.fetchall())
        conn.commit()

def get_user_affiliation(user_id):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "SELECT affiliation FROM Users WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)
        return c.fetchone()[0]

def get_total_job_that_the_user_viewed(user_id):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "SELECT totalJobThatTheUserViewed FROM Users WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)
        return c.fetchone()[0]

def set_new_professional_affiliation(user_id,professional_affiliation):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "UPDATE Users SET affiliation='" + str(professional_affiliation) + "',lastJobThatTheUserViewed='"+str(get_first_job_id())+ "' WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)

def set_new_mail(user_id,mail):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "UPDATE Users SET mail='" + str(mail) + "' WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)

def delete_mail(user_id):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "UPDATE Users SET mail='NULL' WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)

# Return false if the user doesnt have mail in db, else return true
def check_if_user_already_have_mail(user_id):
    try:
        conn = sqlite3.connect(database_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    with conn:
        stmt = "SELECT mail FROM Users WHERE userId='" + str(user_id) + "'"
        c.execute(stmt)
        ans = c.fetchone()[0]
    if ans == "NULL":
        return False
    return True

