#进制转换
while True:
    x, base = eval(input("x,base="))
    while x > 0:
        print(x % base)
        x //= base
