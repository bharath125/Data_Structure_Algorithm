## find the prefix sum

## question
## You are given an integer array A of length N.
## You are also given a 2D integer array B with dimensions M x 2, where each row denotes a [L, R] query.
## For each query, you have to find the sum of all elements from L to R indices in A (0 - indexed).
## More formally, find A[L] + A[L + 1] + A[L + 2] +... + A[R - 1] + A[R] for each query.

## Problem contraints
## 1 <= N, M <= 105
## 1 <= A[i] <= 109
## 0 <= L <= R < N




A=[7,3,1,5,5,5,1,2,4,5]
B=[[6,9],[2,9],[2,4],[0,9]]

prefix_sum=[]
pre_sum=0
for i in range(0,len(A)):
    pre_sum=pre_sum+A[i]
    prefix_sum.append(pre_sum)
print(prefix_sum)

Q=len(B)
res=[]

## [ 6,9 ]
## [ 2,9 ]
## [ 2,4 ]
## [ 0,9 ]
##
##
##
##


for i in range(Q):
    # print(i)
    L=B[i][0]
    # print(L)
    R=B[i][1]  
    # print(R)
    total=0
    if(L==0):
        total=prefix_sum[R]
    else:
        total=prefix_sum[R]-prefix_sum[L-1]
    res.append(total)
print(res) 
