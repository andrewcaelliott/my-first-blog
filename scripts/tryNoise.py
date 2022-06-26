

f1 = 1024 * [1,0]
f2 = 512 * [1,1,0,0]
f3 = (512 * [1,1,1,0,0,0])[:1024]
f4 = 256 * [1,1,1,1,0,0,0,0]
f8 = 128 * [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
f16 = 64 * [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

zip = zip(f1, f2, f3, f4)
sumeach = [sum(item) % 2 for item in zip]
print(sumeach)

c = 1
run = 0
for i in range(len(sumeach)):
    if sumeach[i] == c:
        run += 1
    else:
        print(c, run)
        c = sumeach[i]
        run =1
