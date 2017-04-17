#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

program = sys.argv[1]
inputs = ["full", "seahorse", "elephant", "triple_spiral"]
legends = [x.title () for x in inputs]
results_dir = "./results/mandelbrot_" + program
results = {}
for input_name in inputs:
    #result[input] = ([x1, x2, ...], [t(x1), t(x2), ...], [sd(x1), ...])
    results[input_name] = ([], [], [])

# Process log files
input_size = 0;
for input_name in inputs:
    result_file = open (results_dir + "/" + input_name + ".log")
    for line in result_file:
        match = re.search ('(\d+(\.|,)\d+)\s+seconds\s+time\s+elapsed\s+\(\s+\+\-\s+(\d+(\.|,)\d+)%\s+\)', line)
        if match:
            avg = float (match.group (1))
            std_dev = (float (match.group (3)) / 100) * avg
            results[input_name][1].append (avg)
            results[input_name][2].append (std_dev)
        match = re.search ('\s+Performance\scounter\sstats\sfor\s+\'\.\/mandelbrot_seq.+\s(\d+)\'.*', line)
        if match:
            input_size = float (match.group (1))
            results[input_name][0].append (input_size)

# Plot data
ax = plt.gca () 
for i, input_name in enumerate (inputs):
    r = results[input_name]
    plt.errorbar (r[0], r[1], yerr = r[2], label = legends[i])
handlers, labels = ax.get_legend_handles_labels ()
handlers = [h[0] for h in handlers]
ax.legend(handlers, labels, loc = 'upper left', numpoints = 1)
plt.xlabel ("Tamanho de instância")
plt.ylabel ("Tempo médio de execução")
plt.title ("Comparação de tempo gasto em diferentes instâncias")
plt.show ()
