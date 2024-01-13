import os
from user import User
from csv_operations import save_to_csv, save_user
from welcome_generator import generate_welcome_text, update_welcome_text
from config import CSV_DIRECTORY, WELCOME_DIRECTORY

FILENAME = "users.csv"

def create_user(users, csv_directory, welcome_directory):
    while True:
        print("For at vende tilbage til hovedmenuen, tast '0'.")

        first_name = input("Indtast Fornavn: ")
        if first_name == "0":
            if return_to_main_menu():
                break  
            else:
                continue
            
        last_name = input("Indtast Efternavn: ")
        if last_name == "0":
            return_to_main_menu()
            break

        domain = get_domain_choice()
        if domain == "0":
            return_to_main_menu()
            break
        domain_extension = get_domain_extension()
        if domain_extension == "0":
            return_to_main_menu()
            break
        
        director = get_director_name()
        if director == "0":
            return_to_main_menu()
            break    

        user = User(first_name, last_name, domain, domain_extension, director)
        user.generate_email()

        print("\nGennemse Indtastet Information:")
        print(f"Fornavn: {user.first_name}")
        print(f"Efternavn: {user.last_name}")
        print(f"Email: {user.email}")
        print(f"Direktør: {user.director}")

        create_another_input = input("Vil du oprette en anden bruger? (ja/nej): ").lower()
        # Gemmer brugeren her
        save_user(users, user, csv_directory, welcome_directory)

        if create_another_input == "ja":
            continue  # Fortsætter til at oprette en ny bruger
        else:
            break 


def get_domain_choice():
    while True:
        domain_choice = input("Vælg domæne ('TheImperium' eller 'Local'): ").lower()
        if domain_choice in ["theimperium", "local"]:
            return domain_choice.title()
        elif domain_choice == "0":
            return "0"
        else:
            print("Ugyldigt domæne. Indtast venligst et gyldigt domæne.")

def get_domain_extension():
    while True:
        domain_extension = input("Indtast domæneudvidelse (f.eks., '.com', '.dk'): ")
        if domain_extension.startswith("."):
            return domain_extension
        elif domain_extension == "0":
            return "0"
        else:
            print("Ugyldig domæneudvidelse. Skal starte med '.'.")

def get_director_name():
    while True:
        director_input = input("Indtast Direktørens Fulde Navn: ")
        if director_input.lower() == "leto atreides":
            return director_input.title()
        elif director_input == "0":
            return "0"
        else:
            print("Ugyldigt direktørens navn. Prøv igen.")
            
def delete_user(users, csv_directory, welcome_directory):
    if not users:
        print("Ingen brugere tilgængelige.")
        return

    while True:
        print("\nBrugerliste:")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.first_name} {user.last_name} - {user.email}")

        print("\nVælg en bruger for at slette:")
        print("Indtast nummeret på brugeren, 'alle' for at slette alle brugere, eller '0' for at gå tilbage.")
        
        user_choice = input("Valg: ")
        if user_choice.lower() == '0':
            return_to_main_menu()
            break
        elif user_choice.lower() == 'alle':
            confirm = input("Er du sikker på, at du vil slette alle brugere? (ja/nej): ").lower()
            if confirm == "ja":
                users.clear()
                print("Alle brugere er blevet slettet.")
                save_to_csv(users, csv_directory, FILENAME)
            else:
                print("Sletning af alle brugere annulleret.")
        else:
            try:
                deleted_user_index = int(user_choice) - 1
                if 0 <= deleted_user_index < len(users):
                    deleted_user = users[deleted_user_index]
                    confirm_user_deletion(users, deleted_user, csv_directory, welcome_directory)
                else:
                    print("Ugyldigt valg. Indtast venligst et gyldigt nummer.")
            except ValueError:
                print("Ugyldig input. Indtast venligst et gyldigt nummer, 'alle', eller '0'.")

def confirm_user_deletion(users, deleted_user, csv_directory, welcome_directory):
    confirm = input(f"Er du sikker på, at du vil slette {deleted_user.first_name} {deleted_user.last_name}? (ja/nej): ").lower()
    if confirm == "ja":
        users.remove(deleted_user)
        welcome_file_path = os.path.join(welcome_directory, f"Velkomst_{deleted_user.email}.txt")
        if os.path.exists(welcome_file_path):
            os.remove(welcome_file_path)
        print(f"Bruger '{deleted_user.first_name} {deleted_user.last_name}' slettet.")
        save_to_csv(users, csv_directory, FILENAME)
    else:
        print("Sletning annulleret.")

def edit_user(users, csv_directory, welcome_directory):
    if not users:
        print("Ingen brugere tilgængelige. Opret venligst en bruger først.")
        return

    print("\nBrugerliste for redigering:")
    for index, user in enumerate(users, start=1):
        print(f"{index}. {user.first_name} {user.last_name}")

    try:
        user_choice = int(input("Vælg en bruger for at redigere eller indtast '0' for at gå tilbage: "))
        if user_choice == 0:
            return
        elif 0 < user_choice <= len(users):
            selected_user = users[user_choice - 1]
            edit_user_details_menu(selected_user, users, csv_directory, welcome_directory)
        else:
            print("Ugyldigt valg. Indtast venligst et gyldigt nummer.")
    except ValueError:
        print("Ugyldig input. Indtast venligst et gyldigt tal.")
        
