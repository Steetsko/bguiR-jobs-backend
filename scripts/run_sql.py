import psycopg2, sys, pathlib
sql = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
conn = psycopg2.connect(dbname="bsuir", user="postgres", password="111", host="localhost", port=5432)
conn.autocommit = True
with conn, conn.cursor() as cur: cur.execute(sql)
print("Seed applied OK") #
