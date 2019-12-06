import os
import subprocess
import sys

max_scores = 0
out = '20'
while out == '20':	
	out = subprocess.check_output(["python3", "other.py"])
	out = out.decode('utf-8').replace('\n', '')
	if out == '20':
		max_scores += 1
		print("# Successful attempts =", max_scores, end='\r')

print("Failed! Last attempt returned", out)
print("# Successful attempts =", max_scores)
