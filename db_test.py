import sqlite3

db_conn = sqlite3.connect("test.db")
while True:
    cmd = input("Enter the query you would like to run:\n")
    c = db_conn.cursor()
    print("Command: %s \n" % cmd)
    print(c.execute(cmd).)
    for row in c.execute(cmd):
        print(row)
