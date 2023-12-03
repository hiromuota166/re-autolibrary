import schedule
from time import sleep
import time

def job():
  print("I'm working...")

schedule.every().sunday.at("13:04").do(job)

while True:
  schedule.run_pending()
  time.sleep(1)