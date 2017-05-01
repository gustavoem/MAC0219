#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

######## Parsers ##########

def parse_results(results_dir, threads_range, size_range):
    if results_dir[-1] != '/':
        results_dir+='/'

    regions = ["full", "seahorse", "elephant", "spiral"]
    results = {}
    for i in threads_range:
        nThreads = 2 ** i
        results[nThreads] = {}

        for j in size_range:
            size = 2 ** j
            results[nThreads][size] = {}
            file_name = ""

            for region in regions:
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

def parse_parallel_results(results_dir):
    return parse_results(results_dir, range(0, 6), range(4, 14))

def parse_sequential_results(results_dir):
    return parse_results(results_dir, range(0, 1), range(4, 14))                     

############## Plotters #################

class Plotter:
    def __init__(self, implementation = "OpenMP", comment = ""):
        self.fig = plt.figure(figsize=(14, 8))
        self.ax = self.fig.add_subplot(111)
        self.implementation = implementation
        self.comment = comment
        self.reset_colors(12)
        self.init_data_vectors()
    
    def reset(self):
        self.fig = plt.figure(figsize=(14, 8))
        self.ax = self.fig.add_subplot(111)
        self.reset_colors(12)
        self.init_data_vectors()

    def reset_colors(self, nColors):
        self.cm = plt.get_cmap('gist_rainbow')
        self.ax.set_color_cycle([self.cm(1. * i / nColors) for i in range(nColors)])

    def init_data_vectors(self, threads_range=range(0, 6), size_range=range(4, 14)):
        self.threads = [2 ** i for i in threads_range]
        self.sizes = [2 ** i for i in size_range]
        self.regions = ["full", "seahorse", "elephant", "spiral"]

    def save(self, img_name=""):
        self.fig.savefig(img_name, dpi=200)
        self.reset()

    def show(self, img_name=""):
        plt.show()

    def get_timeXsize_lists(self, results, reg):
        ylists = {nThreads: {"avg": [], "std_dev": []} for nThreads in self.threads}

        for size in self.sizes:
            for nThreads in self.threads:
                ylists[nThreads]["avg"].append(results[nThreads][size][reg]["avg"])
                ylists[nThreads]["std_dev"].append(results[nThreads][size][reg]["std_dev"])

        return ylists

    def get_timeXthread_lists(self, results, reg):
        ylists = {size: {"avg": [], "std_dev": []} for size in self.sizes}

        for nThreads in self.threads:
            for size in self.sizes:
                ylists[size]["avg"].append(results[nThreads][size][reg]["avg"])
                ylists[size]["std_dev"].append(results[nThreads][size][reg]["std_dev"])

        return ylists

    def plot(self, xlist, ylist, marker="o", label=""):
        legend, = plt.plot(xlist, ylist["avg"], marker, mew=2, mfc='none', label=label)
        plt.plot(xlist, ylist["avg"], color='0.85', linewidth=0.5)
        self.ax.errorbar(xlist, ylist["avg"], yerr=ylist["std_dev"], ecolor='black', color='0.85', linewidth=0.5)
        return legend

    ##### Plot methods #####

    def timeXsize(self, results, reg):
        self.reset_colors(12)

        ylists = self.get_timeXsize_lists(results, reg)

        legend_handles = []
        legends = []

        for nThreads, ylist in ylists.items():
            th_legend = self.plot(self.sizes, ylist)

            legend_handles.append(th_legend)
            legends.append(str(nThreads) + " Threads")

        self.ax.legend(legend_handles, legends)


        plt.title('Time of execution X input size (' + self.implementation + " - " + reg + self.comment + ")")
        plt.ylabel('Time (s)')
        plt.xlabel('Input size')

        my_xticks = ['$2^{4}$','$2^{5}$','$2^{6}$','$2^{7}$', '$2^{8}$', '$2^{9}$', '$2^{10}$', '$2^{11}$', '$2^{12}$', '$2^{13}$']
        plt.xticks(self.sizes, my_xticks)

        self.show("timeXsize_" + reg + "_" + self.implementation + "png")

    def timeXthread(self, results, reg):
        self.reset_colors(20)

        ylists = self.get_timeXthread_lists(results, reg)

        legend_handles = []
        legends = []

        for size, ylist in ylists.items():
            size_legend = self.plot(self.threads, ylist)

            legend_handles.append(size_legend)
            legends.append(str(size) + " px")

        self.ax.legend(legend_handles, legends)

        plt.title('Time of execution X number of threads (' + self.implementation + " - " + reg + self.comment + ")")
        plt.ylabel('Time (s)')
        plt.xlabel('Number of threads')

        my_xticks = ['$2^{0}$','$2^{1}$','$2^{2}$','$2^{3}$', '$2^{4}$', '$2^{5}$', '$2^{6}$']
        plt.xticks(self.threads, my_xticks)

        self.show("timeXthread_" + reg + "_" + self.implementation + "png")

    def compare_timeXthread(self, results, results2, reg, nColors=10, group1="group 1", group2="group 2"):
        label1 = group1
        label2 = group2

        self.reset_colors(nColors)

        ylists = self.get_timeXthread_lists(results, reg)
        ylists2 = self.get_timeXthread_lists(results2, reg)

        for size, ylist in ylists.items():
            self.plot(self.threads, ylist)

        self.reset_colors(nColors)
        for size, ylist in ylists2.items():
            self.plot(self.threads, ylist, marker="s")


        ### Legends ###
        legends = []
        colors = [self.cm(1. * i / nColors) for i in range(nColors)]
        for ind in range(len(self.sizes)):
            lbl = str(2 ** (ind + 4)) + " px"
            legends.append(mpatches.Patch(color=colors[ind], label=lbl))

        legends.append(mlines.Line2D([], [], marker="o", mfc='none', linestyle="none", color="black", label=label1))
        legends.append(mlines.Line2D([], [], marker="s", mfc='none', linestyle="none", color="black", label=label2))

        plt.legend(handles = legends)

        plt.title('Comparision of time of execution X number of threads (' + self.implementation + " - " + reg + self.comment + ")")
        plt.ylabel('Time (s)')
        plt.xlabel('Number of threads')

        my_xticks = ['$2^{0}$','$2^{1}$','$2^{2}$','$2^{3}$', '$2^{4}$', '$2^{5}$', '$2^{6}$']
        plt.xticks(self.threads, my_xticks)

        self.show("compare_timeXthread_" + reg + "_" + self.implementation + "png")

    def compare_timeXsize(self, results, results2, reg, nColors=10, group1="group 1", group2="group 2"):
        label1 = group1
        label2 = group2

        self.reset_colors(nColors)

        ylists = self.get_timeXsize_lists(results, reg)
        ylists2 = self.get_timeXsize_lists(results2, reg)

        for size, ylist in ylists.items():
            self.plot(self.sizes, ylist)

        self.reset_colors(nColors)
        for size, ylist in ylists2.items():
            self.plot(self.sizes, ylist, marker="s")


        ### Legends ###
        legends = []
        colors = [self.cm(1. * i / nColors) for i in range(nColors)]
        for ind in range(len(self.threads)):
            lbl = str(2 ** ind) + " Threads"
            legends.append(mpatches.Patch(color=colors[ind], label=lbl))

        legends.append(mlines.Line2D([], [], marker="o", mfc='none', linestyle="none", color="black", label=label1))
        legends.append(mlines.Line2D([], [], marker="s", mfc='none', linestyle="none", color="black", label=label2))

        plt.legend(handles = legends)

        plt.title('Comparision of time of execution X size of input (' + self.implementation + " - " + reg + self.comment + ")")
        plt.ylabel('Time (s)')
        plt.xlabel('size of input')


        my_xticks = ['$2^{4}$','$2^{5}$','$2^{6}$','$2^{7}$', '$2^{8}$', '$2^{9}$', '$2^{10}$', '$2^{11}$', '$2^{12}$', '$2^{13}$']
        plt.xticks(self.sizes, my_xticks)

        self.show("compare_timeXsize_" + reg + "_" + self.implementation + "png")


    def all_timeXthread(self, results, nColors=10):
        self.reset_colors(nColors)

        ylists = {}

        for reg in self.regions:
            ylists[reg] = self.get_timeXthread_lists(results, reg) 


        legends = []
        colors = [self.cm(1. * i / nColors) for i in range(nColors)]
        for ind in range(len(self.sizes)):
            lbl = str(2 ** (ind + 4)) + " px"
            legends.append(mpatches.Patch(color=colors[ind], label=lbl))

        markers = ["o", "^", "s", "x"]
        for reg in self.regions:
            marker = markers.pop(0)
            legends.append(mlines.Line2D([], [], marker=marker, mfc='none', linestyle="none", color="black", label=reg))
            self.reset_colors(10)
            for size, ylist in ylists[reg].items():
                self.plot(self.threads, ylist, marker=marker)

        plt.legend(handles = legends)

        plt.title('Time of execution X number of threads (' + self.implementation + " - All regions)")
        plt.ylabel('Time (s)')
        plt.xlabel('Number of threads')

        my_xticks = ['$2^{0}$','$2^{1}$','$2^{2}$','$2^{3}$', '$2^{4}$', '$2^{5}$', '$2^{6}$']
        plt.xticks(self.threads, my_xticks)

        self.show("all_timeXthread" + "_" + self.implementation + "png")

    def all_timeXsize(self, results, nColors=12):
        self.reset_colors(nColors)

        ylists = {}

        for reg in self.regions:
            ylists[reg] = self.get_timeXsize_lists(results, reg) 


        legends = []
        colors = [self.cm(1. * i / nColors) for i in range(nColors)]
        for ind in range(len(self.threads)):
            lbl = str(2 ** ind) + " Threads"
            legends.append(mpatches.Patch(color=colors[ind], label=lbl))

        markers = ["o", "^", "s", "x"]
        for reg in self.regions:
            marker = markers.pop(0)
            legends.append(mlines.Line2D([], [], marker=marker, mfc='none', linestyle="none", color="black", label=reg))
            self.reset_colors(10)
            for size, ylist in ylists[reg].items():
                self.plot(self.sizes, ylist, marker=marker)

        plt.legend(handles = legends)

        plt.title('Time of execution x Input size (' + self.implementation + " - All regions)")
        plt.ylabel('Time (s)')
        plt.xlabel('Input size')

        my_xticks = ['$2^{4}$','$2^{5}$','$2^{6}$','$2^{7}$', '$2^{8}$', '$2^{9}$', '$2^{10}$', '$2^{11}$', '$2^{12}$', '$2^{13}$']
        plt.xticks(self.sizes, my_xticks)

        self.show("all_timeXsize" + "_" + self.implementation + "png")

    #### For sequential test plots ####
    def seq_timeXsize(self, results, reg):
        self.init_data_vectors(threads_range=range(1))
        self.timeXsize(results, reg)


    def compare_seq_timeXsize(self, results, results2, reg):
        self.init_data_vectors(threads_range=range(1))
        self.compare_timeXsize(results, results2, reg, nColors=1)

    def all_seq_timeXsize(self, results, nColors=1):
        self.init_data_vectors(threads_range=range(1))
        self.all_timeXsize(results, nColors=1)
        return

if __name__ == '__main__':
    argv = sys.argv
    plot = Plotter()

    #### sequential ####
    if (sys.argv[1] == '-s'):
        results = parse_sequential_results(argv[2])

        if (len(sys.argv) == 4):
            results2 = parse_sequential_results(argv[3])
            plot.compare_seq_timeXsize(results, results2, "full")
        else:
            plot.all_seq_timeXsize(results, "full")

    #### parallel ####
    else:
        results = parse_parallel_results(sys.argv[1])

        if (len(sys.argv) == 3):
            results2 = parse_parallel_results(argv[2])
            # plot.timeXsize(results, "full")
            # plot.timeXthread(results, "full")
            # plot.all_timeXsize(results)
            # plot.all_timeXthread(results)
            # plot.compare_timeXsize(results, results2, "full", group1="Dynamic1", group2="Static1")
            plot.compare_timeXthread(results, results2, "full", group1="Dynamic1", group2="Static1")
        else:
            plot.timeXthread(results, "full")
            plot.timeXsize(results, "full")
            plot.all_timeXsize(results)

