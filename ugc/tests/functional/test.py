a = list(range(1,1025))

for i in range(1,11):
    num = 0 if i % 2 == 0 else 1
    a = a[num::2]
    print(a[:10])

print(a)