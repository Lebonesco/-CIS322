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
    
    order = {"users": 0, "facilities": 1, "assets": 2, "transfers": 3}
    def byName(file):
        for item in order:
            if item in file.name:
                return order[item]
    files = sorted(files, key=byName)
    
    for file in files:
        lines = csv.reader(file, delimiter=',')
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
            print("Importing Transfers")
            transfers(lines)

def users(lines):
    global cur
    global conn
    header = next(lines)
    for row in lines:
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
            cur.execute("INSERT INTO users (username, password, role_fk, active) VALUES ('"+name+"', '"+password+"', '"+str(role_pk[0])+"', "+active+");")
            conn.commit()

def assets(lines):
    global cur
    global conn
    header = next(lines)
    for row in lines:
        asset_tag, description, facility, arrive_dt, depart_dt = row[0], row[1], row[2], row[3], row[4]
        cur.execute("SELECT facility_pk FROM facilities WHERE code='"+facility+"';")
        facility_pk = cur.fetchall()
        if len(facility_pk) == 0:
            cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+facility+"', '"+facility+"');")
            cur.execute("SELECT facility_pk FROM facilities WHERE code='"+facility+"';")
            facility_pk = cur.fetchall()
        facility_pk = facility_pk[0]
        cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('"+asset_tag+"','"+description+"');")
        conn.commit()
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='"+asset_tag+"';")
        asset_fk = cur.fetchone()
        if depart_dt == 'NULL':
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ('"+str(asset_fk[0])+"','"+str(facility_pk[0])+"','"+str(arrive_dt)+"');")
        else:
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) VALUES ('"+str(asset_fk[0])+"','"+str(facility_pk[0])+"','"+str(arrive_dt)+"','"+depart_dt+"');")
        conn.commit()

def facilities(lines):
    global cur
    global conn

    for row in lines:
        name = row[1]
        code = row[0]
        cur.execute("SELECT common_name FROM facilities WHERE common_name='"+name+"';")
        results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+name+"', '"+code+"');")
        conn.commit()

def transfers(lines):
    global cur
    global conn
    header = next(lines)
    for row in lines:
        asset_tag, request_by, request_dt, approve_by, approve_dt, source, destination, load_dt, unload_dt = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
        
        cur.execute("SELECT user_pk FROM users WHERE username='"+request_by+"';")
        requester_fk = cur.fetchall()
        cur.execute("SELECT facility_pk FROM facilities WHERE code='"+source+"';")
        source_fk = cur.fetchall()
        cur.execute("SELECT facility_pk FROM facilities WHERE code='"+destination+"';")
        destination_fk = cur.fetchall()
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='"+asset_tag+"';")
        asset_fk = cur.fetchall()
        
        cur.execute("INSERT INTO requests (requester_fk, request_data, approval_data, source_fk, destination_fk, assset_fk) VALUES ('"+str(requester_fk[0][0])+"', '"+request_dt+"','"+approve_dt+"','"+str(source_fk[0][0])+"','"+str(destination_fk[0][0])+"','"+str(asset_fk[0][0])+"');")
        conn.commit()
        cur.execute("SELECT request_pk from requests WHERE requester_fk='"+str(requester_fk[0][0])+"' AND assset_fk='"+str(asset_fk[0][0])+"' AND request_data='"+request_dt+"' AND approval_data='"+approve_dt+"';")
        request_pk = cur.fetchall()
        cur.execute("INSERT INTO transit (request_fk, load_time, unload_time) VALUES ('"+str(request_pk[0][0])+"','"+load_dt+"','"+unload_dt+"');")
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
