#pripojeni_db():

#vytvoreni_tabulky()

#hlavni_menu()

import mysql.connector


DB_NAME = "manager_library"
PASSWORD = "19791979"


def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = PASSWORD
            )
        cursor = conn.cursor()
        create_database(cursor, DB_NAME)
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = PASSWORD,
            database = DB_NAME
            )
        print(f"Připojeno k databázi {DB_NAME}.")
        return conn

    except mysql.connector.Error as err:
        print (f"Chyba při připojování: {err}.")
        return None

    

def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev VARCHAR(100) NOT NULL,
                Popis VARCHAR (255) NOT NULL,
                Stav VARCHAR (20) DEFAULT 'Nezahájeno',
                Datum_vytvoreni DATE DEFAULT (CURDATE()));""")
        
        conn.commit()
    finally:
        cursor.close()


def digit_check(digit_nr):
    """funkce kontroluje, zda je vstup číslo a převádí jej na integer"""
    if digit_nr.isdigit():
        digit_intg = int(digit_nr)
        return digit_intg
    else:
        return print("Zadaná hodnota musí být číslo.")
    

def pridat_ukol(conn, task_name, task_cont):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ukoly (Nazev, Popis) 
            VALUES (%s, %s)""",(task_name, task_cont)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}.")
    finally:
        cursor.close()


def zobrazit_ukoly(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ukoly")
        seznam = cursor.fetchall()
        
        return seznam

    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    finally:
        cursor.close()


def aktualizovat_ukol(conn, choosen_id, new_state):
    try:
        cursor = conn.cursor()
        cursor.execute ("""UPDATE ukoly
                        SET Stav = (%s)
                        WHERE ID = (%s);""",
                        (new_state, choosen_id))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    finally:
        cursor.close()


def odstranit_ukol(conn,id_to_delete):
    try: 
        cursor = conn.cursor()
        cursor.execute ("""DELETE FROM ukoly
                        WHERE ID = (%s);""",(id_to_delete,)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    finally:
        cursor.close()


def seznam_id(conn):
    try:
        cursor = conn.cursor()
        cursor.execute ("SELECT ID FROM ukoly;")
        id_seznam = cursor.fetchall()
        id_seznam_nr = []
        for nr in id_seznam:
            id_seznam_nr.append(nr[0])
        
        return id_seznam_nr
    
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    finally:
        cursor.close()
        

def main():
    
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        create_table(conn)

        while True:
            print("Správce úkolů - Hlavní menu\n")
            print("1. Přidat úkol")
            print("2. Zobrazit úkoly")
            print("3. Aktualizovat úkol")
            print("4. Odstranit úkol")
            print("5. Ukončit program")
           
           
            while True:
                    choice_number = input("Vyberte možnost (1-5):")
                    choice_nr_checked = digit_check(choice_number)
                
                    if choice_nr_checked not in range(1,6):
                        print("Zadané číslo musí být v rozsahu 1-5")
                    else:
                        break

                
            if choice_nr_checked == 1:
                while True:
                    task_name = input("Zadejte název úkolu:")
                    task_cont = input("Zadejte popis úkolu:")
                    if not task_name or not task_cont:
                        print("Název úkolu i jeho popis musí být vyplněny.")
                    else:
                        pridat_ukol(conn,task_name, task_cont)
                        print(f"Úkol {task_name} byl úspěšně zadán.")
                        break

            
            elif choice_nr_checked == 2:
                seznam = zobrazit_ukoly(conn)
                if not seznam:
                    print("žádný úkol není zadán\n")
                else:    
                    for line in seznam:
                        print(
                    f"{line[0]}. {line[1]} - {line[2]} - {line[3]} - {line[4]}"
                    )

            
            elif choice_nr_checked == 3:
                seznam = zobrazit_ukoly(conn)
                if not seznam:
                    print("žádný úkol není zadán\n")
                else:    
                    for line in seznam:
                        print(f"{line[0]}. {line[1]} - {line[3]}")
                    
                    while True:
                        choosen_id = input(
                            "Zadejte číslo úkolu," \
                            " u kterého chcete změnit stav.")
                        
                        choosen_id_checked = digit_check(choosen_id)
                        id_seznam = seznam_id(conn)
                        if choosen_id_checked not in id_seznam:
                            print("Zadanému číslu neodpovídá žádný úkol.")
                        else:
                            new_state = input(
                                "Zadejte nový stav 'Probíhá' nebo 'Hotovo':")
                            aktualizovat_ukol(
                                conn,choosen_id,new_state)
                            print("Úkol byl úspěšně aktualizován.")
                            break

            elif choice_nr_checked == 4:
                seznam = zobrazit_ukoly(conn)
                if not seznam:
                    print("žádný úkol není zadán\n")
                else:    
                    for line in seznam:
                        print(
                    f"{line[0]}. {line[1]} - {line[2]} - {line[3]} - {line[4]}"
                    )
                    
                    while True:
                        id_to_delete = input(
                            "Zadejte číslo úkolu," \
                            " který chcete trvale odstranit.")
                        
                        id_to_delete_checked = digit_check(id_to_delete)
                        id_seznam = seznam_id(conn)
                        if id_to_delete_checked not in id_seznam:
                            print("Zadanému číslu neodpovídá žádný úkol.")
                        else:
                            odstranit_ukol(
                                conn,id_to_delete_checked)
                            print("Úkol byl úspěšně odstraněn.")
                            break


            else:
                print("Program je ukončen.")
                break

    else:
        print("Nelze se připojit k databázi.")

if __name__ == "__main__":
    main()