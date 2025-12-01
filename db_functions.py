import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()

host_env = os.getenv("HOST")
user_env = os.getenv("USER")
password_env = os.getenv("PASSWORD")
db_name_env = os.getenv("DB_NAME")


def create_database(cursor, db_name):
    """vytvoří databázi, pokud již neexistuje"""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")


def connect_to_db():
    """vytvoří připojení k mysql a vytvoří databázi"""
    try:
        conn = mysql.connector.connect(
            host = host_env,
            user = user_env,
            password = password_env
            )
        cursor = conn.cursor()
        create_database(cursor, db_name_env)
        cursor.execute(f"USE {db_name_env};")
        print(f"Připojeno k databázi {db_name_env}.")
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


