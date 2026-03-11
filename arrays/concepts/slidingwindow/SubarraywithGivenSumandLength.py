## TC : O(n) SC : O(1)
        n=len(A) 
        window_sum=0
        if n==1 and A[0]==C:
            return 1
            
        for i in range(0,B-1+1):
            window_sum+=A[i]
        
        start=1
        end=B

        while (end<n):
            window_sum=window_sum - A[start-1] + A[end]
            if window_sum==C:
                return 1
            start+=1
            end+=1
        return 0
