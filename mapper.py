import sys

for line in sys.stdin:
    data = line.strip().split()

    if len(data) >= 4:
        status = data[3]
        print(status, 1)