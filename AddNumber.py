import random

print('Hello World')

randomStop = random.randint(1, 5000)
for i in range(10000):
    if randomStop == i:
        break
    print(i)


print(i)