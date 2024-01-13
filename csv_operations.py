import os
import csv
from user import User
from config import CSV_DIRECTORY
from directory_operations import ensure_directory_exists
from welcome_generator import generate_welcome_text

script_directory = os.path.dirname(__file__)
brugere_directory = os.path.join(script_directory, "Brugere")
velkomst_directory = os.path.join(script_directory, "Velkomst")
ensure_directory_exists(brugere_directory)
ensure_directory_exists(velkomst_directory)

# Constants for CSV headers
CSV_HEADERS = ["Fornavn", "Efternavn", "Email", "Direktør"]

# Data handling related functions
def load_from_csv(csv_directory, filename):
    full_path = os.path.join(csv_directory, filename)
    users = []
    if os.path.exists(full_path):
        with open(full_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                if len(row) >= 4:
                    try:
                        first_name, last_name, email, director = row[:4]
                        # Splitting email
                        email_parts = email.split("@")
                        if len(email_parts) == 2 and '.' in email_parts[1]:
                            domain, domain_extension = email_parts[1].split(".", 1)
                            domain_extension = "." + domain_extension
                        else:
                            domain = "unknown"
                            domain_extension = ".unknown"

                        user = User(first_name, last_name, domain, domain_extension, director)
                        user.email = email
                        users.append(user)
                    except ValueError:
                        print("Fejl ved indlæsning af bruger fra CSV. Ignorerer række.")
    return users


def save_to_csv(users, csv_directory, filename):
    full_path = os.path.join(csv_directory, filename) 
    with open(full_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)
        for user in users:
            director = user.director.capitalize()
            writer.writerow([user.first_name, user.last_name, user.email, director])
    print(f"Brugere gemt i {full_path}")

# User interaction related functions
def save_user(users, user, csv_directory, welcome_directory):
    users.append(user)
    generate_welcome_text(user, welcome_directory)
    save_to_csv(users, csv_directory, "users.csv") 
    print(f"Bruger '{user.first_name} {user.last_name}' gemt med succes.")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")


# Global Constants
FILENAME = "users.csv"
CSV_DIRECTORY = brugere_directory  # Save CSV in the "Brugere" subdirectory
WELCOME_DIRECTORY = velkomst_directory  # Save Welcome files in the "Velkomst" subdirectory

# Ensure CSV and Welcome directories exist
ensure_directory_exists(CSV_DIRECTORY)
ensure_directory_exists(WELCOME_DIRECTORY)