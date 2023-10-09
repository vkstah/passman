class Entry:
  def __init__(self, row):
    self.id = row[0]
    self.name = row[1]
    self.username = row[2]
    self.password = row[3]

  def get_id(self):
    return self.id
  
  def get_name(self):
    return self.name
  
  def get_username(self):
    return self.username
  
  def get_password(self):
    return self.password