import psycopg2

# Dla localhosta wszystko pięknie działa i tak samo dla serwerów własnych, a z plutonem coś nie chce działać
# Dane potrzbne do wejścia do bazy danych
db_name = "finaltest"
db_user = "postgres"
db_pass = "atom13"    # pytanie czy to nie jest przypadkiem hasło do bazy danych, a nie do samego konta na plutonie
db_host = "localhost"
db_port = "5432"

# Łączenie się z bazą danych 
try:
    conn = psycopg2.connect(database = db_name, user = db_user, password = db_pass, host = db_host, port = db_port)

    print("DB connected successfully !!! :D")

except:
    print("DB not connected successfully :( ( Only sad reactions )")

cur = conn.cursor()

# pytanie dlazcego tu taj wypisuje 'none' XD
print(cur.execute("SELECT * FROM categories"))

rows = cur.fetchall()

for data in rows:
    print(" ")
    print("cid: " + str(data[0]))
    print("Name: " + data[1])
    print("cserid: " + str(data[2]))
    print(" ")

cur.execute("INSERT INTO categories (cid, name, cserid) values (15, 'Siemka', '50')")

conn.commit()
print("Results displayed !")