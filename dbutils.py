'''
MIT License

Copyright (c) 2023 Shonil B, Akshada M, Rutuja R, Sakshi B

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import sqlite3

def create_tables(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            usertype TEXT NOT NULL
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        location TEXT,
        job_position TEXT,
        salary INTEGER,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()


def add_client(value_set,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    print(value_set)
    # Inserting rows into the 'client' table
    cursor.execute("INSERT INTO client (name, username, password, usertype) VALUES (?, ?, ?, ?)",
                       value_set)
    conn.commit()
    conn.close()

def get_user_by_username_role(username, usertype, db):
    conn = sqlite3.connect(db)
    print('Data==>', username, usertype)
    cursor = conn.cursor()
    # Querying the 'client' table
    cursor.execute("SELECT * FROM client WHERE username = ? AND usertype=?", (username,usertype))
    rows = cursor.fetchone()
    conn.close()
    return rows


def find_user(data,db):
    conn = sqlite3.connect(db)
    print('Data==>', data)
    cursor = conn.cursor()
    # Querying the 'client' table
    cursor.execute("SELECT * FROM client where username ='"+str(data)+"'")
    rows = cursor.fetchone()
    conn.close()
    print('rowsss->>>', rows)
    return rows


def add_job(data,db):
    conn = sqlite3.connect(db)
    print('Data==>', data)
    cursor = conn.cursor()
    # Inserting rows into the 'jobs' table
    cursor.execute("INSERT INTO jobs (company_name, location, job_position, salary, status) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def get_job_applications(user_name, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE user_name=?",(user_name,))
    rows = cursor.fetchall()  # Use fetchall() to get all rows
    conn.close()
    return rows


def update_job_application_by_id(job_id, company, location, jobposition, salary, status,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Update the 'jobs' table based on jobid
    cursor.execute("UPDATE jobs SET company_name=?, location=?, job_position=?, salary=?, status=? WHERE id=?",
                   (company, location, jobposition, salary, status, job_id))

    conn.commit()
    conn.close()


def delete_job_application_by_job_id(job_id,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Delete the job application from the 'jobs' table based on the company name
    cursor.execute("DELETE FROM jobs WHERE id=?", (job_id,))

    conn.commit()
    conn.close()

def get_job_applications_by_status(db, status):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE status = ?", (status,))
    rows = cursor.fetchall()  # Use fetchall() to get all rows
    conn.close()
    print('rows ->>>', rows)
    return rows



