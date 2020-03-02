from flask import Flask, render_template, request
import psycopg2
import time
from datetime import date,timedelta

#pomysł mam taki, żeby najpierw sobie zrobić listy z wszystkimi rzeczmi z bazy
#następnie przechowywać je w listach i na nich sprawdzać czy użytkownik może
#zrobić akcję, wykonać ją i dokonać zmiany w bazie danych i updatnąć wszystko
#Poszedłbym tą drogą, ponieważ polecenie "SELECT * FROM coś tam" niestety zwraca none i za bardzo nie wiem jak 
#to inaczej ominąć :/

# Dla localhosta wszystko pięknie działa i tak samo dla serwerów własnych, a z plutonem coś nie chce działać
# Dane potrzbne do wejścia do bazy danych
db_name = "biblio2"
db_user = "postgres"
db_pass = "haselko"    # pytanie czy to nie jest przypadkiem hasło do bazy danych, a nie do samego konta na plutonie
db_host = "localhost"
db_port = "5432"

# Łączenie się z bazą danych 
try:
    conn = psycopg2.connect(database = db_name, user = db_user, password = db_pass, host = db_host, port = db_port)
    conn.autocommit = True
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

#login data:
log_b_id = []
log_title = []
log_us_id = []

#generowanie strony po wpisaniu szukanego tytułu
@app.route('/submit', methods=['POST'])
def submit():
    bid = []
    cid = []
    name = []
    aid = []
    rok = []
    order = [] # czy wypozyczona xd
    state = "Wypożycz" # czy wypozyczona ( unavailable) lub wolna (available), defaultowo not_defined

    if request.method == 'POST':
        search = request.form['title']
        if search == '':
            return render_template('page.html', message='Aby znaleźć książkę wpisz tytuł :)')
        #  TU JEST PROBLEM, BO WYPISUJE NONE ZAMIAST TYTUŁU WIĘC NIC NAM NIE ZNAJDZIE NIESTETY
        #if cur.execute("SELECT * FROM categories") == title: ???
        #to z listami by działało, ale z zapytaniem jak na razie nie

        cur.execute( "Select id_ksiazki from wypozyczenia;" )
        orders = cur.fetchall()
        for data in orders:
            order.append(data[0])
            print("takie numery sa wypozyczone: ")
            print(order)



        if search.lower() in titles:
            print("Znalazłem pozycję w bazie danych :D")
            # Te dwie komendy poniżej elegancko działaja, pierwsza ustawia kursor na pasującym wierszu
            # Następnie fetchall wyciąga wynik z zapytania selecta, czyli wiersze na które kursor wskazał
            cur.execute( "SELECT * FROM ksiazki WHERE tytul ~* " + "'" + search + "'" )
            results = cur.fetchall()
            for data in results:
                bid.append(data[0])
                log_b_id.append(data[0])
                print(log_b_id)
                print("logowanie ksiazka id: " + str(log_b_id[-1]))
                cid.append(data[1])
                name.append(data[2])
                log_title.append(data[2])
                print("logowanie tytul : " + str(log_title[-1]))
                aid.append(data[3])
                rok.append(data[4])
            
            for var in range(len(order)):
                print("moj for :")
                print(var,order[var])
                if order[var] ==  bid[0]:
                    state = "Już wypożyczona"
                
                

            cur.execute( "SELECT * FROM kategorie WHERE id_kategorii = " + str(cid[0]) )
            nazwa_kategorii = cur.fetchall()[0][1]
            cur.execute( "SELECT * FROM autorzy WHERE id_autora = " + str(aid[0]) )
            godnosc_autora = cur.fetchall()
            return render_template( 'new_redirect.html', id = bid[0], kategoria = nazwa_kategorii, tytul = name[0], rok = rok[0], autor = godnosc_autora[0][1] + " " + godnosc_autora[0][2], state = state)
        print(autorzy_nazwisko)


        if search.lower() in autorzy_nazwisko:
            print("Znalazłem pozycję w bazie danych :D")
            # Te dwie komendy poniżej elegancko działaja, pierwsza ustawia kursor na pasującym wierszu
            # Następnie fetchall wyciąga wynik z zapytania selecta, czyli wiersze na które kursor wskazał
            cur.execute( "SELECT * FROM ksiazki k, autorzy a WHERE k.id_autora = a.id_autora and nazwisko ~* " + "'" + search + "'" )
            results = cur.fetchall()
            for data in results:
                bid.append(data[0])
                log_b_id.append(data[0])
                print("logowanie ksiazka id: " + str(log_b_id[-1]))
                cid.append(data[1])
                name.append(data[2])
                log_title.append(data[2])
                print("logowanie tytul : " + str(log_title[-1]))
                aid.append(data[3])
                rok.append(data[4])
            
            for var in range(len(order)):
                print("moj for :")
                print(var,order[var])
                if order[var] ==  bid[0]:
                    state = "Już wypożyczona"
            

            cur.execute( "SELECT * FROM kategorie WHERE id_kategorii = " + str(cid[0]) )
            nazwa_kategorii = cur.fetchall()[0][1]
            cur.execute( "SELECT * FROM autorzy WHERE id_autora = " + str(aid[0]) )
            godnosc_autora = cur.fetchall()
            return render_template( 'new_redirect.html', id = bid[0], kategoria = nazwa_kategorii, tytul = name[0], rok = rok[0], autor = godnosc_autora[0][1] + " " + godnosc_autora[0][2], state = state)

        else:
            print("Nic ni ma, czarna dziura po prostu :P")
            return render_template('mistake.html', tytul="Nie posiadamy takiej pozycji w naszej bibliotece :/")
        # na wyświetleniu redirect trzeba by zwrócić tą książkę plus przycik "Wypożycz", a po kliknięciu pop-up z wpisaniem swoich danych czytelnika :D

