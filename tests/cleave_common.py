import os

def compare(filename, basename, n):
    with open(filename, 'r') as src:
        for i in range(n):
            with open(basename + '{:02}'.format(i), 'r') as dst:
                for line in dst:
                    if line != src.readline():
                        return False
    return True

def remove(basenames, n):
    for basename in basenames:
        for i in range(n):
            os.unlink(basename + '{:02}'.format(i))

