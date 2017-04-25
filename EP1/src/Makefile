OUTPUT=mandelbrot

IMAGE=.ppm

CC=gcc
CC_OPT=-std=c11 -Wall -Wno-unused-result

CC_OMP=-fopenmp
CC_PTH=-pthread

.PHONY: all
all: $(OUTPUT)_omp $(OUTPUT)_pth $(OUTPUT)_seq $(OUTPUT)_seq_s $(OUTPUT)_pth_sta

$(OUTPUT)_omp: $(OUTPUT)_omp.c
	$(CC) -o $(OUTPUT)_omp $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp.c

$(OUTPUT)_omp_nd: $(OUTPUT)_omp_nd.c
	$(CC) -o $(OUTPUT)_omp_nd $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp_nd.c

$(OUTPUT)_pth: $(OUTPUT)_pth.c
	$(CC) -o $(OUTPUT)_pth $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth.c

$(OUTPUT)_pth_sta: $(OUTPUT)_pth_sta.c
	$(CC) -o $(OUTPUT)_pth_sta $(CC_OPT) $(CC_PTH) $(OUTPUT)_pth_sta.c

$(OUTPUT)_seq: $(OUTPUT)_seq.c
	$(CC) -o $(OUTPUT)_seq $(CC_OPT) $(OUTPUT)_seq.c

$(OUTPUT)_seq_s: $(OUTPUT)_seq_s.c
	$(CC) -o $(OUTPUT)_seq_s $(CC_OPT) $(OUTPUT)_seq_s.c

.PHONY: clean
clean:
	rm $(OUTPUT)_omp $(OUTPUT)_omp_nd $(OUTPUT)_pth $(OUTPUT)_pth_sta $(OUTPUT)_seq $(OUTPUT)_seq_s *$(IMAGE)
