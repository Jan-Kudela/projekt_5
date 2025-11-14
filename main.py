import mysql.connector
from db_functions import create_database, connect_to_db, create_table
from tasks import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol
from other_func import filtr_stavu, digit_check, zalomeni_radku_ukolu, seznam_id


def main():
    
    conn = connect_to_db()
    
    if conn:
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
                    zalomeni_radku_ukolu(seznam)
                    while True:
                        filtr = input(
                            "Vyfiltrovat nezahájené úkoly (zadejte 'n') nebo "
                            "probíhající (zadejte'p')? Zpět ('z')"
                        )
                        if filtr == "n":
                            
                            seznam_n = filtr_stavu(conn, "Nezahájeno")
                            zalomeni_radku_ukolu(seznam_n)
                        elif filtr == "p":
                            
                            seznam_p = filtr_stavu(conn, "Probíhá")
                            zalomeni_radku_ukolu(seznam_p)
                        elif filtr == "z":
                            break
                        else:
                            print("Vyberte ze zadaných možností n, p, z.")
                            
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