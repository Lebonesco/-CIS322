import os
import csv 
import psycopg2

db_name = "test_user"
port = 5432
cursor = None

def main():
    connect()
    fileDirectory = os.path.dirname(os.path.abspath(__file__)) + "/osnap_legacy"
    files = load(fileDirectory)
    itemLocation = {}
    for file in files:
        try:
            lines = csv.reader(file)
            if "inventory" in file.name:
                inventory(lines)
                print("*****************************************")
            elif "product_list" in file.name:
                product_list(lines)
            elif "transit" in file.name:
                transit(lines)
        except Exception(e):
            print("Error: " + e)

def transit(lines):
    header = next(lines)
    for row in lines:
        pass

def inventory(lines):
    header = next(lines)
    for row in lines:
        product_pk = generatePrimary("product_pk")
        asset_pk = generatePrimary("asset_pk")
        insert("products", ["product_pk", header[1], "description"], [product_pk, row[1], row[1]])
        insert("assets", ["asset_pk", header[1], header[0]], [asset_pk, row[1], row[0]])

def insert(table, keys, values):
    valueResult = ""
    for i in range(len(values)):
        if type(values[i]) == str:
            valueResult += "'" + values[i] +  "'"
        else:
            valueResult += str(values[i])

        if i < len(values) - 2:
            valueResult += ","

            print("INSERT INTO {} ({}) VALUES ({});".format(table, ",".join(keys), valueResult))

def product_list(lines):
    header = next(lines)
    for row in lines:
        insert("products", ["product_pk", "vendor", "description", "alt_description"], [row[0], row[4], row[2], row[1]])

def load(fileDirectory):
    files = []
    for filename in os.listdir(fileDirectory):
        files.append(open(fileDirectory + "/" + filename, "r"))
    return files

def connect():
    global cursor
    connection = "host='localhost' port='" + str(port) + "' dbname='" + db_name + "' user='osnapdev' password='secret'"

    conn = psycopg2.connect(connection)

def generatePrimary(string):
    return abs(hash(string)) % (10**8)

if __name__ == '__main__':
    main()
