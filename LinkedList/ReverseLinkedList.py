# Definition for singly-linked list.
# class ListNode:
#	def __init__(self, x):
#		self.val = x
#		self.next = None

class Solution:
	# @param A : head node of linked list
	# @return the head node in the linked list
	def reverseList(self, A):
        prev=None
        curr=A
        if curr.next==None:
            return A
        while(curr!=None):
            nextNode=curr.next
            curr.next=prev
            prev=curr
            curr=nextNode
        A=prev
        return A
