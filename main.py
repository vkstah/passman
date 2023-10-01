from dotenv import dotenv_values
from db import Database
import threading
import pyperclip
import inquirer
import threads
import typer
import sys

def main(
  master_password: str = typer.Option(..., prompt="Master Password", hide_input=True),
  timeout: int = 90
):
  # Bail if no .env is found
  env = dotenv_values('.env')
  if not env:
    return
  
  # Establish connection to database
  db = Database(host=env['DB_HOST'], dbname=env['DB_NAME'], user=env['DB_USER'], password=env['DB_PASSWORD'], port=env['DB_PORT'])

  # Create timer thread to timeout the program after X amount of seconds
  timer_thread = threading.Thread(target=threads.timer, daemon=True, args=(timeout,))
  timer_thread.start()

  choices=[('View all passwords', 'view'), ('Add new password', 'new'), ('Exit', 'exit')]
  while True:

    # Reset timer and maybe timeout after choice
    threads.reset_timer()
    choice = inquirer.list_input("What would you like to do?", choices=choices)
    threads.maybe_timeout(db)

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
    threads.reset_timer()
    choice = inquirer.list_input("Please select an entry", choices=choices)
    threads.maybe_timeout(db)

    # Handle choice
    if choice == 'Back':
      break
    else:
      entry(entry=choice, db=db)

def entry(entry, db):
  choices = [("Username", "username"), ("Password", "password"), ("Back", "back")]
  while True:

    # Reset timer and maybe timeout after choice
    threads.reset_timer()
    choice = inquirer.list_input(f"Copy {entry[1]}", choices=choices)
    threads.maybe_timeout(db)

    # Handle choice
    if choice == 'back':
      break
    elif choice == 'username':
      pyperclip.copy("Implement me!")
      print('\033[92m' + f'Copied Username to clipboard!' + '\033[0m')
      print()
    elif choice == 'password':
      pyperclip.copy(entry[2])
      print('\033[92m' + f'Copied Password to clipboard!' + '\033[0m')
      print()

# Bootstrap the program
if __name__ == "__main__":
  typer.run(main)