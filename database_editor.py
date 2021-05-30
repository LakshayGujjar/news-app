#file to work with db

import sqlite3

con = sqlite3.connect("users.db")
cursor_obj = con.cursor()

#cursor_obj.execute("CREATE TABLE users (email_id text PRIMARY KEY,name text,password text,gender text,status text)")

cursor_obj.execute('ALTER TABLE users ADD COLUMN id number')

con.commit()
con.close()