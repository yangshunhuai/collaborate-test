#韩信点兵: 今有物不知其数，七七数之余二，五五数之余三
#三三数之余二，问物有几何？
'''

n = 0
while True:
    n += 1
    if n % 7 == 2 and n % 5 == 3 and n % 3 == 2:
        print(n)
        break

'''

'''

n = 1001
while True:
    n -= 1
    if n % 7 == 2 and n % 5 == 3 and n % 3 == 2:
        print(n)
        break

'''

'''

n = 1000
个数 = 0
while True:
    n -= 1
    if n % 7 == 2 and n % 5 == 3 and n % 3 == 2:
        个数 += 1
        print(n, 个数)
    if n == 0:
        break

'''

'''

n = 0
个数 = 0
while True:
    n += 1
    if n % 7 == 2 and n % 5 == 3 and n % 3 == 2:
        个数 += 0
        print(n)
    if 个数 == 12:
        break

'''
