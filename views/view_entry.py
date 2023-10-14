from timeout import reset_timer, maybe_timeout
from views import edit_username, edit_password, delete_entry
import encryption
import pyperclip
import inquirer

def view_entry(id, db, master_password):
  choices = [
    ("Copy Username", "copy_username"),
    ("Copy Password", "copy_password"),
    ("Edit Username", "edit_username"),
    ("Edit Password", "edit_password"),
    ("Delete", "delete_entry"),
    ("Back", "back")
  ]

  while True:

    # Fetch a fresh entry from database
    entry = db.get_entry(id)

    # Reset timer and maybe timeout after choice
    reset_timer()
    choice = inquirer.list_input(f"Perform action with {entry.get_name()}", choices=choices)
    maybe_timeout(db)

    # Copy username
    if choice == 'copy_username':
      pyperclip.copy(entry.get_username())
      print('\033[92m' + f'[+] Copied Username to clipboard!' + '\033[0m')
      print()

    # Copy password
    elif choice == 'copy_password':
      vault_key = encryption.compute_vault_key(master_password)
      decrypted_password = encryption.decrypt(key=vault_key, source=entry.get_password()).decode()
      pyperclip.copy(decrypted_password)
      print('\033[92m' + f'[+] Copied Password to clipboard!' + '\033[0m')
      print()

    # Edit username
    elif choice == 'edit_username':
      edit_username(entry=entry, db=db)
    
    # Edit password
    elif choice == 'edit_password':
      edit_password(entry=entry, db=db, master_password=master_password)
    
    # Delete entry
    elif choice == 'delete_entry':
      delete_entry(entry=entry, db=db)
      break