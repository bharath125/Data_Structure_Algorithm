#  Subarray with least average [Amazon, Google]

Problem Description
Given an array A of size N, find the subarray of size B with the least average.

Problem Constraints
1 <= B <= N <= 10^5
-10^5 <= A[i] <= 10^5 


## My brute force solution 
- first, declare the variables named start_index = 0 and end_index = B and min_avg = float('inf') bigger value, min_subarr_index = 0
- using the while loop so easy to find the subarray from start_index to end_index while end <= len(A), it needs to be less than or equal because if the end  = len(A) it should work, last window miss the calculation avg if the least avg is in this window, and the time comeplexity is N - B + 1 in worst case O(N)
- I am finding the subArray = A[start:end]
- then find the average of the subarray avg = sum(subArray)/B as the subarray will B number of elements here the time complexity is O(B)
-  I am using the if conditional statement if the avg < min_avg, update the min_avg=avg and update the min_subarr_index = start (becuase we want the least subarray first elements index)
-  as it is while we need to end the loop instead of running it for infinity times by start_index+=1 and end_index+=1
-  Time Complexity is (N - B + 1) x B (if N==B) ==> O(N^2) and Space Complexity is O(B) as the subArray = A[start:end]

## My Optimizaed solution 
- as I have the O(N^2) Time Complexity eventhough the solution is correct it will throw TLE
- the fix at every window I am calculating the sum of the subarray this repetation we need to reduce
- so for the first window, I will calculate the sum of subarray for the B, but for the second window, from the subarray first element I will subtract and end of the subarray I will end new element
- here is how the the code writing goes like this
- declare variables min_subarr_index = 0 and total=0
- find the first window for the subarray of value B with for loop from 0 to B - 1 




