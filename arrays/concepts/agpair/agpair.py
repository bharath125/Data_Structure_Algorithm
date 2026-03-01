## brute force solution
string='acbagkagg'
length=len(string)

pair_count=0
for i in range(length):
  if (string[i]=='a'):
    for j in range(i+1,length):
      if (string[j]=='g'):
        pair_count+=1
print(pair_count)


## optimized solution TC:O(n) SC:O(1)
string='acbagkagg'
length=len(string)

pair_count=0
count_a=0
for i in range(length):
    if (string[i]=='a'):
        count_a+=1
    elif (string[i]=='g'):
        pair_count+=count_a
print(pair_count)
        