@app.route('/login', methods=['POST'])
def login():
    # To do validate users :D

    book_id = []
    name_user = []
    secound_name = []


    if request.method == 'POST':
        us_id = request.form['id']
        us_name = request.form['us_name']
        us_sname = request.form['us_sname']

        print(us_sname)
        print("dziala hehehehhehehehahsda xDDD111111111")

        cur.execute( "SELECT * FROM czytelnicy where id_czytelnika = " +str(us_id) + " and imie~*" + "'" + str(us_name) + "' and nazwisko~*" + "'" + str(us_sname) + "';")    
        authorizedUser = cur.fetchall() #default fetchall[0][variable]

        #print("id urzytkownika toooo ")
        if(authorizedUser != []):
            
            if authorizedUser[0][1] == us_name:
                print("jest taki ktos")
                log_us_id.append(us_id)
                print("loggowanie user id : " + str(log_us_id[-1]))
                btaken = 0
                cur.execute( "SELECT * FROM wypozyczenia" )
                taken = cur.fetchall()
                #inicjalizuje date dzisiejsza i oddania (domyslnie na za 2 tyg ;) )
                today = date.today()
                giving_back = timedelta(days=14) + today

                if(taken != []):
                    indicator = 0
                    for data in taken:
                        book_id.append(data[2])
                        if log_b_id[-1] == (book_id[indicator]):
                            btaken += 1
                        indicator += 1    
                    if btaken > 0:
                        ### zawsze tu wchodzi ..............................
                       
                        #cur.execute("INSERT INTO wypozyczenia (id_czytelnika,id_ksiazki, tytul,data_wypozyczenia,data_oddania) values('" + str(log_us_id[0]) + "'," + "'" + str(log_b_id[0]) + "'," + "'" + str(log_title[0]) + "'," +  "'2020-02-11','2020-03-12');")
                        return render_template('mistake.html', tytul="Ta ksiazka jest juz wypozyczona, wybierz inna1")
                    else:
                        cur.execute("INSERT INTO wypozyczenia (id_czytelnika,id_ksiazki, tytul,data_wypozyczenia,data_oddania) values('" + str(log_us_id[-1]) + "'," + "'" + str(log_b_id[-1]) + "'," + "'" + str(log_title[-1]) + "'," +  "'" + str(today) + "','" + str(giving_back) + "')" )
                        #INSERT INTO wypozyczenia (id_czytelnika,id_ksiazki, tytul,data_wypozyczenia,data_oddania) values('1','1','Teoria Sygnalow','2020-02-11','2020-03-12');
                        print("sukces po prostu")
                        return render_template('success.html')
                else:
                    cur.execute("INSERT INTO wypozyczenia (id_czytelnika, id_ksiazki, tytul, data_wypozyczenia, data_oddania) values ('" + str(log_us_id[-1]) + "'," + "'" + str(log_b_id[-1]) + "'," + "'" + str(log_title[-1]) + "'," +  "'" + str(today) + "','" + str(giving_back) + "')")
                    print("sukces bo pusta")
                    return render_template('success.html')
            else:
                print("nie ma kogos takiego ")
                return render_template('mistake.html', tytul="Nie ma takiego użytkownika biblioteki")

        else:
            print("na pewno nie ma kogos takiego ! ")
            return render_template('mistake.html', tytul="Nie ma takiego użytkownika biblioteki")            
      
    print("dziala hehehehhehehehahsda xDDD22222222")

    return render_template('success.html')

