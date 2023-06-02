import time

limit = 1000

w_start = time.perf_counter()
i=0
while i<limit:
    print(i)
    i+=1
print(i)
w_end = time.perf_counter()
print(f'Time with prints: {w_end-w_start}')

n_start = time.perf_counter()
i=0
while i<limit:
    i+=1
print(i)
n_end = time.perf_counter()
print(f'Time without prints: {n_end-n_start}')

print(f'With prints is {(w_end-w_start)/(n_end-n_start)*100}% slower')