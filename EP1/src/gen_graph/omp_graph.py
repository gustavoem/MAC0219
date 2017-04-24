#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

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
# xlist = []
# ylist = []
# ylist2 = []
# for i in range(0, 6):
#     nThreads = 2 ** i
#     xlist.append(nThreads)
#     ylist.append(results[nThreads][2**13]["full"]["avg"])
#     ylist2.append(results[nThreads][2**13]["elephant"]["avg"])
# plt.plot(xlist, ylist, 'ro', xlist, ylist2, 'bs')
# plt.axis([0, 35, 0, 100])
# plt.show()

NUM_COLORS = 16
fig = plt.figure(figsize=(14, 8))
cm = plt.get_cmap('gist_rainbow')
ax = fig.add_subplot(111)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

xlist = []
ylist = []
ylist2 = []
ylist3 = []
ylist4 = []
ylist5 = []
ylist6 = []
for i in range(4, 14):
    size = 2 ** i
    xlist.append(size)
    ylist.append(results[1][size]["full"]["avg"])
    ylist2.append(results[2][size]["full"]["avg"])
    ylist3.append(results[4][size]["full"]["avg"])
    ylist4.append(results[8][size]["full"]["avg"])
    ylist5.append(results[16][size]["full"]["avg"])
    ylist6.append(results[32][size]["full"]["avg"])
thread1,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist, 'o', mfc='none')
thread2,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist2, 'o', mfc='none')
thread4,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist3, 'o', mfc='none')
thread8,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist4, 'o', mfc='none')
thread16,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist5, 'o', mfc='none')
thread32,zoosazzzasadasdafsafasasdafsasafsdadsfafdsafdsafdsa = plt.plot(xlist, ylist6, 'o', mfc='none')

plt.title('Time of execution X input size')
plt.ylabel('Time (s)')
plt.xlabel('Input size')

my_xticks = ['4','5','6','7', '8', '9', '10', '11', '12', '13' ]
plt.xticks(xlist, my_xticks)

ax.legend([thread1, thread2, thread4, thread8, thread16, thread32], ['1 Threads', '2 Threads', '4 Threads', '8 Threads', '16 Threads', '32 Threads'])

# plt.axis([0, 35, 0, 100])
plt.show()

# # Plot data
# ax = plt () 
# for i, input_name in enumerate (inputs):
#     r = results[input_name]
#     plt.errorbar (r[0], r[1], yerr = r[2], label = legends[i])
# handlers, labels = ax.get_legend_handles_labels ()
# handlers = [h[0] for h in handlers]
# ax.legend(handlers, labels, loc = 'upper left', numpoints = 1)
# plt.xlabel ("Tamanho de instância")
# plt.ylabel ("Tempo médio de execução")
# plt.title ("Comparação de tempo gasto em diferentes instâncias")
# plt.show ()





# legends = [x.title () for x in inputs]

# for input_name in inputs:
#     #result[input] = ([x1, x2, ...], [t(x1), t(x2), ...], [sd(x1), ...])
#     results[input_name] = ([], [], [])

# # Process log files
# input_size = 0;
# for input_name in inputs:
#         match = re.search ('(\d+(\.|,)\d+)\s+seconds\s+time\s+elapsed\s+\(\s+\+\-\s+(\d+(\.|,)\d+)%\s+\)', line)
#         match = re.search ('\s+Performance\scounter\sstats\sfor\s+\'\.\/mandelbrot_seq.+\s(\d+)\'.*', line)
#         if match:
#             input_size = float (match.group (1))
#             results[input_name][0].append (input_size)

# # Plot data
# ax = plt.gca () 
# for i, input_name in enumerate (inputs):
#     r = results[input_name]
#     plt.errorbar (r[0], r[1], yerr = r[2], label = legends[i])
# handlers, labels = ax.get_legend_handles_labels ()
# handlers = [h[0] for h in handlers]
# ax.legend(handlers, labels, loc = 'upper left', numpoints = 1)
# plt.xlabel ("Tamanho de instância")
# plt.ylabel ("Tempo médio de execução")
# plt.title ("Comparação de tempo gasto em diferentes instâncias")
# plt.show ()