@app.route('/worker', methods=['POST'])
def worker():
    return render_template('worker.html')

@app.route('/added', methods=['POST'])
def added():
    dodano = False
    if request.method == 'POST':
        addNewKategoria = request.form['addNewKategoria']
        addNewImie = request.form['addNewImie']
        addNewNazwisko = request.form['addNewNazwisko']
        addNewIdKategorii = request.form['addNewIdKategorii']
        addNewTitle = request.form['addNewTitle']
        addNewIdAutora = request.form['addNewIdAutora']
        addNewRok = request.form['addNewRok']
        addNewImieCzytelnika = request.form['addNewImieCzytelnika']
        addNewNazwiskoCzytelnika = request.form['addNewNazwiskoCzytelnika']
        addNewPESEL = request.form['addNewPESEL']
        addNewDataUrodzenia = request.form['addNewDataUrodzenia']
        
        # Dodanie nowej kategorii
        if addNewKategoria != '':
            try:
                cur.execute("INSERT INTO kategorie (nazwa) VALUES ('" + addNewKategoria + "');")
                dodano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się dodać nowej kategorii, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Dodanie nowego autora
        if addNewImie != '' and addNewNazwisko != '':
            try:
                cur.execute("INSERT INTO autorzy (imie, nazwisko) VALUES ('" + addNewImie + "', " +"'" + addNewNazwisko + "');")
                dodano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się dodać nowego autora, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Dodanie nowej książki
        if addNewIdKategorii != '' and addNewTitle != ''  and addNewIdAutora != '' and addNewRok != '':
            try:
                cur.execute("INSERT INTO ksiazki (id_kategorii, tytul, id_autora, rok_wydania) VALUES ('" + addNewIdKategorii + "', '" + addNewTitle + "', '" + addNewIdAutora + "', '" + addNewRok + "');")
                dodano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się dodać nowej książki, upewnij się czy dane zostały wprowadzone poprawnie !")

         # Dodanie nowego czytelnika
        if addNewImieCzytelnika != '' and addNewNazwiskoCzytelnika != '' and addNewPESEL != '' and addNewDataUrodzenia != '':
            try:
                cur.execute("INSERT INTO czytelnicy (imie, nazwisko, pesel, data_urodzenia) VALUES ('" + addNewImieCzytelnika + "', '" + addNewNazwiskoCzytelnika + "', '" + addNewPESEL + "', '" + addNewDataUrodzenia + "');")
                dodano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się dodać nowego czytelnika, upewnij się czy dane zostały wprowadzone poprawnie !")
        if dodano == True:
            return render_template('added.html')
        else:
            return render_template('mistake.html', tytul="Nie udało się dodać nowej pozycji, upewnij się czy dane zostały wprowadzone poprawnie !")

