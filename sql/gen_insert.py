import os
import csv 
import psycopg2
import random
import sys

cursor = None
conn = None

def main(db_name, port):
    connect(db_name, port)
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
                pass
                #transit(lines)
        except Exception as e:
            print("Error: " + str(e))




    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['MB 005', 'Headquarters', '1/4/2017', '1/7/2017'])
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Site 300', 'Headquarters', '1/8/2017', '1/8/2017'])
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Groom Lake', 'Headquarters', '1/8/2017', '1/8/2017'])
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Los Alamos, NM', 'Headquarters', 'NULL', 'NULL'])

    cursor.execute("SELECT convoy_pk FROM convoys WHERE dest_fk='MB 005' AND source_fk='Headquarters';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA154672';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk, convoy_pk])

        
    cursor.execute("SELECT convoy_pk FROM convoys WHERE dest_fk='Site 300' AND source_fk='Headquarters';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA154672';")
    asset_pk = cursor.fetchone
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk, convoy_pk])




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

def connect(db_name, port):
    global cursor
    global conn
    connection = "host='localhost' port='" + str(port) + "' dbname='" + db_name + "' user='osnapdev' password='secret'"

    conn = psycopg2.connect(connection)
    cursor = conn.cursor()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("missing arguments. Try again.")
    else:
        main(sys.argv[1], sys.argv[2])
