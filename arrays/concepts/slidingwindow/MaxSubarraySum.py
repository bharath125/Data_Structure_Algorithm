## brute force solution
A=[-3,4,-2,5,3,-2,8,2,-1,4]
K=5

n=len(A)
ans=float('-inf')
s=0 ## start index
e=K-1 ##end index

## TC : O ((n-k+1)*k)
## SC : O(1)

while (e<n): ## TC : O((n-k)+1 )
    subarraysum=0
    for i in range(s,e+1): ## TC : O(k)
        subarraysum+=A[i]
    ans=max(subarraysum,ans)
    s+=1
    e+=1
print(ans)

## optimization using the prefix sum
## TC : O(n) SC: O(n)
n=len(A)
ans=float('-inf')
s=0 ## start index
e=K-1 ##end index

pf_sum=[]
total=0
for i in range(n):  ## TC : O(n)
    total+=A[i]
    pf_sum.append(total)

while (e<n): ## TC : O((n-k)+1 )
    subarraysum=0
    if s==0:
        subarraysum=pf_sum[e]
    else:
        subarraysum=pf_sum[e] - pf_sum[s-1]
    ans=max(subarraysum,ans)
    s+=1
    e+=1
print(ans)



## can we optimize more ??
## If the expectation is TC : O(n) SC : O(1)
## we can do with the sliding window approach


n=len(A)
ans=float('-inf')
subarraysum=0
## first window
for i in range(0,K-1+1):
    subarraysum+=A[i]
    
s=1 ## start index staring from 2nd window
e=K ##end index from 2nd window



while (e<n):
    subarraysum=subarraysum-A[s-1]+A[e] ## formula for sliding window sum-A[s-1]+A[e]
    ans=max(subarraysum,ans)
    s+=1
    e+=1
print(ans)


















