# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Dragom Fury
> In the final confrontation, the dragons unleash their fury against Malakar’s forces. Simulate the battle by computing the total damage dealt over successive rounds until victory is achieved.

- **Category**: Coding
- **Difficulty**: Very Easy
- **Author**: Massandre

## Summary & Consideration

In this challenge we are given as input the number each possible value of damage done in every single turn and the target value.

## Writeup

The challenges tells you that you have to find exact combination damage that summed equal exactly the target value and the damage values must be one from every turn.

The solution could be very complicate but the simplest gets the job done so brute forcing every single combination of values gets us the flag


```py
import ast
input_text = input()
target=int(input())

turns = ast.literal_eval(input_text)

sum=0
if len(turns) == 3:
    for i in turns[0]:
        for j in turns[1]:
            for k in turns[2]:
                sum=i+j+k

                if sum == target:
                    array=list()
                    array.append(i)
                    array.append(j)
                    array.append(k)
                    print(array)
                    exit()
elif len(turns) == 4:
    for i in turns[0]:
        for j in turns[1]:
            for k in turns[2]:
                for l in turns[3]:
                    sum=i+j+k+l
                    if sum == target:
                        array=list()
                        array.append(i)
                        array.append(j)
                        array.append(k)
                        array.append(l)
                        print(array)
                        exit()
elif len(turns) == 5:
    for i in turns[0]:
        for j in turns[1]:
            for k in turns[2]:
                for l in turns[3]:
                    for m in turns[4]:
                        sum=i+j+k+l+m
                        if sum == target:
                            array=list()
                            array.append(i)
                            array.append(j)
                            array.append(k)
                            array.append(l)
                            array.append(m)
                            print(array)
                            exit()
elif len(turns) == 6:
    for i in turns[0]:
        for j in turns[1]:
            for k in turns[2]:
                for l in turns[3]:
                    for m in turns[4]:
                        for n in turns[5]:
                            sum=i+j+k+l+m+n
                            if sum == target:
                                array=list()
                                array.append(i)
                                array.append(j)
                                array.append(k)
                                array.append(l)
                                array.append(m)
                                array.append(n)
                                print(array)
                                exit()
```

> HTB{DR4G0NS_FURY_SIM_C0MB0_90450fd047b3b79d7b9b4408e9f8431b}