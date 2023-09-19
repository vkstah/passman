import psycopg2

class Database:
  def __init__(self, host, dbname, user, password, port):
    self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    self.cur = self.conn.cursor()
    self.maybe_setup()

  def maybe_setup(self):
    self.cur.execute("""CREATE TABLE IF NOT EXISTS password (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(255),
                username VARCHAR(255),
                password VARCHAR(255)
    );          
    """)
    self.conn.commit()
  
  def close(self):
    self.cur.close()
    self.conn.close()