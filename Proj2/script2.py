import os
import subprocess
import sys

alpha = float(sys.argv[1])
gamma = float(sys.argv[2])

print("Attempting with:")
print("alpha:",  alpha)
print("gamma:",  gamma)

max_scores = 0
out = '20'
while out == '20':	
	out = subprocess.check_output(["python3", "other.py", str(alpha), str(gamma)])
	out = out.decode('utf-8').replace('\n', '')
	max_scores += 1

	if max_scores % 25 == 0:
		print(max_scores)
	
print("Attempts until failure:", max_scores)
