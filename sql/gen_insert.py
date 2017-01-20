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
            print(file.name)
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
        pass

def inventory(lines):
    header = next(lines)
    for row in lines:
        product_pk = generatePrimary("product_pk")
        asset_pk = generatePrimary("asset_pk")
        insert("products", ["product_pk", "description"], [product_pk, row[1]])
        insert("assets", ["asset_pk","product_fk", "asset_tag"], [asset_pk, product_pk, row[0]])

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
        product_pk = generatePrimary("product_pk")
        insert("products", ["product_pk", "vendor", "description", "alt_description"], [product_pk, row[4], row[2], row[1]])

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

def generatePrimary(string):
    return random.random()*(10**8)

if __name__ == '__main__':
    main()
