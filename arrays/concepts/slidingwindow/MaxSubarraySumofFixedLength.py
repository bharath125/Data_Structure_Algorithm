        n=len(A)
        if n==1:
            return A[0]
        window_sum=0
        ## first window
        for i in range(B-1+1):
            window_sum+=A[i]
        
        start=1
        end=B

        ans=window_sum

        while (end<n):
            window_sum=window_sum - A[start - 1] + A[end]
            ans=max(window_sum,ans)
            start+=1
            end+=1
        return ans
