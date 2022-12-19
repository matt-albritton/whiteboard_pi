import time
from datetime import datetime
import pytz
import subprocess


tz_NY = pytz.timezone('America/New_York') 
while True:
    now = datetime.now(tz_NY).strftime("%H:%M")
    print(now)
    if now == "01:00":
        subprocess.call("./run.sh")
        time.sleep(59)
    else:
        time.sleep(30)