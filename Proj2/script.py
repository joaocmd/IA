import os
import subprocess
import threading
import sys
from filelock import FileLock

def run_program(alpha, gamma, f):
	results = []
	for i in range(int(sys.argv[2])):
		out = subprocess.check_output(["python3", "other.py", str(alpha), str(gamma)])
		results.append(out.decode('utf-8').replace('\n', ''))
	lock = FileLock("results.lock")
	with lock:
		f.write(f"{str(alpha).replace('.', ',')};{str(gamma).replace('.', ',')}")
		for r in results:
			f.write(f";{r}")
		f.write(f"\n")

f = open("results.csv", "w+")
step = float(sys.argv[1])
alpha = 0
gamma = 0

threads = []
n_threads = int(sys.argv[3])
while True:
	for i in range(n_threads):
		if gamma > 1:
			alpha += step
			gamma = 0
		if alpha > 1:
			break
		thread = threading.Thread(target=run_program, args=(alpha, gamma, f))
		thread.start()
		threads.append(thread)
		gamma += step

	for index, thread in enumerate(threads):
		thread.join()
	if alpha > 1:
		f.close()
		break