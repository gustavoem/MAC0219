import sys
import matplotlib.pyplot as plt


def parse_results(results_dir):
    if results_dir[-1] != '/':
        results_dir+='/'

    regions = ["full", "seahorse", "elephant", "spiral"]
    results = {}
    for region in regions:
    	results[region] = {}
	    for i in range(5):
	    	mult = 2 ** i
            results[region][mult] = {}

            file_name = region + "_" + str(mult) + "x2048_chunk.log"
            result_file = open (results_dir + file_name)

            for line in result_file:
                match = re.search ('(\d+(\.|,)\d+)\s+seconds\s+time\s+elapsed\s+\(\s+\+\-\s+(\d+(\.|,)\d+)%\s+\)', line)
                if match:
                    avg = float (match.group (1))
                    std_dev = (float (match.group (3)) / 100) * avg
                    results[region][mult]["avg"] = avg
                    results[region][mult]["std_dev"] = std_dev

if __name__ == '__main__':
	results = parse_results(sys.argv[1])
	xlist = [2 ** i for i in range(5)]
	ylist = [results["full"][mult]["avg"] for mult in xlist]
	errlist = [results["full"][mult]["std_dev"] for mult in xlist]

	plt.plot(xlist, ylist)
	plt.errorbar(xlist, errlist)

	# plt.ylabel('Iterations')
	# plt.xlabel('Image vector index')
	# plt.title('Number of iteractions for image of ' + str(sqrt(len(dist))) + 'px')

	plt.xlabel ("Tamanho do chunk (x" + 2 ** 11 + ")")
	plt.ylabel ("Tempo medio de execucao (s)")
	plt.title ("Comparação de tempo gasto na região " + "full" 
	        + " com 2048 pixels" )

	plt.show()
