# Definition for singly-linked list.
# class ListNode:
#    def __init__(self, x):
#        self.val = x
#        self.next = None

class Solution:
    # @param A : head node of linked list
    def solve(self, A):
        values=[]
        current=A

        while current:
            values.append(str(current.val))
            current=current.next
        
        print(" ".join(values) + " ")
