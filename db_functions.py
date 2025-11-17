import mysql.connector

USER = "root"
HOST = "localhost"
DB_NAME = "manager_library"
PASSWORD = "19791979"

def create_database(cursor, db_name):
    """vytvoří databázi, pokud již neexistuje"""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")


def connect_to_db():
    """vytvoří připojení k mysql a vytvoří databázi"""
    try:
        conn = mysql.connector.connect(
            host = HOST,
            user = USER,
            password = PASSWORD
            )
        cursor = conn.cursor()
        create_database(cursor, DB_NAME)
        cursor.execute(f"USE {DB_NAME};")
        print(f"Připojeno k databázi {DB_NAME}.")
        return conn

    except mysql.connector.Error as err:
        print (f"Chyba při připojování: {err}.")
        return None


def create_table(conn):
    """vytvoří tabulku 'ukoly' se sloupci ID, Nazev, Popis, Stav,
    a datum"""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev VARCHAR(100) NOT NULL,
                Popis VARCHAR (255) NOT NULL,
                Stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                Datum_vytvoreni DATE DEFAULT (CURDATE())
            );"""
        )
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}.")
        raise
    finally:
        cursor.close()


