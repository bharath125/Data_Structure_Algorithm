# Definition for a  binary tree node
# class TreeNode:
#	def __init__(self, x):
#		self.val = x
#		self.left = None
#		self.right = None

class Solution:
	# @param A : root node of tree
	# @return an integer
	def isBalanced(self, A):
        def height(A):
            if A==None: return 0
            Left=height(A.left)
            if Left==-1: return -1
            Right=height(A.right)
            if Right==-1: return -1
            if abs(Left-Right)>1: return -1
            return max(Left,Right)+1
        return 0 if height(A)==-1 else 1
   
       
