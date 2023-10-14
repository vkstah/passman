from timeout import timer, reset_timer, maybe_timeout
from dotenv import dotenv_values
from views import new_entry, view_all
from db import Database
import threading
import inquirer
import bcrypt
import typer

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
  
  # Check validity of master password
  while True:
    print()
    master_password = inquirer.password(message="Enter Master Password")
    if db.check_master_password(master_password):
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

# Bootstrap the program
if __name__ == "__main__":
  typer.run(main)