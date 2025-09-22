#pripojeni_db():

#vytvoreni_tabulky()

#hlavni_menu()

import mysql.connector

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

    
   

def main():

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        
 


if __name__ == "__main__":
    main()