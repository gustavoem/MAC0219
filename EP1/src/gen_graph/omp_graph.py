#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
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
    yerr = [[] for _ in range(0, 6)]
    for i in range(4, 14):
        size = 2 ** i
        xlist.append(size)
        for j in range(0, 6):
            nThreads = 2 ** j
            ylists[j].append(results[nThreads][size][reg]["avg"])
            yerr[j].append(results[nThreads][size][reg]["std_dev"])

    legend_handles = []
    legends = []
    for i, ylist in enumerate(ylists):
        nThreads = 2 ** i
        threads, = plt.plot(xlist, ylist, 'o', mfc='none', mew=2)
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        legend_handles.append(threads)
        legends.append(str(nThreads) + " Threads")
    ax.legend(legend_handles, legends)

    for i, err in enumerate(yerr):
        plt.errorbar(xlist, ylists[i], yerr = err, color = '0.85', ecolor="black", linewidth=0.5)
    ax.legend(legend_handles, legends)

    plt.title('Time of execution X input size (OpenMP)')
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
    yerr = [[] for _ in range(4, 14)]

    for i in range(0, 6):
        nThreads = 2 ** i
        xlist.append(nThreads)
        for j in range (4, 14):
            size = 2 ** j
            ylists[j - 4].append(results[nThreads][size][reg]["avg"])
            yerr[j - 4].append(results[nThreads][size][reg]["std_dev"])

    legend_handles = []
    legends = []
    for i, ylist in enumerate(ylists):
        size = 2 ** (i + 4)
        sizex, = plt.plot(xlist, ylist, 'o', mfc='none', mew=2)
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        legend_handles.append(sizex)
        legends.append(str(size) + " px")

    for i, err in enumerate(yerr):
        plt.errorbar(xlist, ylists[i], yerr = err, color = '0.85', ecolor="black", linewidth=0.5)
    ax.legend(legend_handles, legends)

    plt.title('Time of execution X number of threads (OpenMP)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of threads')
    # ax.yaxis.grid(True)

    my_xticks = ['$2^{0}$','$2^{1}$','$2^{2}$','$2^{3}$', '$2^{4}$', '$2^{5}$']
    plt.xticks(xlist, my_xticks)

    plt.show()

def get_results(results_dir):
    if results_dir[-1] != '/':
        results_dir+='/'

    inputs = ["full", "seahorse", "elephant", "spiral"]
    results = {}
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

    return results

def plot_compare_timeXthread(results, results2):
    reg = "full"
    NUM_COLORS = 10
    fig = plt.figure(figsize=(14, 8))
    cm = plt.get_cmap('gist_rainbow')
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

    xlist = []
    ylists = [[] for _ in range(4, 14)]
    ylists2 = [[] for _ in range(4, 14)]
    for i in range(0, 6):
        nThreads = 2 ** i
        xlist.append(nThreads)
        for j in range (4, 14):
            size = 2 ** j
            ylists[j - 4].append(results[nThreads][size][reg]["avg"])
            ylists2[j - 4].append(results2[nThreads][size][reg]["avg"])

    legend_handles = []
    legends = []
    for i, ylist in enumerate(ylists):
        size = 2 ** (i + 4)
        sizex, = plt.plot(xlist, ylist, 'o', mfc='none')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        legend_handles.append(sizex)
        legends.append(str(size) + " px")

    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for i, ylist in enumerate(ylists2):
        size = 2 ** (i + 4)
        plt.plot(xlist, ylist, 's', mfc='none')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
    ax.legend(legend_handles, legends)

    plt.title('Time of execution X number of threads')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of threads')
    # ax.yaxis.grid(True)
    plt.show()

def plot_all_timeXthread(results):
    reg = "full"
    NUM_COLORS = 10
    fig = plt.figure(figsize=(14, 8))
    cm = plt.get_cmap('gist_rainbow')
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

    xlist = []
    ylists = [[] for _ in range(4, 14)]
    ylists2 = [[] for _ in range(4, 14)]
    ylists3 = [[] for _ in range(4, 14)]
    ylists4 = [[] for _ in range(4, 14)]
    for i in range(0, 6):
        nThreads = 2 ** i
        xlist.append(nThreads)
        for j in range (4, 14):
            size = 2 ** j
            ylists[j - 4].append(results[nThreads][size]["full"]["avg"])
            ylists2[j - 4].append(results[nThreads][size]["elephant"]["avg"])
            ylists3[j - 4].append(results[nThreads][size]["seahorse"]["avg"])
            ylists4[j - 4].append(results[nThreads][size]["spiral"]["avg"])

    legend_handles = []
    legends = []
    bola_handle = ''
    for i, ylist in enumerate(ylists):
        size = 2 ** (i + 4)
        bola_handle, = plt.plot(xlist, ylist, 'o', mfc='none', label='Full')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)
        # legend_handles.append(sizex)
        # legends.append(str(size) + " px")

    square_handle = ''
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for i, ylist in enumerate(ylists2):
        size = 2 ** (i + 4)
        square_handle, = plt.plot(xlist, ylist, 's', mfc='none', label='Elephant')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)

    triangle_handle = ''
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for i, ylist in enumerate(ylists3):
        size = 2 ** (i + 4)
        triangle_handle, = plt.plot(xlist, ylist, '^', mfc='none', label='Seahorse')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)

    x_handle = ''
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for i, ylist in enumerate(ylists4):
        size = 2 ** (i + 4)
        x_handle, = plt.plot(xlist, ylist, 'x', mfc='none', label='spiral')
        plt.plot(xlist, ylist, color='0.85', linewidth=0.5)        

    legends = []
    for ind, c in enumerate([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]):
        lbl = str(2 ** (ind + 4)) + " px"
        legends.append(mpatches.Patch(color=c, label=lbl))
    my_bola = mlines.Line2D([], [], color='blue', marker='*',
                          markersize=15, label='Blue stars')
    my_bola.update_from(bola_handle)
    my_bola.set_color('black')
    my_square = mlines.Line2D([], [], color='blue', marker='*',
                          markersize=15, label='Blue stars')
    my_square.update_from(square_handle)
    my_square.set_color('black')
    my_triangle = mlines.Line2D([], [], color='blue', marker='*',
                          markersize=15, label='Blue stars')
    my_triangle.update_from(triangle_handle)
    my_triangle.set_color('black')
    my_x = mlines.Line2D([], [], color='blue', marker='*',
                          markersize=15, label='Blue stars')
    my_x.update_from(x_handle)
    my_x.set_color('black')
    legends += [my_bola, my_square, my_triangle, my_x]
    plt.legend(handles=legends)




    plt.title('Time of execution X number of threads')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of threads')
    # ax.yaxis.grid(True)
    plt.show()

if __name__ == '__main__':
    results_dir = sys.argv[1]
    if results_dir[-1] != '/':
        results_dir+='/'
    results = get_results(results_dir)
        

    results_dir2 = ""
    results2 = {}
    if (len(sys.argv) == 3):
        results_dir2 = sys.argv[2]
        if results_dir2[-1] != '/':
            results_dir2+='/'
        results2 = get_results(results_dir2)

        plot_compare_timeXthread(results, results2)

    else:
        # plot_timeXthread(results)
        plot_timeXinput(results)
        # plot_all_timeXthread(results)
