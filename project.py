import sys
import json
from tabulate import tabulate
from cryptography.fernet import Fernet
from getpass import getpass

class Password_manager:
    def __init__(self):
        self.key = self.load_key()
        try:
            with open("password_dict.json", "rb") as file:
                encrypted_data = file.read()
                self.password_dict = self.decrypt_file(encrypted_data)
        except FileNotFoundError:
            self.password_dict = {
                "example.com": {"username": "alice", "password": "password123"},
                "anotherapp.com": {"username": "bob", "password": "mypassword"},
            }
            self.save()

    def verify_identity(self):
        if "master_user" not in self.password_dict or not self.password_dict["master_user"]["password"]:
           self.password_dict["master_user"] = {"username": input("Please set a master username! "),"password": getpass("Please set a master password! ")}
           self.save()
           print("Master password was set successfully!\n")
           return True
        else:
            password = getpass("Please enter your master password: ")
            if password == self.password_dict["master_user"]["password"]:
                return True
            else:
                print("Incorrect Password. Please try again.\n")
                return False

    def load_key(self):
        with open("encrypt.key", "rb") as encryptkey:
            key = encryptkey.read()
            return key

    def encrypt_file(self, password_dict):
        f = Fernet(self.key)
        json_data = json.dumps(password_dict).encode('utf-8')
        return f.encrypt(json_data)

    def decrypt_file(self, encrypted_data):
        f = Fernet(self.key)
        decrypted_data = f.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode('utf-8'))

    def save(self):
        encrypted_data = self.encrypt_file(self.password_dict)
        with open ("password_dict.json", "wb") as file:
            file.write(encrypted_data)

    def add(self, app_website, username, password):
        self.password_dict[app_website] = {"username": username, "password": password}
        self.save()
        print(f"Password for {app_website} has been added.\n")

    def check_appWebsite(self, app_website):
        try:
            if app_website in self.password_dict:
                return True
            else:
                raise AssertionError(f"{app_website} is an Invalid app/website.\n")
        except AssertionError as e:
            print(e)

    def check_oldPassword(self, app_website, old_password):
        try:
            if self.password_dict[app_website]["password"] == old_password:
                return True
            else:
                raise AssertionError("Invalid Password\n")
        except AssertionError as e:
            print(e)

    def update(self, app_website):
        if self.check_appWebsite(app_website):
            old_password = input("Old password: ")
            if self.check_oldPassword(app_website, old_password):
                new_password = input("New password: ")
                self.password_dict[app_website]["password"] = new_password
                self.save()
                print(f"Password for {app_website} has been updated.\n")

    def delete(self, app_website):
        if self.check_appWebsite(app_website):
            old_password = input("Old password: ")
            if self.check_oldPassword(app_website, old_password):
                del self.password_dict[app_website]
                self.save()
                print(f"Password for {app_website} has been deleted.\n")

    def print_table(self):
        if self.password_dict:
            table_data = [
                [app_website, creds["username"], creds["password"]]
                for app_website, creds in self.password_dict.items()
            ]
            print(tabulate(table_data, headers =["App/Website", "Username", "Password"], tablefmt="pretty"))
        else:
            print("No existing password dictionary.\n")


def main ():
    manager = Password_manager ()
    commands = {
        "add": add,
        "update": update,
        "delete": delete,
        "list passwords": list_passwords,
        "quit": quit,
    }
    while not manager.verify_identity():
        pass
    while True:
        command = input("What would you like to do today? add/ update/ delete/ list passwords/ quit ").strip().lower()
        if command in commands:
            commands[command](manager)
        else:
            print(f"{command} is an invalid command, please try again.\n")

def add(manager):
    app_website = input("App/Website: ")
    username = input("Username: ")
    password = input("Password: ")
    manager.add(app_website, username, password)

def update(manager):
    app_website = input("App/Website: ")
    manager.update(app_website)

def delete(manager):
    app_website = input("App/Website: ")
    manager.delete(app_website)

def list_passwords(manager):
    manager.print_table()

def quit(_):
    sys.exit("Have a nice day!\n")

if __name__ == "__main__":
    main()
