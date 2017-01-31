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
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Site 300', 'National City', '1/8/2017', '1/8/2017'])
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Groom Lake', 'Sparks, NV', '1/8/2017', '1/8/2017'])
    insert("convoys", ['source_fk', 'dest_fk', 'depart_dt', 'arrive_dt'],['Los Alamos', 'Washington', '1/1/1980', '1/1/2030'])

    cursor.execute("SELECT convoy_pk FROM convoys WHERE source_fk='MB 005' AND dest_fk='Headquarters';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467287';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467287'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467287';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])
    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='';")

       

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467288';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467288'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467288';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467289';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467289'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467289';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])
    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467290';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467290'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467290';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])
    
    
    cursor.execute("SELECT convoy_pk FROM convoys WHERE source_fk='Site 300' AND dest_fk='National City';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467291';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467291'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467291';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467292';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467292'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467292';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467293';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467293'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467293';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467294';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467294'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467294';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT convoy_pk FROM convoys WHERE source_fk='Groom Lake' AND dest_fk='Sparks, NV';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467295';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467295'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467295';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT  FROM assets WHERE asset_tag='CA15467296';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['CA15467296'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='CA15467296';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])

    cursor.execute("SELECT convoy_pk FROM convoys WHERE source_fk='Los Alamos' AND dest_fk='Washington';")
    convoy_pk = cursor.fetchone()
    cursor.execute("SELECT  FROM assets WHERE asset_tag='DC15467299';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['DC15467299'])

    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='DC15467299';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])


    cursor.execute("SELECT  FROM assets WHERE asset_tag='DC25467300';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['DC25467300'])


    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='DC25467300';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])
    cursor.execute("SELECT  FROM assets WHERE asset_tag='DC25467301';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['DC25467301'])


    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='DC25467301';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])
    cursor.execute("SELECT  FROM assets WHERE asset_tag='DC25467302';")
    if cursor.fetchone() == None:
        insert("assets", ["asset_tag"], ['DC25467302'])


    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag='DC25467302';")
    asset_pk = cursor.fetchone()
    insert("asset_on", ['asset_fk', 'convoy_fk'], [asset_pk[0], convoy_pk[0]])




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
