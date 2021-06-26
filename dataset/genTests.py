#!/usr/bin/env python3

from array import array
import random
import time
import sys

CASES = [
    # test number, number of operations, operation chances
    [1, 100,        [0.4, 0.3, 0.3, 0, 0]],
    [2, 1_000,      [0.3, 0.3, 0.3, 0.05, 0.05]],
    [3, 10_000,     [0.3, 0.3, 0.3, 0.05, 0.05]],
    [4, 100_000,    [0.3, 0.3, 0.3, 0.05, 0.05]],
    [5, 50_000,     [0.59, 0.4, 0.0, 0.005, 0.005]],  # performence check - balance tree must be quicker
]

"""
Input:  On first line is number of operations. On next N lines contain individual operations.

Operations (key and value are same):
0 <key> - insert
1 <key> - find/contains
2 <key> - delete
3 - print sequence in increasing order
4 - print sequence in decreasing order
"""

random.seed(42)


def insert(key):
    global arr
    for i in range(len(arr)):
        if arr[i] == key:
            return
        if arr[i] > key:
            arr.insert(i, key)
            return
    arr.append(key)


def delete(key):
    global arr
    arr.remove(key)


def contains(key):
    global arr, fout
    try:
        arr.index(key)
        fout.write(f"1\n")
    except Exception:
        fout.write(f"0\n")


def printAll(increasing=True):
    global arr, fin, fout
    if increasing:
        fin.write(f"3\n")
        fout.write(f"{' '.join(str(x) for x in arr)}\n")
    else:
        fin.write(f"4\n")
        arr.reverse()
        fout.write(f"{' '.join(str(x) for x in arr)}\n")
        arr.reverse()


def log(str):
    print(str, file=sys.stderr)


start = time.time()

for case in CASES:
    test_num, num_op, chances = case
    keys = []
    arr = []

    log(f"Generating test case {test_num}")
    with open(f"test{test_num}.in", "w") as fin, open(f"test{test_num}.out", "w") as fout:
        fin.write(f"{num_op + 2}\n")

        operation_now = 0
        while operation_now < num_op:
            chance = random.random()
            prev_chance = 0
            operation = 0
            for c in chances:
                if prev_chance + c > chance:
                    break
                else:
                    prev_chance += c
                    operation += 1

            if operation == 0:
                key = random.randint(0, num_op*2)
                if key in keys:
                    continue

                keys.append(key)
                insert(key)
                fin.write(f"{operation} {key}\n")
            elif operation == 1:
                idx_key = random.randint(0, len(keys))
                if idx_key == len(keys):
                    key = random.randint(0, num_op*2)
                else:
                    key = keys[idx_key]
                fin.write(f"{operation} {key}\n")
                contains(key)
            elif operation == 2:
                if len(keys) == 0:
                    continue
                key = keys[random.randint(0, len(keys) - 1)]
                keys.remove(key)
                fin.write(f"{operation} {key}\n")
                delete(key)
            elif operation == 3:
                printAll(True)
            else:
                printAll(False)
            operation_now += 1
        # Final check
        printAll(True)
        printAll(False)

end = time.time()
log(f"Generating tests took {end - start} s")
