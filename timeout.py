import time
import sys

def timer(timeout):
  """Timer function to be used as the target parameter of an additional thread.
  
  Args:
    timeout (int): Number of seconds to timeout.
  """

  global timer_reset
  global timer_timedout

  timer_reset = False
  timer_timedout = False
  counter = timeout

  while 1:
    time.sleep(1)
    counter -= 1

    if counter == 0:
      timer_timedout = True
      break

    if timer_reset:
      counter = timeout
      timer_reset = False

def reset_timer():
  """Reset the timer back to its starting value.

  Under the hood this function will actually just flag to the thread that the counter needs to be reset.
  """
  global timer_reset
  timer_reset = True

def maybe_timeout(db):
  """Maybe timeouts the program.
  
  This function will check if the timer function has flagged the program as timed out. If that is the case,
  this function will also perform some cleanup tasks and exit the program.

  Args:
    db (Database): The database instance.
  """

  global timer_timedout
  if timer_timedout:
      print('\033[91m' + f"[-] You took too long and timed out! Please start the program again." + '\033[0m')
      db.close()
      sys.exit()