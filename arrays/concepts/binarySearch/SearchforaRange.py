## TC : O(log2N) and SC : O(10
def searchRange(self, A, B):
        N=len(A)
        L=0
        R=N-1

        first_occ=-1
        while L<=R:
            mid=L+(R-L)//2
            if A[mid]==B:
                first_occ=mid
                R=mid-1
            elif A[mid]<B:
                L=mid+1
            else:
                R=mid-1
        Lo=0
        Ro=N-1
        sec_occ=-1
        while Lo<=Ro:
            mid=Lo+(Ro-Lo)//2
            if A[mid]==B:
                sec_occ=mid
                Lo=mid+1
            elif A[mid]<B:
                Lo=mid+1
            else:
                Ro=mid-1
           
        return [first_occ,sec_occ]
