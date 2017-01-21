import os
import csv 
import psycopg2
import random

db_name = "test_user"
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
                inventory(lines)
                print("*****************************************")
            elif "product_list" in file.name:
                product_list(lines)
            elif "transit" in file.name:
                transit(lines)
        except Exception as e:
            print("Error: " + str(e))

def transit(lines):
    header = next(lines)
    for row in lines:
        print(cursor.execute("SELECT asset_tag FROM assets WHERE asset_pk=3;"))
        if(cursor.execute("SELECT count(1) FROM facilities WHERE common_name="+"'"+row[1]+"'"+";") == 0):
            print("testing")
            insert("facilities", ["common_name", "depart_dt"], [row[1], row[3]])
        
        if(cursor.execute("SELECT count(1) FROM facilities WHERE common_name="+"'"+row[2]+"'"+";") == 0):
            insert("facilities", ["common_name", "arrive_at"], [row[2], row[4]])
            print("testign2")
        if(cursor.execute("SELECT count(1) FROM assets WHERE asset_tag="+"'"+row[0]+"'"+";") == 0):
            insert("assets", ["asset_tag", "description"], [row[0], row[6]])
            print("testing3")
        asset_fk = cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag="+"'"+row[0]+"'"+";")
        facility_fk1 = cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[1]+"'" +";")
        facility_fk2 = cursor.execute("SELECT facility_pk FROM facilities WHERE common_name="+"'"+row[2]+"'"+";")
        
        print(asset_fk)
        insert("asset_at", ["asset_fk", "facility_fk", "depart_dt"], [asset_fk, facility_fk2, row[4]])
        insert("asset_at", ["asset_fk", "facility_fk", "arrive_dt"], [asset_fk, facility_fk1, row[3]]) 

def inventory(lines):
    header = next(lines)
    for row in lines:
        insert("products", ["description"], [row[1]])
        insert("assets", ["asset_tag"], [row[0]])

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
