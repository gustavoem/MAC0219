#/bin/bash

if [ ! -d results ]; then
	mkdir results
fi

dir_name=results/chunk-$(date +%Y-%m-%d:%H:%M:%S)/
mkdir $dir_name

nTests=10
size=$((2 ** 11))
nThreads=8

echo "Starting tests"
for i in $(seq 0 5); do
	chunkSize=$(((2 ** $i) * $size))
	echo "chunkSize: $chunkSize"

	file=$chunkSize"x2048_chunk.log"

	perf stat -r $nTests ./mandelbrot_pth -2.5 1.5 -2.0 2.0 $size $nThreads $chunkSize 2> $dir_name"full_"$file
	perf stat -r $nTests ./mandelbrot_pth -0.8 -0.7 0.05 0.15 $size $nThreads $chunkSize 2> $dir_name"seahorse_"$file
	perf stat -r $nTests ./mandelbrot_pth 0.175 0.375 -0.1 0.1 $size $nThreads $chunkSize 2> $dir_name"elephant_"$file
	perf stat -r $nTests ./mandelbrot_pth -0.188 -0.012 0.554 0.754 $size $nThreads $chunkSize 2> $dir_name"spiral_"$file
done
