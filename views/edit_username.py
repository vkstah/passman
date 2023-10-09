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
    if len(new_username) > 0: break
  
  # Edit the username column
  sql = db.cur.mogrify("""UPDATE password SET username = %s WHERE id = %s;""", (new_username, entry.get_id()))
  db.cur.execute(sql)
  db.conn.commit()
  
  print()
  print('\033[92m' + f'[+] New Username for {entry.get_name()}: {new_username}' + '\033[0m')
  print()