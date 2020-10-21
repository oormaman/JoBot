import sqlite3

database_path =r"C:\Users\oorma\PycharmProjects\pythonProject4\server\bot_db.db"

def initialize_users_table_in_db():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        c.execute('''CREATE TABLE Users (
                            userId TEXT,
                            userName TEXT,
                            lastJobThatTheUserViewed TEXT,
                            totalJobThatTheUserViewed TEXT,
                            mail TEXT,
                            affiliation TEXT,
                            lastLogin TEXT,
                            joinDate TEXT); ''')
        conn.commit()

def initialize_student_jobs_table_in_db():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    with conn:
        c.execute('''CREATE TABLE Student_Jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                link TEXT,
                description TEXT,
                site_name TEXT,
                upload_date TEXT,
                affiliation1 TEXT,
                affiliation2 TEXT);
            ''')
        conn.commit()


def main():
    initialize_users_table_in_db()
    initialize_student_jobs_table_in_db()

if __name__=="__main__":
    main()

