import random
import sys
random.seed(10)

for _ in range(10):
    print(random.randint(1, 4294967295) % 10 - 5)
