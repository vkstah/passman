from getpass import getpass
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
                master_password VARCHAR(255)
    );          
    """)
    self.conn.commit()
  
  def get_master_password(self):
    self.cur.execute("""SELECT master_password FROM secret;""")
    self.conn.commit()
    master_password_hash = self.cur.fetchall()
    if not master_password_hash:
      return None
    else:
      return master_password_hash[0][0].encode()

  def set_master_password(self):
    while True:
      master_password = inquirer.password(message="Set your Master Password")
      if master_password == inquirer.password(message="Re-enter") and master_password != "":
        break
      print("Please try again.")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(master_password.encode(), salt)

    # Decode hash before we store it
    sql = self.cur.mogrify("""INSERT INTO secret (master_password) VALUES (%s)""", (hash.decode(),))
    self.cur.execute(sql)
    self.conn.commit()
  
  def close(self):
    self.cur.close()
    self.conn.close()