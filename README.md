# Password Manager App
## Video Demo: <https://youtu.be/UPcdjTufX74>

## Description:

My password manager app is designed to store multiple passwords and usernames for various apps/websites. It allows you to add, update, delete, and list the stored passwords and usernames for the apps/websites. The passwords are stored in a Json file as a dictionary called password_dict. The key in the dictionary is an app/website and the values are password and username. This helps to organize the usernames and passwords to their respective app/website when called. The program uses Fernet encryption from python's Cryptography library. Instead of encrypting only the individual passwords, the program encrypts the entire Json file the passwords and usernames are stored in, enhancing security of the sensitive data. During each function executed by the app, the Password_manager.save() method encrypts the file again. The reason I opted to encrypt the entire file rather than the individual passwords is because it is important to protect the usernames as well. The program also lists out all of the passwords and usernames for you for your various apps/websites using python's tabulate library. Below I will go over each file in further detail. I hope to build upon this further by converting it into a .exe program so that it can be run off of the desktop!

## How to Use:
1. If encrypt.key does not exist. Run 'python encryption.py' in the command line to generate an encrypt.key file. If password_dict.json exists before you created the encrypt.key, delete password_dict.json.

2. Run 'python project.py' to use the Password manager app. If password_dict.json did not exist before inputting the command, project.py will generate a fresh password_dict.json with example app/websites stored inside which can be deleted.

3. Follow the prompts given to you by the password manager app to execute the desired actions.


## Files included

#### encryption.py
Before you can run the main project.py file, you must create an encryption key. Encryption.py utilizes Fernet encryption to generate an encryption key in a file called encrypt.key. This file is very important and will be utilized for encrypting and decrypting the json file where the passwords and usernames are stored. For trouble shooting, if the json file containing the dictionary becomes corrupted and is not working as intended, you will need to delete the existing encrypt.key and password_dict.json file. You must then rerun encryption.py to generate a new encrypt.key file, and then run project.py to regenerate a new password_dict.json file with the new encryption key.

#### encrypt.key
Encrypt.key is a key used by Fernet to encrypt and decrypt the password_dict.json file. This is generated from encryption.py. This file contains the encryption key.

#### password_dict.json
Password_dict.json stores the encrypted user data for their app/websites, usernames, and passwords. When running project.py for the first time, if a password_dict.json file does not exist, it will create one with example usernames and passwords: "example.com": {"username": "alice", "password": "password123"}, "anotherapp.com": {"username": "bob", "password": "mypassword"}. If it already exists, the file will have the stored passwords/usernames created by the user.

#### project.py
The main file, project.py, when ran for the first time will create an encrypted file called password_dict.json where it will store all of the passwords/usernames of the apps/websites the user inputs. The user will be greeted with a prompt that will ask for which command the user would like to execute: add, delete, update, and list passwords. The program has one class called Password_manager that has 8 class functions: load key, encrypt_file, decrypt_file, save, add, delete, update, check_appWebsite, check_oldPassword, and print_table.


## Non-class functions:
These functions handle the main operations of adding, deleting, updating, and listing the passwords. They each call on on a corresponding class method to perform their tasks.

#### main function:
The main function creates a new object called "manager" from the class Password_manager.It first calls on manager.verify_identity() to ask the user to input the correct master password. If manager.verify_identity() returns true, main() will prompt the user asking what command they would like to execute. The command options are stored in a dictionary which its values are used to call the corresponding function. After each command is completed, the main function will continue to loop until the user inputs "q" or "quit". If the user inputs a command that is not one of the options, it will print and inform the user that their inputted command is invalid.

#### add function:
If the user inputs "add" into the command line, the program will begin to ask for the name of the app/website, the username, and the password to store in password_dict.json. Afterwards, it will call the manager.add() class function which will add the new app/website to the password_dict.json file.

#### delete function:
If the user inputs "delete", the program will first ask the name of the app/website the user would like to delete. The delete() function will then call on the class function, manager.delete(). This function relies on the class methods self.check_oldPassword() and self.check_appWebsite() to determine if the app/website or passwords are valid. If the app/website is not found by self.check_appWebsite(), the program will raise an assertion error stating the app/website is invalid. If the app/website is found, self.delete() requests the user to input the current password ("old_password") before the program deletes it from the password_dict.json file. If the current password is found to be incorrect by self.check_oldPassword(), it will raise an assertion error stating it was an invalid password.

