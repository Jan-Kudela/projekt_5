import mysql.connector
from db_functions import connect_to_db, create_table
from tasks import (
    pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, 
    odstranit_ukol, kontrola_integeru
)


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
                choice_nr_checked = kontrola_integeru(choice_number)
            
                if choice_nr_checked not in range(1,6):
                    print("Zadané číslo musí být v rozsahu 1-5")
                else:
                    break
                
            if choice_nr_checked == 1:
                pridat_ukol(conn)
                
            elif choice_nr_checked == 2:
                zobrazit_ukoly(conn)
                            
            elif choice_nr_checked == 3:
                aktualizovat_ukol(conn)

            elif choice_nr_checked == 4:
                odstranit_ukol(conn)

            else:
                print("Program je ukončen.")
                conn.close()
                break

    else:
        print("Nelze se připojit k databázi.")

if __name__ == "__main__":
    main()