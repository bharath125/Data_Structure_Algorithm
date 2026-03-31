# Definition for singly-linked list.
# class ListNode:
#    def __init__(self, x):
#        self.val = x
#        self.next = None

class Solution:
    # @param A : head node of linked list
    # @param B : integer
    # @return the head node in the linked list
    def solve(self, A, B):
        # newNode=new ListNode()
        if B==0:
            A=A.next
            return A
        temp=A
        for i in range(B):
            if i==B-1:
                temp.next=temp.next.next
                return A
            temp=temp.next
        return A


            

