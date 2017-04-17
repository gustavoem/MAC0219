#! /bin/bash

set -o xtrace

PROGRAM=$1
ITERATIONS=$2
VALID_PROGRAMS=("seq" "pth" "omp")
if ! echo ${VALID_PROGRAMS[@]} | grep -q -w "$PROGRAM"
then
    echo "Invalid program: $PROGRAM. Exiting..."
    exit
fi
if [[ ! $2 ]]
then
    exit
fi

echo "Comparing different inputs of program\
 mandelbrot_$PROGRAM"

INITIAL_SIZE=16
MEASUREMENTS=10
SIZE=$INITIAL_SIZE
rm results/mandelbrot_$PROGRAM/*
mkdir results/mandelbrot_$PROGRAM
for ((i = 1; i <= $ITERATIONS; i++)); do
    perf stat -r $MEASUREMENTS ./mandelbrot_$PROGRAM -2.5 1.5 -2.0 2.0 $SIZE >> full.log 2>&1
    perf stat -r $MEASUREMENTS ./mandelbrot_$PROGRAM -0.8 -0.7 0.05 0.15 $SIZE >> seahorse.log 2>&1
    perf stat -r $MEASUREMENTS ./mandelbrot_$PROGRAM 0.175 0.375 -0.1 0.1 $SIZE >> elephant.log 2>&1
    perf stat -r $MEASUREMENTS ./mandelbrot_$PROGRAM -0.188 -0.012 0.554 0.754 $SIZE >> triple_spiral.log 2>&1
    SIZE=$(($SIZE * 2))
done

mv *.log results/mandelbrot_$PROGRAM
rm output.ppm

./gen_graph/compare_input_graphs.py $PROGRAM
