import os
import subprocess
import sys

times = int(sys.argv[1])
scores = [0, 0, 0, 0]

def perc(scores):
	total = sum(scores)
	return [x * 100 / total for x in scores]

for i in range(times):
	out = subprocess.check_output(["python3", "NDruagomesfreiregame2.py"])
	out = int(out.decode('utf-8').replace('\n', ''))

	if out == 13:
		scores[0] += 1
	elif out == 17:
		scores[1] += 1
	elif out == 20:
		scores[2] += 1
	else:
		scores[3] += 1

	print("Completion:", (i + 1) * 100 / times, "%", end="\r")

print("Completion: 100.0 %")	
print("20:", scores[2] * 100 / times, "%")
print("17:", scores[1] * 100 / times, "%")
print("13:", scores[0] * 100 / times, "%")
print("Other scores:", scores[3] * 100 / times, "%")

if scores[2] == times:
	print("\nPerfect score!")
