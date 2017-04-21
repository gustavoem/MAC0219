#/bin/bash


dir_name=omp_results-$(date +%Y-%m-%d:%H:%M:%S)/
nTests=10

echo "Starting tests"
for i in $(seq 1 16); do
	file=$($i)threads.log
	echo "Testing with $i threads"
	perf stat -r $nTests ./mandelbrot_omp -2.5 1.5 -2.0 2.0 11500 $i 2> $dir_name$"full_"$file
	perf stat -r $nTests ./mandelbrot_omp -0.8 -0.7 0.05 0.15 11500 $i 2> $dir_name"seahorse_"$file
	perf stat -r $nTests ./mandelbrot_omp 0.175 0.375 -0.1 0.1 11500 $i 2> $dir_name"elephant_"$file
	perf stat -r $nTests ./mandelbrot_omp -0.188 -0.012 0.554 0.754 11500 $i 2> $dir_name"spiral_"$file
done