def show_users(users):
    if not users:
        print("Ingen brugere tilgængelige.")
        return

    while True:
        print("\nBrugerliste:")
        for index, user in enumerate(users, start=1):
            print(f"{index}. {user.first_name} {user.last_name}")

        print("\nVælg en bruger for at se detaljer eller '0' for at gå tilbage.")

        user_choice = input("Brugernummer eller '0' for at afslutte: ")

        if user_choice.lower() == '0':
            break
        else:
            try:
                user_index = int(user_choice) - 1
                if 0 <= user_index < len(users):
                    show_user_details(users[user_index])
                else:
                    print("Ugyldigt valg. Indtast venligst et gyldigt nummer.")
            except ValueError:
                print("Ugyldig input. Indtast venligst et gyldigt tal.")
                
def show_current_user_details(user):
    print("\nNuværende Brugerdetaljer:")
    print(f"Fornavn: {user.first_name}")
    print(f"Efternavn: {user.last_name}")
    print(f"Email: {user.email}")
    print(f"Domæne: {user.domain}")
    print(f"Domæneudvidelse: {user.domain_extension}")
    print(f"Direktør: {user.director}")
    print("-" * 30)

def show_user_details(user):
    print("\nBrugerdetaljer:")
    print(f"Fornavn: {user.first_name}")
    print(f"Efternavn: {user.last_name}")
    print(f"Email: {user.email}")
    print(f"Direktør: {user.director}")

def confirm_and_update_attribute(attribute_name, update_function, user, new_value):
    if confirm_action(f"Er du sikker på at du vil ændre {attribute_name}?"):
        update_function(user, new_value)
        print(f"{attribute_name} opdateret.")
    else:
        print(f"{attribute_name} ikke ændret.")

def edit_user_details_menu(user, users, csv_directory, welcome_directory):
    def update_email_and_welcome(user, new_email, users):
        old_email = user.email
        user.email = new_email

    # Opdater brugerens email i brugerlisten eller datalageret
        for u in users:
            if u.email == old_email:
                u.email = new_email 

    # Opdater velkomstteksten med den nye email
    update_welcome_text(user, welcome_directory, old_email)

    # Hvis du bruger en database, tilføj opdateringslogikken her
        
def edit_user_details_menu(user, users, csv_directory, welcome_directory):
    while True:
        show_current_user_details(user)

        print("Vælg en detalje for at redigere:")
        print("1. Rediger fornavn")
        print("2. Rediger efternavn")
        print("3. Rediger email")
        print("4. Rediger domæne")
        print("5. Rediger domæneudvidelse")
        print("6. Rediger direktør")
        print("7. Gem ændringer")
        print("0. Gå tilbage til hovedmenuen")

        choice = input("Vælg en mulighed: ")

        if choice == '0':
            break
        elif choice == '1':
            new_fornavn = input("Indtast nyt fornavn: ")
            if confirm_action("Er du sikker på at du vil ændre fornavn?"):
                user.first_name = new_fornavn
                recreate_welcome_text(user, welcome_directory)
        elif choice == '2':
            new_efternavn = input("Indtast nyt efternavn: ")
            if confirm_action("Er du sikker på at du vil ændre efternavn?"):
                user.last_name = new_efternavn
                recreate_welcome_text(user, welcome_directory)
        elif choice == '3':
            new_email = input("Indtast ny email: ")
            if confirm_action("Er du sikker på at du vil ændre email?"):
                update_email_and_welcome(user, new_email, users, welcome_directory)
        elif choice == '4':
            new_domain = get_domain_choice()
            if new_domain != "0" and confirm_action("Er du sikker på at du vil ændre domæne?"):
                user.domain = new_domain
                recreate_welcome_text(user, welcome_directory)
        elif choice == '5':
            new_domain_ext = get_domain_extension()
            if new_domain_ext != "0" and confirm_action("Er du sikker på at du vil ændre domæneudvidelse?"):
                # Genopbyg den nye email med den nye domain_extension
                new_email = f"{user.first_name.lower()}.{user.last_name.lower()}@{user.domain.lower()}{new_domain_ext.lower()}"
                # Opdater emailen og domain_extension
                update_email_welcome_domain(user, new_email, new_domain_ext, users, welcome_directory, csv_directory)
                print(f"Email og domæneudvidelse opdateret til: {new_email}, {new_domain_ext}")
        elif choice == '6':
            new_director = get_director_name()
            if new_director != "0" and confirm_action("Er du sikker på at du vil ændre direktør?"):
                user.director = new_director
                recreate_welcome_text(user, welcome_directory)
        elif choice == '7':
            if confirm_action("Er du sikker på at du vil gemme alle ændringer?"):
                save_to_csv(users, csv_directory, FILENAME )
                print("Alle ændringer gemt.")
                break
            else:
                print("Ændringer ikke gemt.")
        else:
            print("Ugyldigt valg. Prøv igen.")

