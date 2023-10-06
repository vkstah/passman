from dotenv import dotenv_values
from db import Database
import threading
import pyperclip
import inquirer
from timeout import timer, reset_timer, maybe_timeout
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
      view(db)
    elif choice == 'exit':
      db.close()
      break

def view(db):

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
      entry(entry=choice, db=db)

def entry(entry, db):
  choices = [
    ("Copy Username", "copy_username"),
    ("Copy Password", "copy_password"),
    ("Edit Username", "edit_username"),
    ("Edit Password", "edit_password"),
    ("Delete", "delete"),
    ("Back", "back")
  ]
  while True:

    # Reset timer and maybe timeout after choice
    reset_timer()
    choice = inquirer.list_input(f"Perform action with {entry[1]}", choices=choices)
    maybe_timeout(db)

    # Handle choice
    if choice == 'back':
      break
    elif choice == 'copy_username':
      pyperclip.copy("Implement me!")
      print('\033[92m' + f'[+] Copied Username to clipboard!' + '\033[0m')
      print()
    elif choice == 'copy_password':
      pyperclip.copy(entry[2])
      print('\033[92m' + f'[+] Copied Password to clipboard!' + '\033[0m')
      print()

def new(db):
  pass

# Bootstrap the program
if __name__ == "__main__":
  typer.run(main)