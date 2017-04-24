#! /usr/bin/python3

import sys
import re
import matplotlib
# Unset X as default plot window
matplotlib.use ('Agg')
import matplotlib.pyplot as plt
import numpy as np

if (len (sys.argv) < 4):
    print ('Program usage: ' + sys.argv[0] + ' <list of programs>' +
    ' <input region> <input size>')
    sys.exit ()
programs = sys.argv[1:-2]
input_name = sys.argv[-2]
input_size = sys.argv[-1]
legends = programs
results_dir_prefix = "./results/mandelbrot_"
results = {}
for program in programs:
    #result[program] = ([x1, x2, ...], [t(x1), t(x2), ...], [sd(x1), ...])
    results[program] = ([], [], [])

# Process log files
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
        match = re.search ('\s+Performance\scounter\sstats\sfor\s+\'\.\/mandelbrot_.+\s(\d+)\s+(\d+)\s+(\d+)\'.*(\d+)\sruns.*', line)
        if match:
            chunk_size = int (match.group (3)) / int (input_size)
            results[program][0].append (chunk_size)

# Plot data
ax = plt.gca () 
for program_name in programs:
    r = results[program_name]
    plt.errorbar (r[0], r[1], yerr = r[2], label = program_name)
handlers, labels = ax.get_legend_handles_labels ()
handlers = [h[0] for h in handlers]
ax.legend(handlers, labels, loc = 'upper left', numpoints = 1)
plt.xlabel ("Tamanho do chunk (x" + input_size + ")")
plt.ylabel ("Tempo medio de execucao")
plt.title ("Comparacao de tempo gasto na região " + input_name.title () 
        + " com $" + input_size + "^2$ pixels" )
filename = 'time_x_chunk_size' + '-'.join (programs)
plt.savefig(filename + '.png')
