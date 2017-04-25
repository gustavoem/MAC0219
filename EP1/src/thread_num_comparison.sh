MEASUREMENTS=10
ITERATIONS=5
SIZE=2048
INITIAL_THREAD_NUM=4

if [ ! -d results ]; then
    mkdir results
fi

THREAD_NUM=$INITIAL_THREAD_NUM
# list of programs to be tested
NAMES=('mandelbrot_pth')
REGION=('full')

make > /dev/null
for NAME in ${NAMES[@]}; do
    mkdir -p results/$NAME
    echo 'Testing implementation: ' ${NAME}
    for ((i=1; i<=$ITERATIONS; i++)); do
        perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $THREAD_NUM >> $REGION.log 2>&1
        THREAD_NUM=$(($THREAD_NUM * 2))
    done

    THREAD_NUM=$INITIAL_THREAD_NUM
    mv *.log results/$NAME
    rm output.ppm
done
python ./gen_graph/time_by_thread_num_graphs.py pth full $SIZE
