## MinimumSwap

## My brute force approach
- first find the K how many elements are less than or equal to Given integer B, for this use the for loop and iterate over the all the elements which calculates the Time Complexity as O(N)
- declare the start_index as 0 and end_index as K - 1 and min_swap as float('inf') big value variables, 
- then write the while loop with condition end_index < length of the array A which in worst scenario calculates the Time Complexity as O(N - K + 1) (length array - numbers elements less than or equal to B plus 1 (+1 is for the adjust the with index to array length as index starts at 0))
- and then in the while loop declare the variable count_swap_nums as 0
- run the for loop in a range from start to end + 1 (to include the last element), which calculates the Time Complexity as O(K)
- put the if condition with iterated elements are greater than B, and update the count_swap_nums
- update the min_swap if the count_swap_nums less than min_swap 
- update start_index + 1 and end_index + 1
- Final Time Complexity O(N) + ( O(N - K + 1) x O(K) ) = O(N^2)

## My Optimize solution steps:
- eg:; A = [1, 12, 10, 3, 14, 10, 5] , B = 8
- first window [1,12,10] for loop run on this and checks and count 12, 10 greater than B
- second window [12,10,3] for loop run on this and checks and should not count


