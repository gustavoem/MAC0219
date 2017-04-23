MEASUREMENTS=10
ITERATIONS=7
INITIAL_SIZE=32
THREAD_NUM=4

if [ ! -d results ]; then
    mkdir results
fi

SIZE=$INITIAL_SIZE
NAMES=('mandelbrot_pth' 'mandelbrot_pth_din')

make > /dev/null
for NAME in ${NAMES[@]}; do
    mkdir -p results/$NAME
    echo 'Testing implementation: ' ${NAME}
    for ((i=1; i<=$ITERATIONS; i++)); do
        perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $THREAD_NUM >> full.log 2>&1
        perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $THREAD_NUM >> seahorse.log 2>&1
        perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $THREAD_NUM >> elephant.log 2>&1
        perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $THREAD_NUM >> triple_spiral.log 2>&1
        SIZE=$(($SIZE * 2))
    done

    SIZE=$INITIAL_SIZE

    mv *.log results/$NAME
    rm output.ppm
done
python ./gen_graph/time_by_size_graphs.py pth pth_din full
