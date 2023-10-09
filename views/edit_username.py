from timeout import reset_timer, maybe_timeout
import inquirer

def edit_username(entry, db):

  # Extract the current username
  current_username = entry.get_username()

  # Get the new username
  while True:
    reset_timer()
    new_username = inquirer.text(message=f"Enter new Username for {entry.get_name()}")
    maybe_timeout(db)

    # Validate the new username
    if not len(new_username) > 0:
      print('\033[91m' + f"[-] Username cannot be empty." + '\033[0m')
      continue

    # Break from loop if all checks have passed
    break
  
  # Edit the username column
  sql = db.cur.mogrify("""UPDATE password SET username = %s WHERE id = %s;""", (new_username, entry.get_id()))
  db.cur.execute(sql)
  db.conn.commit()
  
  print()
  print('\033[92m' + f'[+] Updated Username for {entry.get_name()}!' + '\033[0m')
  print()