#### update function:
If the user inputs "update", the program will first ask the name of the app/website the user would like to update the password for. It will then call on the class function, manager.update(). This function relies on the class methods self.check_oldPassword() and self.check_appWebsite() to determine if the app/website or passwords are valid. If the app/website is not found by self.check_appWebsite(), the program will raise an assertion error stating the app/website is invalid. Similar to delete, if the old password inputted is found to be incorrect by self.check_oldPassword(), it will raise an assertion error. Once the user inputs the correct current password, self.update() will prompt for the new password, and save it to password_dict.json.

#### listing passwords:
If the user inputs list passwords, list_passwords() will call the class function manager.print_table(), to print out a table with columns: app/website, usernames, passwords. It will list all the currently stored passwords and usernames associated with their respective app/website. If self.print_table() cannot find password_dict.json, it prints out the message informing the user that there is no existing password dictionary.


## Password_manager Class Functions:
These functions assist the non-class functions in their tasks instructed by the user.

#### verify_identity:
Self.verify_identity() is used to create a self.password_dict object called "master_user" on the programs first run. On the first run, the program will ask the user to input a username and password for the master_user. This can be updated and changed just like any other self.password_dict object. On future runs, it requests the user to input their master password in order to gain access to the programs functions for stored passwords.

#### load_key:
Self.load_key opens the encrypt.key file and returns the key for the program to encrypt and decrypt the password_dict.json file.

#### encrypt_file:
Self.encrypt_file() uses the fernet function with self.key, updates the json file with json.dump by encoding the file into bits with utf-8. Afterwards it encrypts the file and returns it.

#### decrypt_file:
Self.decrypt_file() uses the fernet function with self.key, it decrypts the file, and then returns the decoded file from bits with utf-8.

#### save:
Self.save() uses the self.encrypt_file class function to encrypt the file, and then saves the changes made to the json file with using the .write method for files. This function is used at the end of self.add(), self.update(), and self.delete() before their respective print statements on a successful action.

#### add:
Self.add() creates a new object with 3 parameters along with self, app/website, password, and username which is taken from the user's inputs. Self.add() uses the self.save() class function, and then prints a string informing the user the password has been added. The self.add() function does not return anything so its return type is "None".

#### check_appWebsite:
The self.check_appWebsite() function takes in app/website and self as its parameters. This function checks whether or not the app/website inputted by the user is inside password_dict.json. If it is not found, an assertion error is raised stating that the inputted app/website is invalid. If it is found, the function returns True.

#### check_oldPassword:
The self.check_oldPassword function takes in app/website and old_password along with self as its parameters. Self.check_oldPassword() checks if the stored password for the verified app/website matches the input of the user for old_password. If it does not, an assertion error is raised stating that the inputted old_password is invald. If it does match, it returns True.

#### update:
The self.update() function takes in app/website along with self as its parameters. The function calls self.check_appWebsite() to checks if the app/website exists. If self.check_appWebsite() returns true, the function asks for the user to input the old password. Self.check_oldPasssword() is called to verify the old password inputted by the user. If the app/website or old_password does not exist or is incorrect, it will raise an assertion error. If the old_password matches the stored password, self.update asks the user to input the newly desired password, which will update the stored password in password_dict.json. A print statement is returned informing the user the password for the app/website has been updated.

#### delete:
The delete class function takes in app/website and self as its parameters. The function calls self.check_appWebsite() to checks if the app/website exists. If self.check_appWebsite() returns true, self.delete() asks for the user to input the old password. Self.check_oldPasssword() is called to verify the old password inputted by the user. If the app/website or old_password does not exist or is incorrect, the respective check function will raise an assertion error. If they match, self.delete() deletes the corresponding object from password_dict.json and prints stating the password for the app/website has been deleted. If the app/website or old_password does not exist or is incorrect, it will raise an assertion error.

#### print_table:
Self.print_table() first checks if self.password_dict exists. If self.password_dict does exist, it prints the objects in the dictionary (app/website) as a table with credits (Username, Password). If the dictionary does not exist, the function will print "No existing password dictionary."
