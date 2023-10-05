import time
import sys

def timer(timeout):
  global reset
  global timedout

  reset = False
  timedout = False
  counter = timeout

  while 1:
    time.sleep(1)
    counter -= 1

    if counter == 0:
      timedout = True
      break

    if reset:
      counter = timeout
      reset = False

def reset_timer():
  global reset
  reset = True

def maybe_timeout(db):
  global timedout
  if timedout:
      print('\033[91m' + f"[-] You took too long and timed out! Please start the program again." + '\033[0m')
      db.close()
      sys.exit()