# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Enchanted Cipher
> The Grand Arcane Codex has been corrupted, altering historical records. Each entry has been encoded with a shifting cipher that changes every N characters. Your task is to decode a given string and restore the original message.

- **Category**: Coding
- **Difficulty**: Very Easy
- **Author**: Massandre

## Summary & Consideration

In this challenge we are given as input the encrypted words, the number of groups and the shifts

## Writeup

The challenge tells us that each group of letters in encrypted with a shifting cipher and the first thing that comes to mind thinking about that type of cypher is rot-13 and we can try to see if it is that cipher by looking at the example: 


```
Input:
ibeqtsl
2
[4, 7]

Output:
example
```

And this pretty much confirms the hypothesis.

So the only thing we have to do is make a script that groups each 5 letters and applies the inverse of rot-13 to it using for the ith group the ith key given in the input and crafting the output making sure each space is in the right position:

```py
import string
input_text = input()
numero=int(input())
listOfShifts=input().strip("[]").split(",")
listOfShifts=[int(x.strip()) for x in listOfShifts]
nShifts=input_text.split("\n")[0]

alph=string.ascii_lowercase
smt=""
string=""
for pos,i in enumerate(nShifts):
    if i == " ":
        continue
    smt+=i
    if len(smt) == 5 or pos == len(nShifts)-1:
        for x in smt:
            string+=alph[(alph.index(x)-listOfShifts[0])%len(alph)]
        smt=""
        listOfShifts.pop(0)
answer=""
pos=0
for i in nShifts:
    if i == " ":
        answer+=i
    else:
        if pos >= len(string):
            break
        answer+=string[pos]
        pos+=1
print(answer)
```

> HTB{3NCH4NT3D_C1PH3R_D3C0D3D_16df0101b1ed86904c3a790cb2d5328e}