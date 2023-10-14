from timeout import reset_timer, maybe_timeout
from views import view_entry
import inquirer

def view_all(db, master_password):

  while True:

    # Fetch all entries from database
    entries = db.get_all_entries()

    # Reset timer and maybe timeout after choice
    reset_timer()
    choices = list(map(lambda entry: (entry.get_name(), entry), entries)) + ['Back']
    choice = inquirer.list_input("Please select an entry", choices=choices)
    maybe_timeout(db)

    # Handle choice
    if choice == 'Back':
      break
    else:
      view_entry(id=choice.get_id(), db=db, master_password=master_password)