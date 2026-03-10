## Max subarray Not exceeding B
A = 5
B = 12
C = [2, 1, 3, 4, 5]

        pf_sum=[]
        tot=0
        for i in range(A):
            tot+=C[i]
            pf_sum.append(tot)
        res=0 
        for i in range(A):
            for j in range(i,A):
                subarraysum=0
                if i==0:
                    subarraysum=pf_sum[j]
                else:
                    subarraysum=pf_sum[j] - pf_sum[i-1]
                if subarraysum<=B:
                    res=max(res,subarraysum)
                
        return res