def recreate_welcome_text(user, welcome_directory):
    welcome_text = (
        f"Hej {user.first_name} {user.last_name}\n"
        f"Velkommen til firmaet. Din email er: {user.email}\n"
        f"Din chef er: {user.director}\n"
        f"Med venlig hilsen\nFirmaet"
    )
    welcome_file_path = os.path.join(welcome_directory, f"Velkomst_{user.email}.txt")
    with open(welcome_file_path, 'w', encoding='utf-8') as file:
        file.write(welcome_text)
    print("Velkomstfil opdateret.")
    
def update_email_welcome_domain(user, new_email, new_domain_ext, users, welcome_directory, csv_directory):
    old_email = user.email
    old_domain_ext = user.domain_extension

    user.email = new_email
    user.domain_extension = new_domain_ext

    # Opdater brugerens oplysninger i brugerlisten
    for u in users:
        if u.email == old_email:
            u.email = new_email
        if u.domain_extension == old_domain_ext:
            u.domain_extension = new_domain_ext

    # Opdater velkomstteksten med den nye email
    update_welcome_text(user, welcome_directory, old_email)

    # Gem ændringerne i CSV-filen
    save_to_csv(users, csv_directory, FILENAME)
                
def confirm_action(message):
    response = input(f"{message} (ja/nej): ").strip().lower()
    return response == 'ja'

def update_fornavn(user, new_value):
    user.fornavn = new_value
    
def update_efternavn(user, new_value):
    user.efternavn = new_value

def update_email(user, new_value):
    user.email = new_value
    

def update_domain(user, new_value):
    user.domain = new_value

def update_domain_extension(user, new_value):
    user.domain_extension = new_value
    
    save_to_csv(users, csv_directory, FILENAME)

def update_director(user, new_value):
    user.director = new_value

def return_to_main_menu():
    response = input("Er du sikker på, at du vil vende tilbage til hovedmenuen? (ja/nej): ").lower()
    if response == 'ja':
        print("\n--- Går tilbage til hovedmenuen ---\n")
        return True 
    else:
        print("Fortsætter med den nuværende opgave.")
        return False 
        
# Ny funktion til at vise brugeroplysninger og detaljer
def show_users_and_details(users):
    while True:
        print("\nBrugerliste:")
        for i, user in enumerate(users, 1):
            initials = (user.first_name[0] + user.last_name[0]).lower()
            director = user.director.capitalize()
            print(f"{i}. {initials} - {user.email} - Direktør: {director}")

        print("\nIndtast nummeret på brugeren for at vise detaljer, eller skriv '0' for at vende tilbage til hovedmenuen.")
        action_choice = input("Brugernummer: ")

        if action_choice.lower() == '0':
            return_to_main_menu()
            break
        else:
            try:
                selected_user_index = int(action_choice) - 1
                if 0 <= selected_user_index < len(users):
                    selected_user = users[selected_user_index]
                    show_user_details(selected_user) 
                else:
                    print("Ugyldigt valg. Indtast venligst et gyldigt nummer.")
            except ValueError:
                print("Ugyldig input. Indtast venligst et gyldigt nummer eller '0'.")
    
def display_guidance():
    print("\nVEJLEDNING:")
    print("Denne vejledning hjælper dig med at navigere i brugeradministrationssystemet. Følgende muligheder er tilgængelige:")

    print("\n1. Opret Ny Bruger")
    print("   - Indtast brugerens fornavn, efternavn, domæne, domæneudvidelse og direktørens navn.")
    print("   - Gennemse og gem brugeroplysninger. Vælg '0' for at vende tilbage til den forrige menu.")

    print("\n2. Vis Brugere og Detaljer")
    print("   - Se en liste over brugere med initialer og email-adresser.")
    print("   - Vælg en bruger for at se detaljer. Brug '0' for at vende tilbage.")

    print("\n3. Rediger Bruger")
    print("   - Vælg en bruger fra listen for at redigere.")
    print("   - Opdater fornavn, efternavn, email eller direktør. Brug '0' for at afslutte.")

    print("\n4. Slet Bruger")
    print("   - Vælg en bruger for sletning eller vælg 'alle' for at slette alle brugere.")
    print("   - Bekræft dit valg. Brug '0' for at afbryde.")

    print("\n5. Hjælp")
    print("   - Viser denne vejledning.")
    
    print("\n6. Gem og Afslut")
    print("   - Gemmer alle brugeroplysninger i en CSV-fil og afslutter programmet.")

    print("\n7. Afslut uden at Gemme")
    print("   - Afslutter programmet uden at gemme ændringer.")
    print("   - Nyttig, hvis du ønsker at afslutte uden at gemme ændringer.\n")
    
    choice = input("Tryk 0 for at vende tilbage: ")
    if choice == '0':
        return_to_main_menu()