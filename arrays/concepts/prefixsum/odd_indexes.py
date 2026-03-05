## find the queries of odd indexed value of prefix sum 




## optimized solution

 prefix_sum_odd_indexes=[]
        total=0
        for i in range(len(A)):
            if i%2==1:
                total+=A[i]
                prefix_sum_odd_indexes.append(total)
            else:
                prefix_sum_odd_indexes.append(total)
            
        # return prefix_sum_odd_indexes
        Q=len(B)
        res=[]
        for i in range(Q):
            L=B[i][0]
            R=B[i][1]
            if L==0:
                res.append(prefix_sum_odd_indexes[R])
            else:
                res.append(prefix_sum_odd_indexes[R]-prefix_sum_odd_indexes[L-1])
        return res
