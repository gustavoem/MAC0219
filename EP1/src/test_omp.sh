#/bin/bash

if [ ! -d results ]; then
	mkdir results
fi

dir_name=results/omp_results-$(date +%Y-%m-%d:%H:%M:%S)/
mkdir $dir_name

nTests=10

echo "Starting tests"
for i in $(seq 0 5); do
	nThreads=$((2 ** $i))

	# thread_dir=$dir_name$nThreads"-threads/"
	# mkdir thread_dir

	file=$nThreads"threads.log"
	echo "Testing with $nThreads threads"


	for j in $(seq 4 13); do
		size=$((2 ** $j))
		echo "\tsize: $size"

		perf stat -r $nTests ./mandelbrot_omp_nd -2.5 1.5 -2.0 2.0 $size $nThreads 2> $dir_name"full_"$size"px_"$file
		perf stat -r $nTests ./mandelbrot_omp_nd -0.8 -0.7 0.05 0.15 $size $nThreads 2> $dir_name"seahorse_"$size"px_"$file
		perf stat -r $nTests ./mandelbrot_omp_nd 0.175 0.375 -0.1 0.1 $size $nThreads 2> $dir_name"elephant_"$size"px_"$file
		perf stat -r $nTests ./mandelbrot_omp_nd -0.188 -0.012 0.554 0.754 $size $nThreads 2> $dir_name"spiral_"$size"px_"$file
	done
done
