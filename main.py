#pripojeni_db():

#vytvoreni_tabulky()

#hlavni_menu()

import mysql.connector
from datetime import date

DB_NAME = "manager_library"
PASSWORD = "19791979"

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = PASSWORD,
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
        print (f"Chyba při připojování: {err}")
        return None

    

def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev VARCHAR(100) NOT NULL,
                Popis VARCHAR (255) NOT NULL,
                Stav VARCHAR (20) NOT NULL,
                Datum vytvoreni DATE);""")
        
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
                choice_number = (input("Vyberte možnost (1-5):"))
                choice_nr_checked = digit_check(choice_number)
            
                if choice_nr_checked not in range(1,5):
                    print("Zadané číslo musí být v rozsahu 1-4")
                else:
                    break

            
            if choice_nr_checked == 1:
                while True:
                    task_name = input("Zadejte název úkolu:")
                    task_cont = input("Zadejte popis úkolu:")
                    if not task_name or not task_cont:
                        print("Název úkolu i jeho popis musí být vyplněny.")
                    else:
                        pridat_ukol(task_name, task_cont)
                        break

            
            elif choice_nr_checked == 2:
                if not ukoly:
                    print("žádný úkol není zadán\n")
                else:    
                    zobrazit_ukoly()

            
            elif choice_nr_checked == 3:
                if not ukoly:
                    print("žádný úkol není zadán\n")
                else:
                    zobrazit_ukoly()
                    while True:
                        number_to_del = input(
                        "Zadejte číslo úkolu, který chcete odstranit: "
                        )
                        nr_checked = digit_check(number_to_del)
                        if nr_checked not in range(1,len(ukoly)+1):
                            print(
                            f"Zadané číslo musí být v rozsahu 1 - {len(ukoly)}."
                            )
                        else:
                            odstranit_ukol(nr_checked)
                            break

            else:
                print("Program je ukončen.")
                break


if __name__ == "__main__":
    main()