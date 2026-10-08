import sys

for line in sys.stdin:
    key = line.strip().split()[0]

    if key == "200":
        partition = 0
    else:
        partition = 1

    print(partition)