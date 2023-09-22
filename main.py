from dotenv import dotenv_values
from db import Database
import pyperclip
import inquirer
import psycopg2
import bcrypt
import typer

def main(
  password: str = typer.Option(..., prompt="Master Password", hide_input=True)
):
  # Bail if no .env is found
  env = dotenv_values('.env')
  if not env:
    return
  
  # Establish connection to database
  db = Database(host=env['DB_HOST'], dbname=env['DB_NAME'], user=env['DB_USER'], password=env['DB_PASSWORD'], port=env['DB_PORT'])

  while 1:
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

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

    if answers.get('selection') == 'view':
      view(db)

    if answers.get('selection') == 'exit':
      db.close()
      break

def view(db):
  db.cur.execute("""SELECT * FROM password;""")
  rows = db.cur.fetchall()
  choices = list(map(lambda x: (x[1], str(x[2])), rows)) + [('Exit', 'exit')]

  while 1:
    choice = inquirer.list_input("Select the password to copy it to clipboard", choices=choices)
    if choice == 'exit':
      break
    else:
      pyperclip.copy(choice)
      print('\033[92m' + 'Copied password to clipboard!' + '\033[0m')
      print()

"""Check the validity of a password.

Attributes:
  password: The encoded raw password.
  hashed_password: The hashed password.
"""
def check_password(password, hashed_password):
  return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
  typer.run(main)