
def specilIndex(A):
 ps_odd_index=[]
        odd_total=0
        for i in range(len(A)):
            if i%2==1:
                odd_total+=A[i]
                ps_odd_index.append(odd_total)
            else:
                ps_odd_index.append(odd_total)
        
        ps_even_index=[]
        even_total=0
        for i in range(len(A)):
            if i%2==0:
                even_total+=A[i]
                ps_even_index.append(even_total)
            else:
                ps_even_index.append(even_total)
        
        count=0
        sum_odd=0
        sum_even=0
        n=len(A)
        
        for i in range(len(A)):
            if i==0:
                sum_odd=ps_even_index[n-1]-ps_even_index[i]
                sum_even=ps_odd_index[n-1]-ps_odd_index[i]
            else:
                sum_odd=ps_odd_index[i-1]+ps_even_index[n-1]-ps_even_index[i]
                sum_even=ps_even_index[i-1]+ps_odd_index[n-1]-ps_odd_index[i]
            if sum_even==sum_odd:
                count+=1
        return count
