#! /usr/bin/python3

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

if (len (sys.argv) < 3):
    print ('Program usage: ' + sys.argv[0] + ' <list of programs>' +
    ' <input region>')
    sys.exit ()
programs = sys.argv[1:-1]
input_name = sys.argv[-1]
legends = programs
results_dir_prefix = "./results/mandelbrot_"
results = {}
for program in programs:
    #result[program] = ([x1, x2, ...], [t(x1), t(x2), ...], [sd(x1), ...])
    results[program] = ([], [], [])

# Process log files
input_size = 0
for program in programs:
    result_file = open (results_dir_prefix + program + "/" +
            input_name + ".log")
    for line in result_file:
        match = re.search ('(\d+(\.|,)\d+)\s+seconds\s+time\s+elapsed\s+\(\s+\+\-\s+(\d+(\.|,)\d+)%\s+\)', line)
        if match:
            avg = float (match.group (1))
            std_dev = (float (match.group (3)) / 100) * avg
            results[program][1].append (avg)
            results[program][2].append (std_dev)
        match = re.search ('\s+Performance\scounter\sstats\sfor\s+\'\.\/mandelbrot_.+\s(\d+)\s+(\d+)\'.*(\d+)\sruns.*', line)
        if match:
            input_size = float (match.group (1))
            results[program][0].append (input_size)

# Plot data
ax = plt.gca () 
for program_name in programs:
    r = results[program_name]
    plt.errorbar (r[0], r[1], yerr = r[2], label = program_name)
handlers, labels = ax.get_legend_handles_labels ()
handlers = [h[0] for h in handlers]
ax.legend(handlers, labels, loc = 'upper left', numpoints = 1)
plt.xlabel ("Tamanho de instância")
plt.ylabel ("Tempo médio de execução")
plt.title ("Comparação de tempo gasto em diferentes programas na " +
    "região " + input_name.title ())
filename = 'time_x_size' + '-'.join (programs)
plt.savefig(filename + '.png')
