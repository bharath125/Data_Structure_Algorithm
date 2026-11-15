# MinimumSwap. [Intuit, Thoughtworks, EPAM Systems]

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
- second window [12,10,3] for loop run on this and checks and should not count the 12,10 as they were already counted
- here is the solution that I optimised to solve
- with the for loop, loop over the array A, and calculate number of elements which are good elements
- first early return scenarios, in this there are if the array length is 1 return 0 or length of array and equal to K return 0
- first window, initialize variable count_swap as 0, with for loop, loop over the array from index 0 to index K - 1 is our first window and update the count_swap if the element is less or equal to B.
- Next intilize the start_index = 1, end_index = K, and min_swap=count_swap (Why because we already got the one possible min sum in the first window)
- write the while loop if end < len(A), and here is the amazing part I will not use the for loop inside this while loop,
-  I already calcuate the all the elements in first window, I will not calculate again, i will remove 0th index (start_index - 1) element and add the Kth index (end_index) element
-  here is the important distinction, we are removing the start_index - 1 as we already calculated if this element is > B count_swap - 1 if the adding element end_index is > B count_swap + 1 why??, because we never calculated the end_index, so adding to count_swap
-  same as before if the count_swap < min_swap update the min_swap=count_swap, as we need the minimum number of swaps
-  and very import step increment start_index and end_index with 1, at each window iteration
-  so return the min_swap finally

## FINAL solution in explanatory words
1. Count good elements: First, count all elements <= B. Let this count be K.

2. Determine window size: Since we need all K good elements together, we need a contiguous window of exactly K positions.

3. Count unwanted elements: For each window of size K, count elements > B. These elements occupy positions that should contain good elements.

4. Calculate swaps: Every unwanted element inside the window can be swapped with one good element outside the window. Therefore, the number of unwanted elements equals the swaps needed for that window.

5. Find the minimum: Check every possible window and choose the one with the fewest unwanted elements.
6. There for Minimum Swap = min(unwanted elements in every K - sized window)



