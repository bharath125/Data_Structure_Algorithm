## sum of all subarrays

## brute force solution
A=[2,8,1,3]
n=len(A)
total_sum=0

## TC : O(n3) and SC: O(1)

for i in range(n):
    for j in range(i,n):
        subArraySum=0
        for k in range(i,j+1):
            subArraySum+=A[k]
        total_sum+=subArraySum
print(total_sum)













