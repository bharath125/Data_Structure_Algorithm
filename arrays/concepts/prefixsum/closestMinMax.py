## closest MinMax problem 

## brute force solution
## 1. go to all subarray 
## 2. check if has max and min if yes updating ans
low=min(A)  ## TC O(n) and SC O(1)
high=max(A)   ## TC O(n) and SC O(1)
ans=float('inf')
for i in range(len(A)):  ## TC O(n^2) and SC O(1)
  for j in range(1,len(A)):
      if low and high in A[i:j+1]:
        size=len(A[i:j+1])
        ans=min(ans,size)
    # for k in range(i,j+1):
      ##check it size 
      
        


## Optimized solution
        low=min(A)
        high=max(A)


        min_index=-1
        max_index=-1
        ans=float('inf')

        for i in range(len(A)):  ## TC O(n) and SC O(1)
            if A[i]==low:
                min_index=i
            if A[i]==high:
                max_index=i
            if min_index!=-1 and max_index!=-1:
                ## as index starts from 0 to make calc size we need to add 1
                size=abs(max_index-min_index)+1  ##  ## TC O(1) and SC O(1)
                ans=min(ans,size)
        if min_index==max_index:
            return 1
        return ans
