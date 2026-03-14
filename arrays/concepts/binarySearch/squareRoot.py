## TC : O(logN) SC : O(1)
    def sqrt(self, A):
        L=1
        R=A
        ans=L
        if A==0:
            return A
        while L<=R:
            mid=L+(R-L)//2
            if mid*mid<=A:
                ans=mid
                L=mid + 1
            else:
                R=mid - 1
        return ans
