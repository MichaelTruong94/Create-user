import os
from user import User
from config import WELCOME_DIRECTORY

def generate_welcome_text(user, welcome_directory):
    filename = f"Velkomst_{user.email}.txt"
    path = os.path.join(welcome_directory, filename)
    welcome_text = (
        f"Hej {user.first_name} {user.last_name}\n"
        f"Velkommen til Danit. Arbejdstiden er 8.10 til 15.00.\n"
        f"Vi forventer, du møder til tiden. Din email er: {user.email}\n"
        f"Med venlig hilsen\n{user.director}"
    )

    try:
        with open(path, mode="w", encoding="utf-8") as file:
            file.write(welcome_text)
        print(f"Velkomsttekst gemt i {filename}")
    except IOError as e:
        print(f"Fejl ved gemning af velkomsttekst: {str(e)}")

def update_email_and_welcome(user, new_email, csv_directory):
    old_email = user.email
    old_welcome_filename = f"Velkomst_{old_email}.txt"
    new_welcome_filename = f"Velkomst_{new_email}.txt"
    old_welcome_filepath = os.path.join(csv_directory, old_welcome_filename)
    new_welcome_filepath = os.path.join(csv_directory, new_welcome_filename)

    if os.path.exists(old_welcome_filepath):
        try:
            os.rename(old_welcome_filepath, new_welcome_filepath)
            print(f"Velkomstbrev opdateret til {new_email}.")
        except IOError as e:
            print(f"Fejl ved opdatering af velkomstbrev: {str(e)}")
    else:
        print(f"Velkomstbrevet for {old_email} blev ikke fundet.")

def update_welcome_text(user, welcome_directory, old_email):
    old_welcome_file_path = os.path.join(welcome_directory, f"Velkomst_{old_email}.txt")
    new_welcome_file_path = os.path.join(welcome_directory, f"Velkomst_{user.email}.txt")

    if os.path.exists(old_welcome_file_path):
        os.rename(old_welcome_file_path, new_welcome_file_path)
        print("Velkomstfil opdateret.")
    else:
        print("Ingen eksisterende velkomstfil fundet. En ny vil blive oprettet.")
        generate_welcome_text(user, welcome_directory)