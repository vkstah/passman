from dotenv import dotenv_values
from db import Database
import threading
import pyperclip
import inquirer
import psycopg2
import _thread
import bcrypt
import typer
import time
import sys

def worker():
  counter = 5
  global reset
  reset = False
  while 1:
    time.sleep(1)
    counter -= 1

    if counter == 0:
      print('\033[91m' + "Timed out!" + '\033[0m')
      sys.exit()

    if reset:
      counter = 5
      reset = False

def reset_timer():
  global reset
  reset = True

def main(
  password: str = typer.Option(..., prompt="Master Password", hide_input=True)
):
  # Bail if no .env is found
  env = dotenv_values('.env')
  if not env:
    return
  
  # Establish connection to database
  db = Database(host=env['DB_HOST'], dbname=env['DB_NAME'], user=env['DB_USER'], password=env['DB_PASSWORD'], port=env['DB_PORT'])

  timer = threading.Thread(target=worker, daemon=False)
  timer.start()

  while 1:
    questions = [
      inquirer.List(
        'selection',
        message="What would you like to do?",
        choices=[
          ('View all passwords', 'view'),
          ('Add new password', 'new'),
          ('Exit', 'exit')
        ]
      )
    ]
    answers = inquirer.prompt(questions)
    if not answers:
      break

    if answers.get('selection') == 'view':
      reset_timer()
      view(db)

    if answers.get('selection') == 'exit':
      db.close()
      break

def view(db):
  db.cur.execute("""SELECT * FROM password;""")
  rows = db.cur.fetchall()
  choices = list(map(lambda x: (x[1], x), rows)) + ['Back']

  while 1:
    choice = inquirer.list_input("Please select an entry", choices=choices)
    if choice == 'Back':
      break
    else:
      entry(entry=choice, db=db)

def entry(entry, db):
  choices = [("Username", "username"), ("Password", "password"), ("Back", "back")]

  while 1:
    choice = inquirer.list_input(f"Copy {entry[1]}", choices=choices)
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

if __name__ == "__main__":
  typer.run(main)