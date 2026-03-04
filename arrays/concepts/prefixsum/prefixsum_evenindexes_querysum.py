## prefix sum of even indexes of querysum
A=[2,8,3,9,15] # [2,2,5,5,20]
B=[[1,4],[0,2],[2,3]]

## brute force solution
Q=len(B)
for in in range(Q):
    L=B[i][0]
    R=B[i][1]
    total=0
    for j in range(L,R+1):
        if (j%2==0):
            total+=A[j]
    print(total)





## optimized solution
## first find the prefix sum array at even indexes



prefix_sum=[]
tot=0
for i in range(len(A)):
    if (i%2==0):
        tot+=A[i]
        prefix_sum.append(tot)
    else:
        prefix_sum.append(tot)
print(prefix_sum)

Q=len(B)
res=[]
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


