## printing subarray from 0 th index
arr = [1,2,3]
n = len(arr)

for j in range(0, n):
    for k in range(0, j+1): ## why j+1 when i=0, k can be 0 (not 0,1 as range doesn't include last index) ; i=1, k can be 0,1 ; i=2, k can be 0,1,2
        print(arr[k], end=" ") # giving space after the number eg:; 1 2
    print() ## for pring the second loop, it will take it to new line
