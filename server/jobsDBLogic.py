import sqlite3
from datetime import datetime
from server import initializationDb
database_path = initializationDb.database_path

def insert_job(new_job):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Student_Jobs(name,link,description,site_name,upload_date,affiliation1,affiliation2) "
                  "VALUES ( :name, :link, :description, :site_name,:upload_date,:affiliation1,:affiliation2)",
                  { 'name': new_job.job_name,'link': new_job.link,'description': new_job.description , 'site_name': new_job.site_name,
                    'upload_date':datetime.now().strftime("%x"+" %X"),'affiliation1':new_job.affiliation1,'affiliation2':new_job.affiliation2})

def get_exist_job(user_id_in_telegram):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    last_job_id_in_db=int(get_last_job_id())
    with conn:
        # Get the last job id that the user viewed:
        stmt = "SELECT * FROM Users WHERE userId='" + str(user_id_in_telegram) + "'"
        print(stmt)
        job_list=[]
        c.execute(stmt)
        user_tupple = c.fetchall()
        last_job_that_the_user_viewed = user_tupple[0][2]
        total_job_that_the_user_viewed= user_tupple[0][3]
        user_affiliation = user_tupple[0][5]
        # Check if we have another job in db that the user has not seen:
        while int(last_job_that_the_user_viewed) < int(last_job_id_in_db):
            job_that_the_user_didnt_viewed = str(int(last_job_that_the_user_viewed) + 1)
            last_job_that_the_user_viewed=job_that_the_user_didnt_viewed
            stmt = "UPDATE Users SET lastJobThatTheUserViewed='" + str(
                last_job_that_the_user_viewed) + "' WHERE userId='" + str(user_id_in_telegram) + "'"
            c.execute(stmt)
            # update_last_job_that_the_user_viewed(last_job_that_the_user_viewed, user_id_in_telegram)
            stmt = "SELECT affiliation FROM Users WHERE userId='" + str(user_id_in_telegram) + "'"
            c.execute(stmt)
            job_details = get_job_tupple(job_that_the_user_didnt_viewed,user_affiliation)
            if job_details is not None:
                total_job_that_the_user_viewed= str(int(total_job_that_the_user_viewed) + 1)
                stmt = "UPDATE Users SET totalJobThatTheUserViewed='" + total_job_that_the_user_viewed + "' WHERE userId='" + str(user_id_in_telegram) + "'"
                c.execute(stmt)
                job_list.append(job_details)
        return job_list

def update_last_job_that_the_user_viewed(last_job_that_the_user_viewed,user_id_in_telegram):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "UPDATE Users SET lastJobThatTheUserViewed='" + str(
                last_job_that_the_user_viewed) + "' WHERE userId='" + str(user_id_in_telegram) + "'"
        c.execute(stmt)

def update_total_jobs_that_the_user_viewed(total_job_that_the_user_viewed,user_id_in_telegram):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "UPDATE Users SET totalJobThatTheUserViewed='" + str(int(total_job_that_the_user_viewed)+1) + "' WHERE userId='" +  str(user_id_in_telegram) + "'"
        c.execute(stmt)

def get_job_tupple(job_id,user_affiliation):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "SELECT * FROM Student_Jobs WHERE (id='" + job_id + "'"+" AND affiliation1='"+user_affiliation+"')"
        print(stmt)
        c.execute(stmt)
        job_tupple = c.fetchone()
        print(job_tupple)
        return job_tupple



def get_first_job_id():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "SELECT MIN(id) FROM Student_Jobs"
        c.execute(stmt)
        last_job_id=c.fetchone()[0]
        return last_job_id
        # return 1

def get_last_job_id():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        # Get the last job id in Jobs table
        stmt = "SELECT MAX(id) FROM Student_Jobs"
        c.execute(stmt)
        last_job_id=c.fetchone()[0]
        return last_job_id

def check_if_job_already_exist_in_db(job_link):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "SELECT * FROM Student_Jobs WHERE link='" + job_link + "'"
        print(stmt)
        c.execute(stmt)
        job_tupple = c.fetchone()
        if job_tupple is None:
            return False
        return True

def get_all_job_links_in_db():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "SELECT link FROM Student_Jobs"
        print(stmt)
        c.execute(stmt)
        job_link_tupple = c.fetchall()
        print(type(job_link_tupple))
        return job_link_tupple

def delete_job_from_db(job_link):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        stmt = "DELETE FROM Student_Jobs WHERE link='" + job_link + "'"
        print(stmt)
        c.execute(stmt)

