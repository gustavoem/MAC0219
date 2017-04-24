#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

def plot_timeXinput(results):
    reg = "seahorse"
    NUM_COLORS = 12
    fig = plt.figure(figsize=(14, 8))
    cm = plt.get_cmap('gist_rainbow')
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    # ax.set_xscale('log', basex=2)
    # ax.set_yscale('log', basey=4)


    xlist = []
    ylists = [[] for _ in range(0, 6)]
    for i in range(4, 14):
        size = 2 ** i
        xlist.append(size)
        for j in range(0, 6):
            nThreads = 2 ** j
            ylists[j].append(results[nThreads][size][reg]["avg"])

    legend_handles = []
    legends = []
    for i, ylist in enumerate(ylists):
        nThreads = 2 ** i
        threads, = plt.plot(xlist, ylist, 'o', mfc='none')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        legend_handles.append(threads)
        legends.append(str(nThreads) + " Threads")
    ax.legend(legend_handles, legends)


    plt.title('Time of execution X input size')
    plt.ylabel('Time (s)')
    plt.xlabel('Input size')
    # ax.yaxis.grid(True)

    my_xticks = ['$2^{4}$','$2^{5}$','$2^{6}$','$2^{7}$', '$2^{8}$', '$2^{9}$', '$2^{10}$', '$2^{11}$', '$2^{12}$', '$2^{13}$']
    plt.xticks(xlist, my_xticks)
    # plt.yscale('log')

    plt.show()


# Plot data
def plot_timeXthread(results):
    reg = "full"
    NUM_COLORS = 25
    fig = plt.figure(figsize=(14, 8))
    cm = plt.get_cmap('gist_rainbow')
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    xlist = []
    ylists = [[] for _ in range(4, 14)]

    ylist = []
    ylist2 = []
    for i in range(0, 6):
        nThreads = 2 ** i
        xlist.append(nThreads)
        for j in range (4, 14):
            size = 2 ** j
            ylists[j - 4].append(results[nThreads][size][reg]["avg"])

    legend_handles = []
    legends = []
    for i, ylist in enumerate(ylists):
        size = 2 ** (i + 4)
        sizex, = plt.plot(xlist, ylist, 'o', mfc='none')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        legend_handles.append(sizex)
        legends.append(str(size) + " px")
    ax.legend(legend_handles, legends)

    plt.title('Time of execution X number of threads')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of threads')
    # ax.yaxis.grid(True)
    plt.show()



if __name__ == '__main__':
    results_dir = sys.argv[1]

    if results_dir[-1] != '/':
        results_dir+='/'

    inputs = ["full", "seahorse", "elephant", "spiral"]
    results = {}


    print("*" + results_dir + "*")

    test = sys.argv[1]
    for i in range(0, 6):
        nThreads = 2 ** i
        results[nThreads] = {}

        for j in range(4, 14):
            size = 2 ** j
            results[nThreads][size] = {}
            file_name = ""

            for region in inputs:
                results[nThreads][size][region] = {}
                file_name = region + "_" + str(size) + "px_" + str(nThreads) + "threads.log"
                result_file = open (results_dir + file_name)
                for line in result_file:
                    match = re.search ('(\d+(\.|,)\d+)\s+seconds\s+time\s+elapsed\s+\(\s+\+\-\s+(\d+(\.|,)\d+)%\s+\)', line)
                    if match:
                        avg = float (match.group (1))
                        std_dev = (float (match.group (3)) / 100) * avg
                        results[nThreads][size][region]["avg"] = avg
                        results[nThreads][size][region]["std_dev"] = std_dev


    plot_timeXthread(results)
    plot_timeXinput(results)
