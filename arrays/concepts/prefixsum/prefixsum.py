arr=[2,4,3,1,5]

length=len(arr)

prefix_sum=[]
res=0
# first find the prefix sum meaning
# add the add every element and 
#the sum you got add to new array
for j in range(len(arr)):
    res=res+arr[j]
    prefix_sum.append(res)
# print(prefix_sum)
# prefix_sum=[2,6,9,10,15]


# find the prefix sum at all even indexes
# when you index is divisible by 2 gives remainder zero
# at that index add the sum of prev element and current even index element
prefix_sum[0]=arr[0]
for i in range(1,length):
    if i%2==0:
        prefix_sum[i]=prefix_sum[i-1]+arr[i]
    else:
        prefix_sum[i]=prefix_sum[i-1]
print(prefix_sum)
# prefix_sum=[2,2,5,5,10]
