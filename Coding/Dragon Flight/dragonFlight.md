# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Dragom Flight
> In the mystical realm of the Floating Isles, dragons soar between ancient sanctuaries. However, unpredictable wind conditions can either boost or hinder their journeys.

- **Category**: Coding
- **Difficulty**: Very Easy
- **Author**: Massandre

## Summary & Consideration

In this challenge we are given as input the number of segments and operations, the initial wind effects and then the operations.

## Writeup

The challenges tells you that you have to process the operations, the U type just change the list of wind effects and does not produce an output and the Q type that in this case produces an output that is the maximum contiguous subarray sum between 2 positions in the wind effects list.

Once acquired and parsed the first two lines of input:


```py
input1 = input()
input2 = input()

segments=int(input1.split(" ")[0])
nOperations=int(input1.split(" ")[1])
wind=[int(x) for x in input2.split(" ")]
```

We have to input every operation and execute it as said:

```py
for _ in range(nOperations):
    query=input()
    if query.startswith("U"):
        pos=int(query.split(" ")[1])-1
        val=int(query.split(" ")[2])
        wind[pos]=val
    else:
        startPos=int(query.split(" ")[1])-1
        endPos=int(query.split(" ")[2])

        max=-1000000000 #I initialized the max to a value impossible to reach from the array
        array=wind[startPos:endPos]
        for i in range(len(array)):
            sum=0
            for j in range(i,len(array)):
                sum+=array[j]
                if sum > max:
                    max=sum
        
        print(max)
```

Also notice that every index is given as 1-indexed.

All the program:

```py
input1 = input()
input2 = input()

segments=int(input1.split(" ")[0])
nOperations=int(input1.split(" ")[1])
wind=[int(x) for x in input2.split(" ")]

for _ in range(nOperations):
    query=input()
    if query.startswith("U"):
        pos=int(query.split(" ")[1])-1
        val=int(query.split(" ")[2])
        wind[pos]=val
    else:
        startPos=int(query.split(" ")[1])-1
        endPos=int(query.split(" ")[2])

        max=-1000000000 #I initialized the max to a value impossible to reach from the array
        array=wind[startPos:endPos]
        for i in range(len(array)):
            sum=0
            for j in range(i,len(array)):
                sum+=array[j]
                if sum > max:
                    max=sum
        
        print(max)
```

> HTB{DR4G0N_FL1GHT_5TR33_62ef716a5cfd043c729c8a1426c3fc4e}