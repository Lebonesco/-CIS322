import os
import csv 

def main():
    fileDirectory = os.path.dirname(os.path.abspath(__file__)) + "/osnap_legacy"
    files = load(fileDirectory)
    for file in files:
        try:
             if "inventory" in file.name:
                inventory(file)
                print("*****************************************")
        except Exception(e):
            print("Error: " + e)

def inventory(file):
    file = csv.reader(file)
    header = next(file)
    for line in file:
        row = line.split()
        print("INSERT INTO products (product_pk, description) VALUES ({}, {});".format(row[1], row[1]))
        print("INSERT INTO assets (product_fk, asset_tag) VALUES ({}, {});".format(row[1], row[0]))
    
def load(fileDirectory):
    files = []
    for filename in os.listdir(fileDirectory):
        files.append(open(fileDirectory + "/" + filename, "r"))
    return files

if __name__ == '__main__':
    main()
