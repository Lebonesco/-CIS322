import os
import csv
import psycopg2
import sys

cursor = None
conn = None

def main():
    db_name = sys.argv[0]
    port = sys.argv[1]
    connect(db_name, port)
    fileDirectory = os.path.dirname(os.path.abspath("../files/lost_data"))
    files = load(fileDirectory)
    for file in files:
        lines = csv.reader(file, delimiter=',')
        if "users" in file.name:

        elif "assets" in file.name:

        elif "facilities" in file.name:

        elif "transfers" in file.name:


def users(lines):
    global cursor
    global conn
    cur.execute("SELECT user_pk FROM users WHERE username='"+name+"';")
    result = cur.fetchall()
    if len(result) == 0:
        cursor.execute("SELECT role_pk FROM roles WHERE rolename='"+role+"';")
        role_pk = cur.fetchall()
        if len(role_pk) == 0:
            cur.execute("INSERT INTO roles (rolename) VALUES ('"+role+"');")
            cur.execute("SELECT role_pk FROM roles WHERE rolename='"+role+"';")
            role_pk = cur.fetchall()
        role_pk = role_pk[0]
        cur.execute("INSERT INTO users (username, password, role_fk) VALUES ('"+name+"', '"+password+"', "+role_pk[0]+");")
        conn.commit()

def assets(lines):
    global cursor
    global conn
    cur.execute("SELECT facility_pk FROM facilities WHERE fcode='"+facility+"';")
    facility_pk = cur.fetchall()
    if len(facility_pk) == 0:
        cur.execute("INSERT INTO facility (common_name, fcode) VALUES ('"+facility+"', '"+facility+"');")
        cur.execute("SELECT facility_pk FROM facilities WHERE fcode='"+facility+"';")
        facility_pk = cur.fetchall()
    facility_pk = facility_pk[0]
    cur.execute("INSERT INTO assets (asset_tag, description, facility_fk, arrive_dt, depart_dt) VALUES ('"+asset_tag+"','"+description+"','"+facility_pk[0]+"','"+arrive_dt+"','"+depart_dt+"');")
    conn.commit()

def facilities(lines):
    global cursor
    global conn
    cur.execute("SELECT common_name FROM facilities WHERE common_name='"+name+"';")
    results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+name+"', '"+code+"');")
    conn.commit()

def tranfers(lines):
    pass


def insert(table, keys, values):
    global cursor
    global conn
    valueResult = ""

    for i in range(len(values)):
    if type(values[i]) == str:
        valueResult += "'" + values[i] +  "'"
    else:                                   
        valueResult += str(values[i])
    
    if i < len(values) - 1:        
        valueResult += ","
                                                                                                         
    print("INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), valueResult))
    cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), valueResult))
    conn.commit()


def connect(db_name, port):
    global cursor
    global conn
    connection = "host='localhost' port='" + str(port) + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()

if __name__ == "__main__":
    main()
