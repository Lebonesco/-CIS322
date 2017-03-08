import os
import csv
import psycopg2
import sys

cur = None
conn = None

def main():
    db_name = sys.argv[1]
    port = sys.argv[2]
    input_dir = sys.argv[3]
    
    connect(db_name, port)
    fileDirectory = os.path.abspath(input_dir)
    files = load(fileDirectory)
    
    for file in files:
        lines = csv.reader(file, delimiter=',')
        print(file)
        if "users" in file.name:
            print("Importing Users")
            users(lines)
        elif "assets" in file.name:
            print("Importing Assets")
            assets(lines)
        elif "facilities" in file.name:
            print("Importing facilities")
            facilities(lines)
        elif "transfers" in file.name:
            transfers(lines)

def users(lines):
    global cur
    global conn
    header = next(lines)
    for row in lines:
        print(row)
        name, password, role, active = row[0], row[1], row[2], row[3]

    cur.execute("SELECT user_pk FROM users WHERE username='"+name+"';")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute("SELECT role_pk FROM roles WHERE rolename='"+role+"';")
        role_pk = cur.fetchall()
        if len(role_pk) == 0:
            cur.execute("INSERT INTO roles (rolename) VALUES ('"+role+"');")
            cur.execute("SELECT role_pk FROM roles WHERE rolename='"+role+"';")
            role_pk = cur.fetchall()
        role_pk = role_pk[0]
        cur.execute("INSERT INTO users (username, password, role_fk) VALUES ('"+name+"', '"+password+"', '"+str(role_pk[0])+"');")
        conn.commit()

def assets(lines):
    global cur
    global conn
    header = next(lines)
    for row in lines:
        print(row)
        asset_tag, description, facility = row[0], row[1], row[2]
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
    global cur
    global conn

    for row in lines:
        print(row)
        name = row[1]
        code = row[0]
    cur.execute("SELECT common_name FROM facilities WHERE common_name='"+name+"';")
    results = cur.fetchall()
    if len(results) == 0:
        cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+name+"', '"+code+"');")
    conn.commit()

def transfers(lines):
    pass


def insert(table, keys, values):
    global cur
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
    global cur
    global conn
    connection = "host='localhost' port='" + str(port) + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection)
    cur = conn.cursor()

def load(fileDirectory):
    files = []
    for filename in os.listdir(fileDirectory):
        if filename.endswith(".csv") and not filename.startswith("._"):
            files.append(open(fileDirectory + "/" + filename, "rt"))
    return files

if __name__ == "__main__":
    main()
