from timeout import reset_timer, maybe_timeout
import inquirer

def delete_entry(entry, db):

  # Make sure the user is certain (and valid) by asking for the master password
  while True:
    master_password = inquirer.password(message="Enter Master Password")
    if db.check_master_password(master_password):
      break
    else:
      print('\033[91m' + f"[-] Incorrect password. Please try again." + '\033[0m')
      print()

  # Delete the entry
  db.delete_entry(entry.get_id())
  print('\033[92m' + f'[+] Deleted entry: {entry.get_name()}' + '\033[0m')
  print()