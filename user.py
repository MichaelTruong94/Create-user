class User:
    VALID_DOMAIN_CHOICES = ['theimperium', 'local']
    VALID_DIRECTOR_NAME = 'Leto Atreides'

    def __init__(self, first_name, last_name, domain, domain_extension, director):
        self.first_name = first_name
        self.last_name = last_name
        self.email = None 
        self.domain = domain
        self.domain_extension = domain_extension
        self.director = director

    def generate_email(self):
        if self.first_name and self.last_name:  
            self.email = f"{self.first_name[0].lower()}{self.last_name[0].lower()}@{self.domain.lower()}{self.domain_extension.lower()}"
        else:
            print("Fejl: Fornavn og/eller efternavn er ikke angivet.")
            self.email = ""
    
    def capitalize_director(self):
        self.director = self.director.capitalize()

    @staticmethod
    def get_valid_domain_choice():
        while True:
            domain_choice = input("Vælg domæne ('TheImperium' eller 'Local'): ").lower()
            if domain_choice in User.VALID_DOMAIN_CHOICES:
                return domain_choice
            else:
                print("Ugyldigt domæne. Indtast venligst et gyldigt domæne.")

    @staticmethod
    def get_domain_extension():
        while True:
            domain_extension = input("Indtast domæneudvidelse (f.eks., '.com', '.dk'): ")
            if domain_extension.startswith("."):
                return domain_extension
            else:
                print("Ugyldig domæneudvidelse. Skal starte med '.'.")

    @staticmethod
    def get_director_name():
        while True:
            director_input = input("Indtast Direktørens Fulde Navn: ")
            if director_input.lower() == User.VALID_DIRECTOR_NAME.lower():
                return User.VALID_DIRECTOR_NAME
            else:
                print("Ugyldigt direktørens navn. Prøv igen.")

    @staticmethod
    def input_user_details():
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        domain = User.get_valid_domain_choice()
        domain_extension = User.get_domain_extension()
        director = User.get_director_name()
        return first_name, last_name, domain, domain_extension, director

    @staticmethod
    def save_user(users, user, welcome_directory):
        users.append(user)  # Tilføj brugeren først
        generate_welcome_text(user, welcome_directory)
        save_to_csv(users, csv_directory)  # Gem straks i CSV
        print(f"Bruger '{user.first_name} {user.last_name}' gemt med succes.")
        return True
