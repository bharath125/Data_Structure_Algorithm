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
