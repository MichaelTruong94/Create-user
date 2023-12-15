import os
import csv
import tkinter as tk
from tkinter import messagebox
import hashlib

class BrugeradministrationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Brugeradministration")
        self.create_widgets()
        self.current_step = 0
        self.bruger_data = ["", "", "", "", "", ""]
        self.entry_labels = ["Fornavn", "Efternavn", "Direktørens navn", "Domæne navn", "TLD Topleveldomain"]
        self.entry_widgets = []
        self.program_directory = os.path.dirname(os.path.abspath(__file__))

    def create_widgets(self):
        self.vis_bruger_button = tk.Button(self.master, text="Vis bruger", command=self.vis_bruger)
        self.vis_bruger_button.grid(row=0, column=0, pady=10)

        self.opret_bruger_button = tk.Button(self.master, text="Opret bruger", command=self.opret_bruger)
        self.opret_bruger_button.grid(row=1, column=0, pady=10)

        self.slet_en_bruger_button = tk.Button(self.master, text="Slet en bruger", command=self.slet_en_bruger)
        self.slet_en_bruger_button.grid(row=2, column=0, pady=10)

        self.slet_bruger_button = tk.Button(self.master, text="Slet alle brugere", command=self.slet_alle_brugere)
        self.slet_bruger_button.grid(row=3, column=0, pady=10)

        self.udskriv_bruger_button = tk.Button(self.master, text="Udskriv bruger", command=self.udskriv_bruger)
        self.udskriv_bruger_button.grid(row=4, column=0, pady=10)

        self.afslut_button = tk.Button(self.master, text="Afslut", command=self.master.destroy)
        self.afslut_button.grid(row=5, column=0, pady=10)

    def create_entry_widgets(self):
        self.entry_label = tk.Label(self.master, text=f"Indtast {self.entry_labels[self.current_step]}:")
        self.entry_label.grid(row=0, column=1, padx=10, pady=5)

        self.entry_widget = tk.Entry(self.master)
        self.entry_widget.grid(row=0, column=2, padx=10, pady=5)
        self.entry_widget.focus()

        self.entry_widgets.extend([self.entry_label, self.entry_widget])

    

    def create_næste_button(self):
        self.næste_button = tk.Button(self.master, text="Næste", command=self.finish_process)
        self.næste_button.grid(row=1, column=1, columnspan=2, pady=10)
        self.master.bind("<Return>", self.handle_next_button)

    def handle_next_button(self, event=None):
        self.opret_ny_bruger_action()

    def opret_ny_bruger_action(self):
        if not self.validate_entry():
            return

        if self.current_step == 2 and not self.validate_director_name():
            return
        elif self.current_step == 3 and not self.validate_domain_name():
            return

        if self.current_step == len(self.entry_labels) - 1:
            self.clear_entries()
            self.opret_bruger()
        else:
            self.current_step += 1
            self.create_entry_widgets()
            self.create_next_button()

            if self.current_step == len(self.entry_labels) - 1:
                self.disable_buttons()

    def validate_director_name(self):
        director_name = self.entry_widget.get().strip().lower()
        if director_name != "leto atreides":
            messagebox.showinfo("Ugyldig input", "Direktørens navn skal være 'Leto Atreides'.")
            return False
        return True

    def validate_domain_name(self):
        domain_name = self.entry_widget.get().strip().lower()
        if domain_name != "theimperium.local":
            messagebox.showinfo("Ugyldig input", "Domænenavnet skal være 'TheImperium.local'.")
            return False
        return True

    def create_admin_code_entry(self):
        self.kode_label = tk.Label(self.master, text="Indtast administrator kode:")
        self.kode_label.grid(row=1, column=1, padx=10, pady=5)

        self.kode_entry = tk.Entry(self.master, show="*")
        self.kode_entry.grid(row=1, column=2, padx=10, pady=5)
        self.kode_entry.focus()
        if self.current_step == 5:  # Step where admin code is entered
            self.create_admin_code_button()

    def clear_entries(self):
        for widget in self.entry_widgets:
            widget.destroy()
        self.entry_widgets = []

        if hasattr(self, "næste_button"):
            self.næste_button.destroy()

    def validate_admin_code(self):
        kode_input = self.kode_entry.get().strip()
        hashed_input = hashlib.sha256(kode_input.encode()).hexdigest()
        actual_hashed_password = "d9ff834b36f8d0cceadf79022335d51ca1ecd030208b65c98bc917848d4a16f6"
        if hashed_input == actual_hashed_password:
            return True
        else:
            messagebox.showerror("Adgangskode forkert", "Adgangskoden er forkert.")
            return False

    def create_admin_code_button(self):
        self.næste_button = tk.Button(self.master, text="Opret", command=self.finish_process)
        self.næste_button.grid(row=1, column=1, columnspan=2, pady=10)
        self.master.bind("<Return>", lambda event=None: self.næste_button.invoke())

    def disable_buttons(self):
        self.opret_bruger_button.config(state=tk.DISABLED)
        self.slet_bruger_button.config(state=tk.DISABLED)
        self.udskriv_bruger_button.config(state=tk.DISABLED)

    def opret_bruger(self):
        self.clear_entries()
        self.create_bruger_navn_entry()
        self.create_næste_button()
        self.master.bind("<Return>", self.handle_next_button)

    def create_bruger_navn_entry(self):
        self.bruger_navn_label = tk.Label(self.master, text=f"Indtast {self.entry_labels[0]}:")
        self.bruger_navn_label.grid(row=0, column=1, padx=10, pady=5)

        self.bruger_navn_entry = tk.Entry(self.master)
        self.bruger_navn_entry.grid(row=0, column=2, padx=10, pady=5)
        self.bruger_navn_entry.focus()

    def create_næste_button(self):
        self.næste_button = tk.Button(self.master, text="Næste", command=self.finish_process)
        self.næste_button.grid(row=1, column=1, columnspan=2, pady=10)

    def finish_process(self):
        if self.current_step == 0:
            self.create_næste_button()
        elif self.current_step == 1:
            bruger_kode = self.bruger_kode_entry.get().strip()
            valid_input = self.validate_input(bruger_kode, 5)
            if not valid_input:
                return

            self.bruger_data[5] = bruger_kode
            self.current_step += 1
            self.create_bruger_navn_entry()
            self.create_næste_button()
        else:
            self.current_step += 1
            bruger_navn = self.bruger_navn_entry.get().strip()
            self.bruger_data[0] = bruger_navn

            if self.current_step == 3:
                self.bruger_data[1] = self.entry_widget.get().strip()
                valid_input = self.validate_input(self.bruger_data[1], 1)
                if not valid_input:
                    return

                self.slet_alle_brugere()
            else:
                self.create_entry_widgets()
                self.create_next_button()

            if self.current_step == 5:  # Step where admin code is entered
                if not self.validate_admin_code():
                    return

            self.clear_entries()
            self.opret_bruger()

    def validate_input(self, input_text, index):
        if index == 5:
            if not input_text:
                messagebox.showerror("Manglende information", "Indtast venligst adgangskoden.")
                return False
        else:
            if not input_text:
                messagebox.showerror("Manglende information", f"Indtast venligst {self.entry_labels[index].lower()}.")
                return False
        return True

    def slet_en_bruger(self):
        bruger_navn = self.bruger_navn_entry.get().strip()
        if not bruger_navn:
            messagebox.showerror("Manglende information", "Indtast venligst brugerens navn.")
            return

        bruger_data = self.get_user_data(bruger_navn)
        if not bruger_data:
            messagebox.showerror("Fejl", f"Ingen bruger fundet med navnet: {bruger_navn}")
            return

        self.delete_user(bruger_navn)
        messagebox.showinfo("Bruger slettet", f"Bruger '{bruger_navn}' er blevet slettet.")

    def vis_bruger(self):
        bruger_navn = self.bruger_navn_entry.get().strip()
        if not bruger_navn:
            messagebox.showerror("Manglende information", "Indtast venligst brugerens navn.")
            return

        bruger_data = self.get_user_data(bruger_navn)
        if not bruger_data:
            messagebox.showerror("Fejl", f"Ingen bruger fundet med navnet: {bruger_navn}")
            return

        self.clear_entries()
        self.display_user_data(bruger_data)

    def display_user_data(self, bruger_data):
        info_label = tk.Label(self.master, text="Brugerinformation:")
        info_label.grid(row=0, column=1, columnspan=2, pady=10)

        for i, (key, value) in enumerate(bruger_data.items()):
            label = tk.Label(self.master, text=f"{key}: {value}")
            label.grid(row=i + 1, column=1, columnspan=2, pady=5)

        self.create_tilbage_button()

    def create_tilbage_button(self):
        tilbage_button = tk.Button(self.master, text="Tilbage", command=self.clear_and_create_main_buttons)
        tilbage_button.grid(row=len(self.entry_labels) + 1, column=1, columnspan=2, pady=10)

    def clear_and_create_main_buttons(self):
        self.clear_entries()
        self.create_widgets()

    def slet_alle_brugere(self):
        self.delete_all_users()
        messagebox.showinfo("Alle brugere slettet", "Alle brugere er blevet slettet.")

    def delete_user(self, bruger_navn):
        # Implementer logik for at slette en bruger fra opbevaring (f.eks. CSV-fil)
        # I dette eksempel udskriver vi bare en besked for at simulere sletning.
        print(f"Sletter bruger: {bruger_navn}")

        # Implementer den faktiske logik for at slette en bruger fra opbevaring her
        # Du kan f.eks. opdatere CSV-filen for at fjerne brugeren

    def delete_all_users(self):
        # Implementer logik for at slette alle brugere fra opbevaring (f.eks. CSV-fil)
        # I dette eksempel udskriver vi bare en besked for at simulere sletning.
        print("Sletter alle brugere")

        # Implementer den faktiske logik for at slette alle brugere fra opbevaring her
        # Du kan f.eks. slette hele indholdet af CSV-filen

    def get_user_data(self, bruger_navn):
        # Implementer logik for at hente brugerdata fra opbevaring (f.eks. CSV-fil)
        return self.hent_bruger(bruger_navn)

    def hent_bruger(self, bruger_navn):
        # Implementer logik for at hente brugerdata (f.eks. læs fra en CSV-fil)
        with open(os.path.join(self.program_directory, 'bruger_data.csv'), mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].lower() == bruger_navn.lower():
                    return {
                        "Brugernavn": row[0],
                        "Fornavn": row[1],
                        "Efternavn": row[2],
                        "Direktørnavn": row[3],
                        "Domænenavn": row[4],
                        "Topleveldomain": row[5],
                        "Email": row[6]
                    }
        return None

    def udskriv_bruger(self):
        bruger_navn = self.bruger_navn_entry.get().strip()
        if not bruger_navn:
            messagebox.showerror("Manglende information", "Indtast venligst brugerens navn.")
            return

        bruger_data = self.get_user_data(bruger_navn)
        if not bruger_data:
            messagebox.showerror("Fejl", f"Ingen bruger fundet med navnet: {bruger_navn}")
            return

        self.print_user_data(bruger_data)

    def print_user_data(self, bruger_data):
        print("Brugerinformation:")
        for key, value in bruger_data.items():
            print(f"{key}: {value}")

# Opret hovedvinduet
root = tk.Tk()
app = BrugeradministrationGUI(root)

# Kør hovedløkken
root.mainloop()
