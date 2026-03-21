    def solve(A):
        N=len(A)
       
        if N==1: return A[0]
        elif A[0]>=A[1]: return A[0]
        elif A[N-1]>=A[N-2]: return A[N-1]

        
        L=1
        R=N-2

        while L<=R:
            mid=L+(R-L)//2
            if A[mid]>=A[mid-1] and A[mid]>=A[mid+1]:
                return A[mid]
            elif A[mid+1]>=A[mid]:
                L=mid+1
            else:
                R=mid-1
                
        return -1
