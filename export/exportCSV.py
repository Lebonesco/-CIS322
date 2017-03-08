import csv
import psycopg2
import sys

def main():
    TABLE_NAME = sys.argv[1]
    DB_NAME = sys.argv[2]
    PORT = sys.argv[3]
    HOST = sys.argv[4]
    
    conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
    cur = conn.cursor()

    if TABLE_NAME == "transit":
        headers = ["assset_tag", "request_by", "approve_by", "request_dt", "approve_by", "approve_dt", "source", "destination", "load_dt_dt", "unload_dt" ]

        cur.execute("SELECT asset_tag, username, approve_by approval_data, source_fk, destination_fk, load_time, unload_time FROM requests r JOIN transit t ON t.request_fk=r.request_pk JOIN assets a ON r.assset_fk=a.asset_pk JOIN users u ON r.requester_fk=u.user_pk");
        rows = cur.fetchall()
    else:
        cur.execute("SELECT * FROM "+TABLE_NAME)
        rows = cur.fetchall()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='"+TABLE_NAME+"'")
        headers = cur.fetchall()

        headers = list(map(lambda x: x[0], headers))

    with open(TABLE_NAME+".csv", 'w') as file:

        wr = csv.writer(file)
        wr.writerow(headers)
        for i in range(len(rows)):
            wr.writerow(rows[i])
    
    conn.close()

if __name__ == '__main__':
    main()
