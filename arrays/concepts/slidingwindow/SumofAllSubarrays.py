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

## can we optime above to O(n2)

## prefx_sum optimization
## TC : O(n2) SC:O(n)
prefix_sum=[]
total=0
for i in range(n):
    total+=A[i]
    prefix_sum.append(total)
    
print(pf_sum)
total_sum=0
for i in range(n):
    for j in range(i,n):
        subArraySum=0
        if i==0:
            subArraySum=prefix_sum[j]
        else:
            subArraySum=prefix_sum[j]-prefix_sum[i-1]
        total_sum+=subArraySum
print(total_sum)

## as this quesiton asked in Google and Facebok interviews
## challenge is solve it in TC :O(n) and SC : O(1)

## for the array possible subarrays are 
## 2, 2 8, 2 8 1, 2 8 1 3
## 8, 8 1, 8 1 3
## 1, 1 3
## 3
## observation 2 x 4 times + 8 x 6 times + 1 x 6 times + 3 x 4 times
## we know the what are A[0], A[1], A[2] and A[3]
## but we don't know the occurances of each elements
## How to find the number of occurenaces at each index ??
## I came up with formula (i+1)x(n-i)













