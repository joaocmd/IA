import os
import subprocess
import threading
import sys

def run_program(alpha, gamma, f):
	out = subprocess.check_output(["python3", "other.py", str(alpha), str(gamma)])
	f.write(f"{alpha},{gamma},{out.decode('utf-8')}")

f = open("results.csv", "w+")
step = float(sys.argv[1])
alpha = 0
gamma = 0

threads = []
while True:
	for i in range(8):
		if (gamma > 1):
			alpha += step
			gamma = 0
		if (alpha > 1):
			f.close()
			exit()
		thread = threading.Thread(target=run_program, args=(alpha, gamma, f))
		thread.start()
		threads.append(thread)
		gamma += step

	for index, thread in enumerate(threads):
		thread.join()