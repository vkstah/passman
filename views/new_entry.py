from timeout import reset_timer, maybe_timeout
import encryption
import inquirer

def new_entry(db, master_password):

  # Get the name of the entry
  entries = db.get_all_passwords()
  while True:
    reset_timer()
    name = inquirer.text(message="Enter the name of the entry")
    maybe_timeout(db)
    found = False
    for entry in entries:
      if name in entry:
        found = True
        break
    if not found:
      break
    else:
      print('\033[91m' + f"[-] Duplicate name. Please choose a different name." + '\033[0m')

  # Get the username
  reset_timer()
  username = inquirer.text(message="Enter the Username")
  maybe_timeout(db)

  # Get the password
  reset_timer()
  password = inquirer.password(message="Enter the Password")
  maybe_timeout(db)

  # Encrypt the password
  vault_key = encryption.compute_vault_key(master_password)
  encrypted_password = encryption.encrypt(key=vault_key, source=password)

  # Run the query to store the entry
  sql = db.cur.mogrify("""INSERT INTO password ("name", "username", "password") VALUES (%s, %s, %s);""", (name, username, encrypted_password))
  db.cur.execute(sql)
  db.conn.commit()

  print()
  print('\033[92m' + f'[+] Stored new entry: {name}' + '\033[0m')
  print()