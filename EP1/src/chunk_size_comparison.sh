MEASUREMENTS=50
ITERATIONS=7
SIZE=2048
THREAD_NUM=8
INITIAL_CHUNK_SIZE=$(($SIZE / 2))
CHUNK_SIZE=$INITIAL_CHUNK_SIZE
REGION=('full')
# list of programs to be tested
NAMES=('mandelbrot_pth')

if [ ! -d results ]; then
    mkdir results
fi

make > /dev/null
for NAME in ${NAMES[@]}; do
    mkdir -p results/$NAME
    echo 'Testing implementation: ' ${NAME}
    for ((i=1; i<=$ITERATIONS; i++)); do
        perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $THREAD_NUM $CHUNK_SIZE >> $REGION.log 2>&1
        CHUNK_SIZE=$(($CHUNK_SIZE * 2))
    done

    CHUNK_SIZE=$INITIAL_CHUNK_SIZE
    mv *.log results/$NAME
    rm output.ppm
done
python ./gen_graph/time_by_chunk_size_graphs.py pth full $SIZE
