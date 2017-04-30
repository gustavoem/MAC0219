import sys
import matplotlib.pyplot as plt
from math import sqrt

file_path = sys.argv[1]

f = open(file_path)

dist = []
for line in f:
	dist.append(int(line))

print(len(dist))
xlist = list(range(len(dist)))
plt.figure(figsize=(14, 8))
plt.plot(xlist, dist, "ro", alpha=0.05, ms=2)


plt.ylabel('Iterations')
plt.xlabel('Image vector index')
plt.title('Number of iteractions for image of ' + str(sqrt(len(dist))) + 'px')
plt.show()
