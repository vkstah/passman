from timeout import timer, reset_timer, maybe_timeout
from dotenv import dotenv_values
from utils import clear
from db import Database
import encryption
import threading
import pyperclip
import inquirer
import bcrypt
import typer
import sys

def main(
  timeout: int = 90
):
  # Bail if no .env is found
  env = dotenv_values('.env')
  if not env:
    return
  
  # Establish connection to database
  db = Database(host=env['DB_HOST'], dbname=env['DB_NAME'], user=env['DB_USER'], password=env['DB_PASSWORD'], port=env['DB_PORT'])

  # Set the master password if it's not set already
  if not db.get_master_password():
    db.set_master_password()
  
  # Set secret key if it's not set already
  if not db.get_secret_key():
    db.set_secret_key()
  
  # Get the master password and compare it to the hashed one from storage
  master_password_hash = db.get_master_password()
  while True:
    print()
    master_password = inquirer.password(message="Enter Master Password")
    if bcrypt.checkpw(master_password.encode(), master_password_hash.encode()):
      print()
      break
    else:
      print('\033[91m' + f"[-] Incorrect password. Please try again." + '\033[0m')

  # Create timer thread to timeout the program after X amount of seconds
  timer_thread = threading.Thread(target=timer, daemon=True, args=(timeout,))
  timer_thread.start()

  choices=[('View all passwords', 'view'), ('Add new password', 'new'), ('Exit', 'exit')]
  while True:
    # Reset timer and maybe timeout after choice
    reset_timer()
    choice = inquirer.list_input("What would you like to do?", choices=choices)
    maybe_timeout(db)

    # Handle choice
    if choice == 'view':
      view_all(db=db, master_password=master_password)
    elif choice == 'new':
      new_entry(db=db, master_password=master_password)
    elif choice == 'exit':
      db.close()
      break

def view_all(db, master_password):

  # Fetch all passwords from database.
  db.cur.execute("""SELECT * FROM password;""")
  rows = db.cur.fetchall()

  choices = list(map(lambda x: (x[1], x), rows)) + ['Back']
  while True:

    # Reset timer and maybe timeout after choice
    reset_timer()
    choice = inquirer.list_input("Please select an entry", choices=choices)
    maybe_timeout(db)

    # Handle choice
    if choice == 'Back':
      break
    else:
      view_entry(entry=choice, db=db, master_password=master_password)

def view_entry(entry, db, master_password):

  # Reset timer and maybe timeout after choice
  reset_timer()
  choices = [
    ("Copy Username", "copy_username"),
    ("Copy Password", "copy_password"),
    ("Edit Username", "edit_username"),
    ("Edit Password", "edit_password"),
    ("Delete", "delete"),
    ("Back", "back")
  ]
  choice = inquirer.list_input(f"Perform action with {entry[1]}", choices=choices)
  maybe_timeout(db)

  # Handle choice
  if choice == 'copy_username':
    pyperclip.copy(entry[2])
    print('\033[92m' + f'[+] Copied Username to clipboard!' + '\033[0m')
    print()
    view_entry(entry, db)
  elif choice == 'copy_password':
    vault_key = encryption.compute_vault_key(master_password)
    decrypted_password = encryption.decrypt(key=vault_key, source=entry[3])
    pyperclip.copy(encryption.decrypt(key=vault_key, source=entry[3]).decode())
    print('\033[92m' + f'[+] Copied Password to clipboard!' + '\033[0m')
    print()
    view_entry(entry=entry, db=db, master_password=master_password)

def new_entry(db, master_password):

  # Get the name of the entry
  entries = db.get_all_passwords()
  while True:
    reset_timer()
    name = inquirer.text(message="Enter the name of the entry")
    maybe_timeout(db)
    found = False
    for entry in entries:
      if name in entry:
        found = True
        break
    if not found:
      break
    else:
      print('\033[91m' + f"[-] Duplicate name. Please choose a different name." + '\033[0m')

  # Get the username
  reset_timer()
  username = inquirer.text(message="Enter the Username")
  maybe_timeout(db)

  # Get the password
  reset_timer()
  password = inquirer.password(message="Enter the Password")
  maybe_timeout(db)

  # Encrypt the password
  vault_key = encryption.compute_vault_key(master_password)
  encrypted_password = encryption.encrypt(key=vault_key, source=password)

  # Run the query to store the entry
  sql = db.cur.mogrify("""INSERT INTO password ("name", "username", "password") VALUES (%s, %s, %s);""", (name, username, encrypted_password))
  db.cur.execute(sql)
  db.conn.commit()

  print()
  print('\033[92m' + f'[+] Stored new entry: {name}' + '\033[0m')
  print()

# Bootstrap the program
if __name__ == "__main__":
  typer.run(main)