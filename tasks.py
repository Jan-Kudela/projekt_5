import mysql.connector

def pridat_ukol(conn):
    while True:
        task_name = input("Zadejte název úkolu:")
        task_cont = input("Zadejte popis úkolu:")
        if not task_name or not task_cont:
            print("Název úkolu i jeho popis musí být vyplněny.")
        else:
            pridat_ukol_db(conn,task_name, task_cont)
            print(f"Úkol {task_name} byl úspěšně zadán.")
            break


def pridat_ukol_db(conn, task_name, task_cont):
    """přidá do databáze úkol, zadává se název a popis úkolu."""
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


def zalomeni_radku_ukolu(seznam):
    for line in seznam:
        print(f"{line[0]}. {line[1]} - {line[2]} - {line[3]} - {line[4]}")


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


def zobrazit_ukoly(conn):
    seznam = zobrazit_ukoly_db(conn)
    if not seznam:
        print("žádný úkol není zadán\n")
    else:    
        zalomeni_radku_ukolu(seznam)
        while True:
            filtr = input(
                "Vyfiltrovat nezahájené úkoly (zadejte 'n') nebo "
                "probíhající (zadejte'p')? Zpět ('z')"
            )
            if filtr == "n":
                seznam_n = filtr_stavu(conn, "Nezahájeno")
                zalomeni_radku_ukolu(seznam_n)
                if not seznam_n:
                    print("Žádné nezahájené úkoly.")
            elif filtr == "p":
                seznam_p = filtr_stavu(conn, "Probíhá")
                zalomeni_radku_ukolu(seznam_p)
                if not seznam_p:
                    print("Žádné probíhající úkoly.")

            elif filtr == "z":
                break
            else:
                print("Vyberte ze zadaných možností n, p, z.")


def zobrazit_ukoly_db(conn):
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


def kontrola_integeru(digit_nr):
    """funkce kontroluje, zda je vstup číslo a převádí jej na integer"""
    if digit_nr.isdigit():
        digit_intg = int(digit_nr)
        return digit_intg
    else:
        return None
    

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


stavy = ["probíhá", "hotovo"]
def kontrola_stavu(stav):
    while True: 
        if stav in stavy:
            return stav
        else: 
            print("Zadaný stav neexistuje nebo je napsán chybně.")
            stav = input("Zadejte stav znova - probíhá / hotovo: ")


def aktualizovat_ukol(conn):
    seznam = zobrazit_ukoly_db(conn)
    if not seznam:
        print("žádný úkol není zadán\n")
    else:    
        for line in seznam:
            print(f"{line[0]}. {line[1]} - {line[3]}")
        
        while True:
            choosen_id = input(
                "Zadejte číslo úkolu," \
                " u kterého chcete změnit stav.")
            
            choosen_id_checked = kontrola_integeru(choosen_id)
            id_seznam = seznam_id(conn)
            if choosen_id_checked not in id_seznam:
                print("Zadanému číslu neodpovídá žádný úkol.")
            else:
                break
        
        new_state = input("Zadejte nový stav 'probíhá' nebo 'hotovo':")
        stav_ok = kontrola_stavu(new_state)
        aktualizovat_ukol_db(conn,choosen_id_checked,stav_ok)
        print("Úkol byl úspěšně aktualizován.")


def aktualizovat_ukol_db(conn, choosen_id, new_state):
    """aktualizuje stav úkolu podle zvoleného ID"""
    try:
        cursor = conn.cursor()
        cursor.execute ("""UPDATE ukoly
                        SET Stav = (%s)
                        WHERE ID = (%s);""",
                        (new_state, choosen_id))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}.")
        raise
    finally:
        cursor.close()


def odstranit_ukol(conn):
    seznam = zobrazit_ukoly_db(conn)
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
            
            id_to_delete_checked = kontrola_integeru(id_to_delete)
            id_seznam = seznam_id(conn)
            if id_to_delete_checked not in id_seznam:
                print("Zadanému číslu neodpovídá žádný úkol.")
            else:
                odstranit_ukol_db(
                    conn,id_to_delete_checked)
                print("Úkol byl úspěšně odstraněn.")
                break


def odstranit_ukol_db(conn,id_to_delete):
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