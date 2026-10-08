import sys

current = None
total = 0

for line in sys.stdin:
    key, value = line.strip().split()

    if current == key:
        total += int(value)
    else:
        if current is not None:
            print(current, total)

        current = key
        total = int(value)

if current is not None:
    print(current, total)