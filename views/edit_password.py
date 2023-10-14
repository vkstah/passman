from timeout import reset_timer, maybe_timeout
import encryption
import inquirer

def edit_password(entry, db, master_password):
  
  # Get the new password from user
  while True:
    reset_timer()
    new_password = inquirer.password(message=f"Enter new Password for {entry.get_name()}")
    maybe_timeout(db)

    # Validate the new password
    if not len(new_password) >= 16:
      print('\033[91m' + f"[-] Password should be 16 characters or longer." + '\033[0m')
      continue

    if not any(char.isdigit() for char in new_password):
      print('\033[91m' + f"[-] Password should have at least one numeral." + '\033[0m')
      continue

    if not any(char.isupper() for char in new_password):
      print('\033[91m' + f"[-] Password should have at least one uppercase letter." + '\033[0m')
      continue

    if not any(char.islower() for char in new_password):
      print('\033[91m' + f'[-] Password should have at least one lowercase letter.' + '\033[0m')
      continue
    
    # Break from loop if all checks passed
    break

  # Verify the password by asking the user to re-type it
  while True:
    reset_timer()
    new_password_retyped = inquirer.password(message=f"Re-enter the new Password")
    maybe_timeout(db)

    if not new_password_retyped == new_password:
      print('\033[91m' + f'[-] Incorrect. Please try again.' + '\033[0m')
      continue
    
    # Break from loop if the passwords match
    break

  # Verify once more that the user does want to change the password
  reset_timer()
  are_you_sure = inquirer.confirm(message=f"Are you sure you want to change the Password?", default=False)
  maybe_timeout(db)

  if not are_you_sure:
    print('\033[91m' + f'[-] Aborted Password edit!' + '\033[0m')
    print()
    return

  # Encrypt the password
  vault_key = encryption.compute_vault_key(master_password)
  encrypted_password = encryption.encrypt(key=vault_key, source=new_password)

  # Update the password
  sql = db.cur.mogrify("""UPDATE password SET password = %s WHERE id = %s;""", (encrypted_password, entry.get_id()))
  db.cur.execute(sql)
  db.conn.commit()

  print('\033[92m' + f'[+] Updated Password for {entry.get_name()}!' + '\033[0m')
  print()