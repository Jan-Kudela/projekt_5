import pytest
import mysql.connector
from tasks import pridat_ukol_db, aktualizovat_ukol_db, odstranit_ukol_db
from dotenv import load_dotenv
import os


load_dotenv()

host_env = os.getenv("HOST")
user_env = os.getenv("USER")
password_env = os.getenv("PASSWORD")
db_name_env = os.getenv("DB_NAME")

@pytest.fixture
def connect_to_db():
    """vytvoří připojení k mysql a vytvoří testovací databázi,
       kterou po testech smaže"""
    try:
        conn = mysql.connector.connect(
            host = host_env,
            user = user_env,
            password = password_env
            )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_library;")
        cursor.execute("USE test_library;")
        yield conn

    except mysql.connector.Error as err:
        pytest.fail(f"Chyba při připojování: {err}.")
    
    finally:
        conn.close()
        
        #smazání testovací databáze, v rámci vizuální kontroly
        #v mySQL Workbench lze případně hashtagnout
        conn_clean = mysql.connector.connect(
            host = host_env,
            user = user_env,
            password = password_env
            )
        cursor = conn_clean.cursor()
        cursor.execute("DROP DATABASE IF EXISTS test_library;")
        conn_clean.commit()
        cursor.close()
        conn_clean.close()

    
@pytest.fixture
def create_table(connect_to_db):
    """vytvoří tabulku 'ukoly' se sloupci ID, Nazev, Popis, Stav,
    a datum"""
    cursor = connect_to_db.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev VARCHAR(100) NOT NULL,
                Popis VARCHAR (255) NOT NULL,
                Stav VARCHAR (20) DEFAULT 'Nezahájeno',
                Datum_vytvoreni DATE DEFAULT (CURDATE()));""")
        
        connect_to_db.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    
    yield
    
    # pokud chci vizuálně zkontrolovat zadání úkolu v databázi SQL
    # nutno označit hashtagem níže uvedené dva řádky, které jinak tabulku
    # po provedení testu smažou, tabulku je pak nutné v mySQL Workbench 
    cursor.execute("DROP TABLE IF EXISTS ukoly;")
    connect_to_db.commit()
    cursor.close()


@pytest.fixture
def create_fake_table(connect_to_db):
    "vytvoří tabulku 'fake_table' pouze pro účely testování připojení"
    cursor = connect_to_db.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fake_table (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev VARCHAR(100) NOT NULL,
                Popis VARCHAR (255) NOT NULL,
                Stav VARCHAR (20) DEFAULT 'Nezahájeno',
                Datum_vytvoreni DATE DEFAULT (CURDATE()));""")
        
        connect_to_db.commit()
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
    
    yield

    cursor.execute("DROP TABLE IF EXISTS fake_table;")
    connect_to_db.commit()
    cursor.close()


def test_pridat_ukol_positive(connect_to_db,create_table):
    
    pridat_ukol_db(connect_to_db, "Pes", "Vyvenčit")
    
    cursor = connect_to_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE Nazev = 'Pes';")
    seznam = cursor.fetchall()
    cursor.close()

    assert seznam[0][1] == "Pes"
    assert len(seznam) == 1
        

def test_pridat_ukol_negative(connect_to_db,create_table):
    """testuje, zda se zobrazí chybová hláška při zadání
        prádzné hodnoty 'Nazev' """
    with pytest.raises( mysql.connector.Error):   
        pridat_ukol_db(connect_to_db, None, "Vyvenčit")
    
                
def test_aktualizovat_ukol_positive(connect_to_db,create_table):
    
    pridat_ukol_db(connect_to_db, "Pes", "Vyvenčit")
    aktualizovat_ukol_db(connect_to_db, 1, "Hotovo")

    cursor = connect_to_db.cursor()
    cursor.execute("SELECT * FROM ukoly;")
    seznam = cursor.fetchall()
    cursor.close()

    assert seznam[0][3] == "Hotovo"


def test_aktualizovat_ukol_negative(connect_to_db,create_fake_table):
    """testuje, zda se zobrazí chybová hláška,
      když funkce nenajde zadanou tabulku """
    with pytest.raises( mysql.connector.Error):
        aktualizovat_ukol_db(connect_to_db, 1, "Hotovo")
   

def test_odstranit_ukol_positive(connect_to_db,create_table):
    
    pridat_ukol_db(connect_to_db, "Pes", "Vyvenčit")
    pridat_ukol_db(connect_to_db, "Kočka", "Nakrmit")

    odstranit_ukol_db(connect_to_db, 1)

    cursor = connect_to_db.cursor()
    cursor.execute("SELECT * FROM ukoly;")
    seznam = cursor.fetchall()
    cursor.close()

    assert len(seznam) == 1


def test_odstranit_ukol_negative(connect_to_db,create_table):
    "testuje, zda při smazání neplatného ID zůstane správný počet záznamů"
    pridat_ukol_db(connect_to_db, "Pes", "Vyvenčit")
    pridat_ukol_db(connect_to_db, "Kočka", "Nakrmit")

    odstranit_ukol_db(connect_to_db, 546)

    cursor = connect_to_db.cursor()
    cursor.execute("SELECT * FROM ukoly;")
    seznam = cursor.fetchall()
    cursor.close()

    assert len(seznam) == 2

