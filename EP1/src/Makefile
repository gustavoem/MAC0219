OUTPUT=mandelbrot

IMAGE=.ppm

CC=gcc
CC_OPT=-std=c11 -Wall -Wno-unused-result

CC_OMP=-fopenmp
CC_PTH=-pthread

.PHONY: all
<<<<<<< HEAD
all: $(OUTPUT)_omp $(OUTPUT)_pth $(OUTPUT)_seq $(OUTPUT)_pth_din
=======
all: $(OUTPUT)_omp $(OUTPUT)_pth $(OUTPUT)_seq $(OUTPUT)_pth_sta
>>>>>>> 13604e675ea897dccbaa2ca6f727b0d02120e796

$(OUTPUT)_omp: $(OUTPUT)_omp.c
	$(CC) -o $(OUTPUT)_omp $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp.c

$(OUTPUT)_omp_nd: $(OUTPUT)_omp_nd.c
	$(CC) -o $(OUTPUT)_omp_nd $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp_nd.c

$(OUTPUT)_pth: $(OUTPUT)_pth.c
	$(CC) -o $(OUTPUT)_pth $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth.c

<<<<<<< HEAD
$(OUTPUT)_pth_din: $(OUTPUT)_pth_din.c
	$(CC) -o $(OUTPUT)_pth_din $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth_din.c
=======
$(OUTPUT)_pth_sta: $(OUTPUT)_pth_sta.c
	$(CC) -o $(OUTPUT)_pth_sta $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth_sta.c
>>>>>>> 13604e675ea897dccbaa2ca6f727b0d02120e796

$(OUTPUT)_seq: $(OUTPUT)_seq.c
	$(CC) -o $(OUTPUT)_seq $(CC_OPT) $(OUTPUT)_seq.c

.PHONY: clean
clean:
<<<<<<< HEAD
	rm $(OUTPUT)_omp $(OUTPUT)_omp_nd $(OUTPUT)_pth $(OUTPUT)_seq *$(IMAGE)
=======
	rm $(OUTPUT)_omp $(OUTPUT)_pth_sta $(OUTPUT)_pth $(OUTPUT)_seq *$(IMAGE)
>>>>>>> 13604e675ea897dccbaa2ca6f727b0d02120e796
