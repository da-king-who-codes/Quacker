from replit import db

class Database:
  def newUser(self, username, password):
    db[username] = password
  def login(self, username, password):
    for item in db.keys():
      if item == username:
        if db[item] == password:
          return True
        else:
          return False
      else:
        return False
  def print_all(self):
    print(db.keys())
  def delete_key(self, key):
    del db[key] 
  def print_key(self, key):
    """
    Prints a specific Key
    """
    print(db[key])
  def get_all(self):
    """
    Returns all the items in the database
    """
    return db.keys()
  def delete_all(self):
    for item in db.keys():
      del db[item]