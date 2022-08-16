import time
import schedule
from api import get_price, response

def task():
    print("aaaaa")
    #get_price(response=response)
    

schedule.every().day.at("16:14").do(task)

while True:
    schedule.run_pending()
    time.sleep(1)