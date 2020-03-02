from flask import Flask, render_template, request
import psycopg2

#pomysł mam taki, żeby najpierw sobie zrobić listy z wszystkimi rzeczmi z bazy
#następnie przechowywać je w listach i na nich sprawdzać czy użytkownik może
#zrobić akcję, wykonać ją i dokonać zmiany w bazie danych i updatnąć wszystko
#Poszedłbym tą drogą, ponieważ polecenie "SELECT * FROM coś tam" niestety zwraca none i za bardzo nie wiem jak 
#to inaczej ominąć :/

# Dla localhosta wszystko pięknie działa i tak samo dla serwerów własnych, a z plutonem coś nie chce działać
# Dane potrzbne do wejścia do bazy danych
db_name = "newOne"
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
print(cur.execute("SELECT * FROM ksiazki"))
# musimy wykonać execute -> select żeby móc wykonać fetchall
rows = cur.fetchall()
books_id = []
cat_id = []
titles = []
authors_id = []
years = []

for data in rows:
    print(" ")
    print("books_id: " + str(data[0]))
    books_id.append(str(data[0]))
    print("categories_id: " + str(data[1]))
    cat_id.append(str(data[1]))
    print("Title: " + data[2].lower())
    titles.append(data[2].lower())
    print("author_id: " + str(data[3]))
    authors_id.append(str(data[3]))
    print("year: " + str(data[4]))
    years.append(str(data[4]))
    print(" ")

#conn.commit()
print("Results displayed !")
print(books_id)

autorzy_aid = []
autorzy_imie = []
autorzy_nazwisko = []

print(cur.execute("SELECT * FROM autorzy"))
autorzy = cur.fetchall()
for data in autorzy:
    autorzy_aid.append(data[0])
    autorzy_imie.append(data[1].lower())
    autorzy_nazwisko.append(data[2].lower())


app = Flask(__name__)

# generowanie strony początkowej biblioteki
@app.route('/')
def page():
    return render_template('page.html')

#generowanie strony po wpisaniu szukanego tytułu
@app.route('/submit', methods=['POST'])
def submit():
    bid = []
    cid = []
    name = []
    aid = []
    rok = []
    if request.method == 'POST':
        search = request.form['title']
        if search == '':
            return render_template('page.html', message='Aby znaleźć książkę wpisz tytuł :)')
        #  TU JEST PROBLEM, BO WYPISUJE NONE ZAMIAST TYTUŁU WIĘC NIC NAM NIE ZNAJDZIE NIESTETY
        #if cur.execute("SELECT * FROM categories") == title: ???
        #to z listami by działało, ale z zapytaniem jak na razie nie
        if search.lower() in titles:
            print("Znalazłem pozycję w bazie danych :D")
            # Te dwie komendy poniżej elegancko działaja, pierwsza ustawia kursor na pasującym wierszu
            # Następnie fetchall wyciąga wynik z zapytania selecta, czyli wiersze na które kursor wskazał
            cur.execute( "SELECT * FROM ksiazki WHERE tytul ~* " + "'" + search + "'" )
            results = cur.fetchall()
            for data in results:
                bid.append(data[0])
                cid.append(data[1])
                name.append(data[2])
                aid.append(data[3])
                rok.append(data[4])
            
            cur.execute( "SELECT * FROM kategorie WHERE id_kategorii = " + str(cid[0]) )
            nazwa_kategorii = cur.fetchall()[0][1]
            cur.execute( "SELECT * FROM autorzy WHERE id_autora = " + str(aid[0]) )
            godnosc_autora = cur.fetchall()
            return render_template( 'new_redirect.html', id = bid[0], kategoria = nazwa_kategorii, tytul = name[0], rok = rok[0], autor = godnosc_autora[0][1] + " " + godnosc_autora[0][2])
        print(autorzy_nazwisko)
        if search.lower() in autorzy_nazwisko:
            print("Znalazłem pozycję w bazie danych :D")
            # Te dwie komendy poniżej elegancko działaja, pierwsza ustawia kursor na pasującym wierszu
            # Następnie fetchall wyciąga wynik z zapytania selecta, czyli wiersze na które kursor wskazał
            cur.execute( "SELECT * FROM ksiazki k, autorzy a WHERE k.id_autora = a.id_autora and nazwisko ~* " + "'" + search + "'" )
            results = cur.fetchall()
            for data in results:
                bid.append(data[0])
                cid.append(data[1])
                name.append(data[2])
                aid.append(data[3])
                rok.append(data[4])
            
            cur.execute( "SELECT * FROM kategorie WHERE id_kategorii = " + str(cid[0]) )
            nazwa_kategorii = cur.fetchall()[0][1]
            cur.execute( "SELECT * FROM autorzy WHERE id_autora = " + str(aid[0]) )
            godnosc_autora = cur.fetchall()
            return render_template( 'new_redirect.html', id = bid[0], kategoria = nazwa_kategorii, tytul = name[0], rok = rok[0], autor = godnosc_autora[0][1] + " " + godnosc_autora[0][2])

        else:
            print("Nic ni ma, czarna dziura po prostu :P")
            return render_template('mistake.html', tytul="Nie posiadamy takiej pozycji w naszej bibliotece :/")
        # na wyświetleniu redirect trzeba by zwrócić tą książkę plus przycik "Wypożycz", a po kliknięciu pop-up z wpisaniem swoich danych czytelnika :D

@app.route('/login', methods=['POST'])
def login():
    # To do validate users :D
    return render_template('success.html')

# odpalenie serwera
if __name__ == '__main__':
    app.debug = True 
    app.run()