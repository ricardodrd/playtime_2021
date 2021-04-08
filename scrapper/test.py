import csv
import time
import pandas as pd
from nsetools import Nse
from pprint import pprint
from datetime import datetime

nse = Nse()





while True:
    q = nse.get_quote('infy')
    now = datetime.now().strftime("%H:%M:%S")
    row = [now, q['lastPrice']]

    with open('python_live_plot_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    time.sleep(1)