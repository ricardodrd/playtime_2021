import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import argparse

plt.style.use('seaborn')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
path = 'realtime_data_GME.csv'
#
def plot_realtime(i):
    df_stock = pd.read_csv(path)
    print(df_stock[0:i])
    x = df_stock[0:i]['timestamp']
    y = df_stock[0:i]['price']
    ax.clear()
    ax.plot(x, y)
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="path to csv", type=str)
    args = parser.parse_args()
    # plot_realtime(args.csv_path)
    animation = FuncAnimation(fig, func=plot_realtime, interval=1000)
    plt.show()
