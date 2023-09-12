from dotenv import dotenv_values
import pyperclip
import inquirer
import psycopg2
import bcrypt
import typer

def main(
  password: str = typer.Option(..., prompt=True, hide_input=True)
):
  # Bail if no .env is found
  env = dotenv_values('.env')
  if not env:
    return
  
  # Establish connection to database
  conn = psycopg2.connect(host=env['DB_HOST'], dbname=env['DB_NAME'], user=env['DB_USER'], password=env['DB_PASSWORD'], port=env['DB_PORT'])
  cur = conn.cursor()

  # (Maybe) setup the database
  cur.execute("""CREATE TABLE IF NOT EXISTS password (
              id BIGSERIAL PRIMARY KEY,
              name VARCHAR(255),
              password VARCHAR(255)
  );          
  """)
  conn.commit()

  exit = False
  while not exit:
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
      view(conn, cur)

    if answers.get('selection') == 'exit':
      cleanup(conn, cur)
      exit = True

def view(conn, cur):
  cur.execute("""SELECT * FROM password;""")
  rows = cur.fetchall()
  choices = list(map(lambda x: (x[1], str(x[2])), rows)) + [('Exit', 'exit')]

  exit = False
  while not exit:
    choice = inquirer.list_input("Select the password to copy it to clipboard", choices=choices)
    if choice == 'exit':
      exit = True
    else:
      pyperclip.copy(choice)
      print('\033[92m' + 'Copied password to clipboard!' + '\033[0m')
      print()

def cleanup(conn, cur):
  cur.close()
  conn.close()

"""Check the validity of a password.

Attributes:
  password: The encoded raw password.
  hashed_password: The hashed password.
"""
def check_password(password, hashed_password):
  return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
  typer.run(main)