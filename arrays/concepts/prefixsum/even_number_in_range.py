 Q=len(B)

        even_prefix_sum=[]
        total=0

        for i in range(len(A)):
            if A[i]%2==0:
                total+=1
                even_prefix_sum.append(total)
            else:
                even_prefix_sum.append(total)


        res=[]
        
        for i in range(Q):
            L=B[i][0]
            R=B[i][1]
            tot=0
            if L==0:
                tot=even_prefix_sum[R]
            else:
                tot=even_prefix_sum[R]-even_prefix_sum[L-1]
            res.append(tot)
        return res
