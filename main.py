import os
from config import CSV_DIRECTORY, WELCOME_DIRECTORY
from user_operations import create_user, edit_user, delete_user, show_users, display_guidance
from csv_operations import save_to_csv, load_from_csv 
from directory_operations import ensure_directory_exists


# Global Constants
FILENAME = "users.csv"
CSV_DIRECTORY = r"C:\Users\micha\Desktop\Skole\Eksamensprojekt\Tilføj_bruger_program\Bruger_profiler"
WELCOME_DIRECTORY = r"C:\Users\micha\Desktop\Skole\Eksamensprojekt\Tilføj_bruger_program\Velkomst"

def display_header():
    print("\n" + "=" * 30)
    print("  BRUGER OPRETTELSES SYSTEM  ")
    print("=" * 30)

def display_section_header(title):
    console_width = 80 
    title_length = len(title)
    padding = (console_width - title_length) // 2
    print("\n" + "-" * console_width)
    print(" " * padding + title)
    print("-" * console_width)
    
def print_separator():
    print("\n" + "-" * 80) 
    
def get_user_input(prompt):
    return input(f"     {prompt}:  ")

def display_error(message):
    print(f"Fejl: {message}")

def confirm_action(prompt):
    return get_user_input(f"{prompt} (ja/nej)").lower() == 'ja'

def display_menu():
    display_header()
    print("\nHovedmenu:")
    print("1. Opret Bruger")
    print("2. Vis Brugere")
    print("3. Rediger Bruger")
    print("4. Slet Bruger")
    print("5. Vis Vejledning")
    print("6. Gem og Afslut")
    print("7. Afslut uden at Gemme")
    print("=" * 30)

def main():
    ensure_directory_exists(CSV_DIRECTORY)
    ensure_directory_exists(WELCOME_DIRECTORY)
    users = load_from_csv(CSV_DIRECTORY, FILENAME)

    while True:
        display_menu()
        choice = get_user_input("Indtast dit valg")

        if choice == '1':
            display_section_header("Opret Bruger")
            create_user(users, CSV_DIRECTORY, WELCOME_DIRECTORY)
            print_separator()
        elif choice == '2':
            display_section_header("Vis Brugere")
            show_users(users)
            print_separator()
        elif choice == '3':
            display_section_header("Rediger Bruger")
            edit_user(users, CSV_DIRECTORY, WELCOME_DIRECTORY)
            print_separator()
        elif choice == '4':
            display_section_header("Slet Bruger")
            delete_user(users, CSV_DIRECTORY, WELCOME_DIRECTORY)
            print_separator()
        elif choice == '5':
            display_section_header("Vejledning")
            display_guidance()
            print_separator()
        elif choice == '6':
            if confirm_action("Gem og afslut"):
                save_to_csv(users, CSV_DIRECTORY, FILENAME)
                print("Data er gemt. Afslutter programmet.")
                print_separator()
                break
        elif choice == '7':
            if confirm_action("Afslut uden at gemme"):
                print("Afslutter programmet uden at gemme ændringer.")
                print_separator()
                break
        else:
            display_error("Ugyldigt valg. Vælg venligst en gyldig mulighed.")
            print_separator()

if __name__ == "__main__":
    main()
