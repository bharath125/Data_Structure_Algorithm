# Definition for singly-linked list.
# class ListNode:
#    def __init__(self, x):
#        self.val = x
#        self.next = None

class Solution:
    # @param A : head node of linked list
    # @param B : integer
    # @param C : integer
    # @return the head node in the linked list
    def solve(self, A, B, C):
        newNode=ListNode(B)
        if A is None:
            return newNode
        if C==0:
            newNode.next=A
            head=newNode
            return head
        temp=A
        for i in range(0,C-1):
            if temp.next==None:
                break
            temp=temp.next
        if temp==None:
            return A
        newNode.next=temp.next
        temp.next=newNode
        return A

