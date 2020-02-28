__author__ = "Ricard Lado"
__copyright__ = "Copyright 2020, Lado"
__credits__ = ["Ricard Lado"]
__license__ = "GPLv3"


import argparse
import multiprocessing
import queue
import time

import matplotlib.pyplot as plt
from EkgEmgReader import EkgEmgReader, utils

#Plot style
plt.style.use('seaborn-pastel')

#Argparser
parser=argparse.ArgumentParser(description='Plot EKG/EMG data in real time')
parser.add_argument('-p','--port',type=str,required=True,metavar='',help='Serial port')
parser.add_argument('-b','--baud',type=int,required=True,metavar='',help='Baud rate')
parser.add_argument('-v','--verbose',type=bool,default=False,required=False,metavar='',help='Show packet count and channel data on the terminal')
args=parser.parse_args()


def plot(xdata,ydata):
    while True:
        plt.cla()
        plt.plot(xdata.get(),ydata.get())
        plt.pause(0.01)

if __name__=='__main__':
    ekgSer=EkgEmgReader.serial_ekg(port=args.port,baudrate=args.baud,timeout=1)

    x_q=multiprocessing.Queue(2)
    y_q=multiprocessing.Queue(2)

    time_plot_data=utils.looping_list(512)
    channel_1_plot_data=utils.looping_list(512)
    
    plot_process=multiprocessing.Process(target=plot, args=(x_q,y_q))
    plot_process.start()

    tZero=time.time()

    try:
        while True:
            ekgSer.read_packet()

            if not ekgSer.packet.read_error:
                if args.verbose:
                    print(ekgSer.packet.packet_count)
                    print(ekgSer.packet.channel)
                
                time_plot_data.append(time.time()-tZero)
                channel_1_plot_data.append(ekgSer.packet.channel[0])

                try:
                    if x_q.full() or y_q.full():
                        x_q.get_nowait()
                        y_q.get_nowait()
                except queue.Empty:
                    pass
                try:
                    x_q.put_nowait(time_plot_data.list)
                    y_q.put_nowait(channel_1_plot_data.list)
                except queue.Full:
                    pass

    except KeyboardInterrupt:
        plot_process.terminate()
