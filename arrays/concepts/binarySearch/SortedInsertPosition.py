## SortedInsertPosition
 def searchInsert(self, A, B):
        N=len(A)
        L=0   # left
        R=N-1 # right
        while L<=R:
            mid=L+(R-L)//2  ## middle value
 
            if A[mid]==B:
                return mid 
            elif A[mid]<B:
                L=mid+1
            elif A[mid]>B:
                R=mid-1
        
        return L
