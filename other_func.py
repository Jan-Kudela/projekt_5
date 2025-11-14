import mysql.connector

def filtr_stavu(conn,stav):
    """Vrátí pouze úkoly se stavem v parametru 'stav'"""
    try:
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM ukoly WHERE Stav = %s",(stav,)
        )
        seznam = cursor.fetchall()
        return seznam

    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
        raise
    finally:
        cursor.close() 


def digit_check(digit_nr):
    """funkce kontroluje, zda je vstup číslo a převádí jej na integer"""
    if digit_nr.isdigit():
        digit_intg = int(digit_nr)
        return digit_intg
    else:
        return None
    

def zalomeni_radku_ukolu(seznam):
    for line in seznam:
        print(f"{line[0]}. {line[1]} - {line[2]} - {line[3]} - {line[4]}")


def seznam_id(conn):
    """vytváří list aktuálních ID v tabulce"""
    try:
        cursor = conn.cursor()
        cursor.execute ("SELECT ID FROM ukoly;")
        id_seznam = cursor.fetchall()
        id_seznam_nr = []
        for nr in id_seznam:
            id_seznam_nr.append(nr[0])
        
        return id_seznam_nr
    
    except mysql.connector.Error as err:
        print(f"Chyba při načítání ID: {err}.")
        raise
    finally:
        cursor.close()