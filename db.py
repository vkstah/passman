from dotenv import dotenv_values
from entities import Entry
import psycopg2
import inquirer
import bcrypt

class Database:
  def __init__(self, host, dbname, user, password, port):
    self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    self.cur = self.conn.cursor()
    self.setup()

  def setup(self):
    self.cur.execute("""CREATE TABLE IF NOT EXISTS password (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(255),
                username VARCHAR(255),
                password VARCHAR(255)
    );          
    """)
    self.cur.execute("""CREATE TABLE IF NOT EXISTS secret (
                key VARCHAR(255),
                value VARCHAR(255)
    );          
    """)
    self.conn.commit()
  
  def get_master_password(self):
    self.cur.execute("""SELECT * FROM secret WHERE key = 'master_password';""")
    self.conn.commit()
    master_password_hash = self.cur.fetchall()
    if not master_password_hash:
      return None
    else:
      return master_password_hash[0][1]

  def set_master_password(self):
    while True:
      master_password = inquirer.password(message="Set your Master Password")
      if master_password == inquirer.password(message="Re-enter Master Password") and master_password != "":
        break
      print("Please try again.")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(master_password.encode(), salt)

    # Decode hash before we store it
    sql = self.cur.mogrify("""INSERT INTO secret (key, value) VALUES ('master_password', %s)""", (hash.decode(),))
    self.cur.execute(sql)
    self.conn.commit()
  
  def get_secret_key(self):
    self.cur.execute("""SELECT * FROM secret WHERE key = 'secret_key';""")
    self.conn.commit()
    secret_key = self.cur.fetchall()
    if not secret_key:
      return None
    else:
      return secret_key[0][0]

  def set_secret_key(self):
    env = dotenv_values('.env')
    try:
      secret_key = env["SECRET_KEY"]

      # Raise Exception if secret key isn't valid
      if len(secret_key) != 30:
        raise Exception
      
      # Store the secret key into database
      sql = self.cur.mogrify("""INSERT INTO secret (key, value) VALUES ('secret_key', %s)""", (secret_key,))
      self.cur.execute(sql)
      self.conn.commit()

    except:
      raise Exception("Failed to set secret key into the database. Make sure you have specified a valid secret key in your .env file")
  
  def get_all_passwords(self):
    self.cur.execute("""SELECT * FROM password ORDER BY id;""")
    self.conn.commit()
    return list(map(lambda x: Entry(x), self.cur.fetchall()))

  def get_password(self, id):
    sql = self.cur.mogrify("""SELECT * FROM password WHERE id = %s;""", (id,))
    self.cur.execute(sql)
    self.conn.commit()
    result = self.cur.fetchall()
    return Entry(result[0]) if len(result) > 0 else None
  
  def is_name_unique(self, name):
    sql = self.cur.mogrify("""SELECT * FROM password WHERE name = %s;""", (name,))
    self.cur.execute(sql)
    self.conn.commit()
    return True if len(self.cur.fetchall()) == 0 else False
  
  def close(self):
    self.cur.close()
    self.conn.close()