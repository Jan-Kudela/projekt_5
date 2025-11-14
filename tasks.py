import mysql.connector

def pridat_ukol(conn, task_name, task_cont):
    """přidá do tabulky úkol, zadává se název a popis úkolu."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ukoly (Nazev, Popis) 
            VALUES (%s, %s)""",(task_name, task_cont)
        )
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při přidávání úkolu: {err}.")
        raise
    finally:
        cursor.close()


def zobrazit_ukoly(conn):
    """zobrazuje všechny zadané úkoly s tabulky 'ukoly'"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ukoly")
        seznam = cursor.fetchall()
        return seznam

    except mysql.connector.Error as err:
        print(f"Chyba při výpisu úkolů: {err}.")
        raise
    finally:
        cursor.close()


def aktualizovat_ukol(conn, choosen_id, new_state):
    """aktualizuje stav úkolu podle zvoleného ID"""
    try:
        cursor = conn.cursor()
        cursor.execute ("""UPDATE ukoly
                        SET Stav = (%s)
                        WHERE ID = (%s);""",
                        (new_state, choosen_id))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
        raise
    finally:
        cursor.close()


def odstranit_ukol(conn,id_to_delete):
    """smaže vybraný úkol podle zvoleného ID"""
    try: 
        cursor = conn.cursor()
        cursor.execute ("""DELETE FROM ukoly
                        WHERE ID = (%s);""",(id_to_delete,)
        )
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}.")
        raise
    finally:
        cursor.close()