import csv
import psycopg2
import sys

def main():
    TABLE_NAME = sys.argv[1]
    DB_NAME = sys.argv[2]
    PORT = sys.argv[3]
    HOST = sys.argv[4]
    #print("Argument list: ", str(sys.argv))
    
    conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+TABLE_NAME)
    rows = cur.fetchall()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='"+TABLE_NAME+"'")
    headers = cur.fetchall()
    print("headers: ", headers)
    print("rows: ", rows)
    with open(TABLE_NAME+".csv", 'w') as file:
        wr = csv.writer(file)
        wr.writerow(headers)
        for i in range(len(rows)):
            wr.writerow(rows[i])


    conn.close()






if __name__ == '__main__':
    main()
