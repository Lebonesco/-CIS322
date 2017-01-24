import os
import csv 
import psycopg2
import random

db_name = "lost"
port = 5432
cursor = None
conn = None

def main():
    connect()
    fileDirectory = os.path.dirname(os.path.abspath(__file__)) + "/osnap_legacy"
    files = load(fileDirectory)
    itemLocation = {}
    for file in files:
        try:
            lines = csv.reader(file, delimiter=',')
            if "inventory" in file.name:
                name = file.name[len(fileDirectory) - len(file.name) + 1: -4]
                facility(name)
                inventory(lines, name)
            elif "product_list" in file.name:
                product_list(lines)
            elif "transit" in file.name:
                transit(lines)
        except Exception as e:
            print("Error: " + str(e))

def facility(name):
    insert("facilities", ["fcode"], [name])


def transit(lines):
    global cursor
    header = next(lines)
    for row in lines:
        cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[1]+"'"+";")
        if cursor.fetchone() == None:
            insert("facilities", ["common_name"], [row[1]])
        
        cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[2]+"'"+";")
        if cursor.fetchone() == None:
            insert("facilities", ["common_name"], [row[2]])
        
        cursor.execute("SELECT  FROM assets WHERE asset_tag="+"'"+row[0]+"'"+";")
        if cursor.fetchone() == None:
            insert("assets", ["asset_tag", "description"], [row[0], row[6]])

        cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag="+"'"+row[0]+"'"+";")
        asset_fk = cursor.fetchone()
        cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[1]+"'" +";")
        facility_fk1 = cursor.fetchone()
        cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[2]+"'"+";")
        facility_fk2 = cursor.fetchone()

        insert("asset_at", ["asset_fk", "facility_fk", "depart_dt"], [asset_fk[0], facility_fk2[0], row[4]])
        insert("asset_at", ["asset_fk", "facility_fk", "arrive_dt"], [asset_fk[0], facility_fk1[0], row[3]]) 

def inventory(lines, name):
    global cursor
    header = next(lines)
    for row in lines:
        insert("products", ["description"], [row[1]])
        insert("assets", ["asset_tag"], [row[0]])
        
        cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag="+"'"+row[0]+"'"+ ";")
        asset_fk = cursor.fetchone()
        cursor.execute("SELECT facility_pk FROM facilities WHERE fcode="+"'"+name+"'"+ ";")
        facility_fk = cursor.fetchone()
        insert("asset_at", ["asset_fk", "facility_fk"], [asset_fk[0], facility_fk[0]])


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
    
   # print("INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), valueResult))
    cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), valueResult))
    conn.commit()

def product_list(lines):
    header = next(lines)
    for row in lines:
        insert("products", ["vendor", "description", "alt_description"], [row[4], row[2], row[1]])

def load(fileDirectory):
    files = []
    for filename in os.listdir(fileDirectory):
        files.append(open(fileDirectory + "/" + filename, "r"))
    return files

def connect():
    global cursor
    global conn
    connection = "host='localhost' port='" + str(port) + "' dbname='" + db_name + "' user='osnapdev' password='secret'"

    conn = psycopg2.connect(connection)
    cursor = conn.cursor()

if __name__ == '__main__':
    main()