@app.route('/deleted', methods=['POST'])
def deleted():
    usunieto = False
    if request.method == 'POST':
        delNewKategoria = request.form['delNewKategoria']
        delautorzyIdAutora = request.form['delautorzyIdAutora']
        delNewImie = request.form['delNewImie']
        delNewNazwisko = request.form['delNewNazwisko']
        delNewIdKsiazki = request.form['delNewIdKsiazki']
        delNewIdKategorii = request.form['delNewIdKategorii']
        delNewTitle = request.form['delNewTitle']
        delNewIdAutora = request.form['delNewIdAutora']
        delNewRok = request.form['delNewRok']
        delNewImieCzytelnika = request.form['delNewImieCzytelnika']
        delNewNazwiskoCzytelnika = request.form['delNewNazwiskoCzytelnika']
        delNewPESEL = request.form['delNewPESEL']
        delNewDataUrodzenia = request.form['delNewDataUrodzenia']
        
        # Usuwanie danej kategorii
        if delNewKategoria != '':
            try:
                cur.execute("DELETE FROM kategorie where nazwa = '" + delNewKategoria + "';")
                usunieto = True
            except:
                return render_template('mistake.html', tytul="Nie udało się usunąć podanej kategorii, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Usuwanie danego autora
        if delNewImie != '' and delNewNazwisko != '' and delautorzyIdAutora != '':
            try:
                cur.execute("DELETE FROM autorzy WHERE id_autora = '" + delautorzyIdAutora + "' and nazwisko = '" + delNewNazwisko + "';")
                usunieto = True
            except:
                return render_template('mistake.html', tytul="Nie udało się usunąć podanego autora, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Usuwanie danej książki
        if delNewIdKsiazki != '' and delNewIdKategorii != '' and delNewTitle != ''  and delNewIdAutora != '' and delNewRok != '':
            try:
                cur.execute("DELETE FROM ksiazki WHERE id_ksiazki = '" + delNewIdKsiazki + "' and id_kategorii = '" + delNewIdKategorii + "' and tytul = '" + delNewTitle + "' and id_autora = '" + delNewIdAutora + "' and rok_wydania = '" + delNewRok + "';")
                usunieto = True
            except:
                return render_template('mistake.html', tytul="Nie udało się usunąć podanej książki, upewnij się czy dane zostały wprowadzone poprawnie !")

         # Usuwanie danego czytelnika
        if delNewImieCzytelnika != '' and delNewNazwiskoCzytelnika != '' and delNewPESEL != '' and delNewDataUrodzenia != '':
            try:
                cur.execute("DELETE FROM czytelnicy WHERE imie = '" + delNewImieCzytelnika + "' and nazwisko = '" + delNewNazwiskoCzytelnika + "' and pesel = '" + delNewPESEL + "' and data_urodzenia = '" + delNewDataUrodzenia + "';")
                usunieto = True
            except:
                return render_template('mistake.html', tytul="Nie udało się usunąć podanego czytelnika, upewnij się czy dane zostały wprowadzone poprawnie !")
        if usunieto == True:
            return render_template('deleted.html')
        else:
            return render_template('mistake.html', tytul="Nie udało się usunąć podanej pozycji, upewnij się czy dane zostały wprowadzone poprawnie !")

@app.route('/updated', methods=['POST'])
def updated():
    zaktualiowano = False
    if request.method == 'POST':
        # Zczytanie nowych danych do bazy
        updNewKategoria = request.form['updNewKategoria']
        updNewImie = request.form['updNewImie']
        updNewNazwisko = request.form['updNewNazwisko']
        updNewIdKategorii = request.form['updNewIdKategorii']
        updNewTitle = request.form['updNewTitle']
        updNewIdAutora = request.form['updNewIdAutora']
        updNewRok = request.form['updNewRok']
        updNewImieCzytelnika = request.form['updNewImieCzytelnika']
        updNewNazwiskoCzytelnika = request.form['updNewNazwiskoCzytelnika']
        updNewPESEL = request.form['updNewPESEL']
        updNewDataUrodzenia = request.form['updNewDataUrodzenia']

        # Zczytanie danych, które mają być zaktualizowane
        updOldKategoria = request.form['updOldKategoria']
        updOldAutorzyIdAutora = request.form['updOldAutorzyIdAutora']
        updOldNazwisko = request.form['updOldNazwisko']
        updOldIdKsiazki = request.form['updOldIdKsiazki']
        updOldTitle = request.form['updOldTitle']
        updOldIdCzytelnika = request.form['updOldIdCzytelnika']
        updOldNazwiskoCzytelnika = request.form['updOldNazwiskoCzytelnika']
        
        print(updNewKategoria)
        print(updOldKategoria)
        print(updNewIdKategorii)
        print(updNewTitle)
        print(updNewIdAutora)
        print(updNewRok)

        # Update Kategorii
        if updNewKategoria != '' and updOldKategoria != '':
            try:
                cur.execute("UPDATE kategorie SET nazwa = '" + updNewKategoria + "' WHERE nazwa = '" + updOldKategoria + "';")
                zaktualiowano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się zaktualizować podanej kategorii, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Update Autora
        if updNewImie != '' and updNewNazwisko != '' and updOldAutorzyIdAutora != '' and updOldNazwisko != '':
            try:
                cur.execute("UPDATE autorzy SET imie = '" + updNewImie + "', nazwisko = '" + updNewNazwisko + "' WHERE id_autora = '" + updOldAutorzyIdAutora + "' and nazwisko = '" + updOldNazwisko + "';")
                zaktualiowano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się zaktualizować podanego autora, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Update Książki
        if updNewIdKategorii != '' and updNewTitle != '' and updNewIdAutora != '' and updNewRok != '' and updOldIdKsiazki != '' and updOldTitle != '':
            try:
                cur.execute("UPDATE ksiazki SET id_kategorii = '" + updNewIdKategorii + "', tytul = '" + updNewTitle +  "', id_autora = '" + updNewIdAutora + "', rok_wydania = '" + updNewRok + "' WHERE id_ksiazki = '" + updOldIdKsiazki + "' and tytul = '" + updOldTitle + "';")
                zaktualiowano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się zaktualizować podanej ksiazki, upewnij się czy dane zostały wprowadzone poprawnie !")

        # Update Czytelnika
        if updNewImieCzytelnika != '' and updNewNazwiskoCzytelnika != '' and updNewPESEL != '' and updNewDataUrodzenia != '' and updOldIdCzytelnika != '' and updOldNazwiskoCzytelnika != '':
            try:
                cur.execute("UPDATE czytelnicy SET imie = '" + updNewImieCzytelnika + "', nazwisko = '" + updNewNazwiskoCzytelnika +  "', pesel = '" + updNewPESEL + "', data_urodzenia = '" + updNewDataUrodzenia + "' WHERE id_czytelnika = '" + updOldIdCzytelnika + "' and nazwisko = '" + updOldNazwiskoCzytelnika + "';")
                zaktualiowano = True
            except:
                return render_template('mistake.html', tytul="Nie udało się zaktualizować podanego czytelnika, upewnij się czy dane zostały wprowadzone poprawnie !")

    if zaktualiowano == True:
        return render_template('updated.html')
    else:
        return render_template('mistake.html', tytul="Nie udało się zaktualizować podanych pozycji, upewnij się czy dane zostały wprowadzone poprawnie lub czy zostały wpisane wartości we wszystkie pola aktualizacyjne !!!")

@app.route('/deleteOptions', methods=['POST'])
def deleteOptions():
    return render_template('deleteOptions.html')

@app.route('/addOptions', methods=['POST'])
def addOptions():
    return render_template('addOptions.html')

@app.route('/updateOptions', methods=['POST'])
def updateOptions():
    return render_template('updateOptions.html')

# odpalenie serwera
if __name__ == '__main__':
    app.debug = True 
    app.run()