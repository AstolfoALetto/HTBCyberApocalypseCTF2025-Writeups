# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Kewiri
> The Grand Scholars of Eldoria have prepared a series of trials, each testing the depth of your understanding of the ancient mathematical arts. Those who answer wisely shall be granted insight, while the unworthy shall be cast into the void of ignorance. Will you rise to the challenge, or will your mind falter under the weight of forgotten knowledge?  


- **Category**: Crypto
- **Difficulty**: Very Easy
- **Author**: Alexct549

## Summary & Consideration

This challenge is essentially an Elliptic Curves 101, so I'll make it as beginner-friendly as possible to ensure that everyone can learn something (just like I did with this challenge! 😉)

⚠️ This challenges the way I did it requires multiple files and sage

## Writeup

So the only thing we get it's a docker instance so let's try and see what it gives us


```bash
[!] The ancient texts are being prepared...

You have entered the Grand Archives of Eldoria! The scholars shall test your wisdom. Answer their questions to prove your worth and claim the hidden knowledge.
You are given the sacred prime: p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
[1] How many bits is the prime p? > 
```

Well well well we got a a big prime here (fun fact: it seems it's generation is not linked to the docker instance but to the player/team who requests it) and we got our first question as well!!
Let's dive together in this journey (6 questions) shall we? 🕵️‍♂️

### Question 1 

`[1] How many bits is the prime p? >`

Ok so the first question is pretty easy right?
```py
p=21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061

r.sendlineafter(b'> ', str(len(bin(p))-2).encode())

print("Step 1 Completed")
```

I mean this was a gift , let's go straight to the second 🏃‍➡️

### Question 2

`[2] Enter the full factorization of the order of the multiplicative group in the finite field F_p in ascending order of factors (format: p0,e0_p1,e1_ ..., where pi are the distinct factors and ei the multiplicities of each factor) >`

Finally we finally start to see the good stuff! Second question it's asking us the factorization of the multiplicative order of the finite field F_p in a certain format...that's a lot of new things! 😁

First what's the order of the multiplicative group?

- The order of the multiplicative group in a finite field F_p is (p-1), where p is the prime number given

Ok but what are is a finite field?

- Well i don't think this is the right place to talk about that but if someone is interested this is the [Wikipedia](https://en.wikipedia.org/wiki/Finite_field) of it

Enough with the chit chat let's solve this

```python
from sympy import factorint

def factorize_multiplicative_order(p):
	order = p - 1
	factors = factorint(order)
	result_parts = []
	for prime, exponent in sorted(factors.items()):
	result_parts.append(f"{prime},{exponent}")
	return "_".join(result_parts)

p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
result = factorize_multiplicative_order(p)
print(f"The factorization of the order of the multiplicative group in F_p is:")
print(result)


The factorization of the order of the multiplicative group in F_p is:
2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1
```

Just a custom to put it in the right format (yeah it's python it will take around 30 seconds, you can use sage if you want)

let's see if it works!!

```python
result = "2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1"

r.sendlineafter(b'> ', result.encode())

print("Step 2 Completed")
```

Clean 🧼

### Question 3

`[3] For this question, you will have to send 1 if the element is a generator of the finite field F_p, otherwise 0.
1084581224744421335058668892541562581085810104736732117824114916823430513769469391830561232314851210221380363315626? > `

...and know what the hell is a generator? 🤨

- A generator of this multiplicative group (also called a primitive element) is an element whose powers generate all non-zero elements of the field. 

Ah sweet let's see what are the condition for a number to be a generator 

`g^(p-1) ≡ 1 (mod p) AND g^((p-1)/q) ≠ 1 (mod p)`

😐...better if i start writing the code

```python
def is_generator(element, p):
order = p - 1
factors = {2: 2, 5: 1, 2533393: 1, 635599: 1, 206740999513: 1, 4122411947: 1, 175521834973: 1, 1994957217983: 1, 215264178543783483824207: 1, 10254137552818335844980930258636403: 1} //factors of p change them if your p is different 
for prime_factor in factors:
	exponent = order // prime_factor
	result = pow(element, exponent, p)
	if result == 1:
		return 0
return 1
```

oh a i forgot to tell you the question wants to do it 16 times (really useful 😒)...

Will the crazy function work?

```python
r.recv()
command=r.recv().decode()
count=0
while "?" in command:
	command=command.split('?')
	element= int(command[0])
	result = is_generator(element, p)
	r.sendline(str(result).encode())
	print(f"Step 3.{count} Completed")
	count+=1
	command=r.recv().decode()
```

Of course!! 💪

### Question 4 

`The scholars present a sacred mathematical construct, a curve used to protect the most guarded secrets of the realm. Only those who understand its nature may proceed`


`[4] What is the order of the curve defined over F_p? >`

Phew~ finally a moment of peace, i think...

Sadly no, we got more theory now so let's see what is the order of the curve (at least they gave as a an b).

The order of an elliptic curve is the number of points on the curve, including the point at infinity.

AND HOW I'M SUPPOSED TO CALCULATE THAT? 😱
- Strangely it's pretty easy since there are already algorithms that did that like the [Schoof's Algorithm](https://en.wikipedia.org/wiki/Schoof%27s_algorithm) or the improved version [SEA](https://en.wikipedia.org/wiki/Schoof%E2%80%93Elkies%E2%80%93Atkin_algorithm)

I found some implementation online so here it is
```python
from sage.all import EllipticCurve, GF

def calculate_curve_order(p, a, b):
    F = GF(p)
    try:
        E = EllipticCurve(F, [a, b])
        order = E.order()
        return order
    except Exception as e:
        return f"Error: {e}"

def main():s
    p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
    a = 408179155510362278173926919850986501979230710105776636663982077437889191180248733396157541580929479690947601351140
    b = 8133402404274856939573884604662224089841681915139687661374894548183248327840533912259514444213329514848143976390134   
    print("Calculating the order of the elliptic curve...")
    print(f"Prime p = {p}")
    print(f"Curve equation: y^2 = x^3 + ({a})x + {b}")
    order = calculate_curve_order(p, a, b)
    print(f"\nThe order of the curve is: {order}")

if __name__ == "__main__":
    main()
```

Yay we have mow the order!! 😁

`21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061`

mmmm it's strangely similar to our p...i wonder if that's a problem 🤔

```python
order = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061

r.sendlineafter(b'> ', str(order).encode())

print("Step 4 Completed")
```
### Question 5

`[5] Enter the full factorization of the order of the elliptic curve defined over the finite field F_{p^3}. Follow the same format as in question 2 >`

Now we start to get serious, many people in this CTF stopped here but why?

Well most probably the tried a to calculate the factorization the same way we did in question 2...trust me it takes ages(i tried it too)

So to avoid the problem we factorize it with [factordb.com](https://factordb.com/) manually

```python
from sage.all import GF, EllipticCurve

def compute_order_Fp3(p, order_Fp):
    t_p = p + 1 - order_Fp
    t_p3 = t_p**3 - 3 * p * t_p
    order_Fp3 = p**3 + 1 - t_p3
    return order_Fp3

if __name__ == "__main__":
    p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
    order_Fp = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
    order_Fp3 = compute_order_Fp3(p, order_Fp)
    print(f"Order of the elliptic curve over F_{{p^3}}: {order_Fp3}")
```

We end up with this

`"2,2_7,2_21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061,1_2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019,1"`

Let's if it works 

```python
result = "2,2_7,2_21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061,1_2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019,1"

r.sendlineafter(b'> ', result.encode())

print("Step 5 Completed")
```

Chef kiss 👨‍🍳

### Question 6 

`The final trial awaits. You must uncover the hidden multiplier "d" such that A = d * G.`

⚔️ The chosen base point G has x-coordinate: 10754634945965100597587232538382698551598951191077578676469959354625325250805353921972302088503050119092675418338771

🔮 The resulting point A has x-coordinate: 20218265578401287226238954336311022293363655297243874023240611622078908973786506334254055081465272637959945768214219

`[6] What is the value of d? >`

Ladies and Gentlemen we are now on the final question yippie!!! 🥳

Now this was hard cause we are trying to break the [ECC](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography) more precisely the [Elliptic curve point multiplication](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication) which is basically the thing that the security of ECC depends on

So how do we do it?
- Well....we can't, it's a computational hazard trying to calculate that and this challenge has a very narrow time limit

So you are basically saying we are cooked?
- Absolutely no, remember when i said that the order was identical to the p? If you do then congratulations cause we just found our vulnerability

### THE VULNERABILITY

Props to the [man](https://github.com/elikaski/ECC_Attacks?tab=readme-ov-file#ECC-Attacks) which i stealed the exploit from 🙏

Basically since p and the order are the same it makes the curve anomalous

>If a certain curve has the property that the order of the curve (the number of points on it) is exactly equal to the modulus `𝑝`, then it is called an `Anomalous Curve` and is vulnerable to an attack called Smart's Attack. This attack uses `𝑝-adic numbers`. Such a number can be represented as a sum of powers of `p` (positive and negative) with coefficients. Formally, such a number `s` is a series of the form:

```python
def lift(P, E, p):
    # lift point P from old curve to a new curve
    Px, Py = map(ZZ, P.xy())
    for point in E.lift_x(Px, all=True):
         # take the matching one of the 2 points corresponding to this x on the p-adic curve
        _, y = map(ZZ, point.xy())
        if y % p == Py:
            return point

p = 82880337306360052550952380657384418102169134986290141696988204552000561657747
a = 26413685284385555604181540288021678971301314378522544469879270355650843743231
b = 10017655579196313780863100027113686719855502076415017585743221280232958057095
E = EllipticCurve(GF(p), [a, b])
G = E(37991937053350834320678619330546903567320901767090609881924528835279022654346,
      28947208718252880061735762506756351277969075978732800286053352115837132331595)
assert E.order() == p

private_key = 28153370716511608040616395150859085058202177279382452583684367923334520519740
P = private_key * G

# Lift the points to some new curve over p-adic numbers
E_adic = EllipticCurve(Qp(p), [a+p*13, b+p*37]) 
G = p * lift(G, E_adic, p)
P = p * lift(P, E_adic, p)

# Calculate discrete log
Gx, Gy = G.xy()
Px, Py = P.xy()
found_key = int(GF(p)((Px / Py) / (Gx / Gy)))
assert found_key == private_key
print("success!")

from Crypto.Util.number import long_to_bytes
print("The private key is:", long_to_bytes(found_key).decode())
```

then we are left with a few things to do:
1. find the exact coordinate of the points
2. modify and finalize the solve

### Final push

To find the exact cooridnate we use [Tonelli-shanks algorithm](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm) which will help us calculate the Weirestrass form y^2=x^3+ax+b of the elliptic curve

```python
def tonelli_shanks(n, p):
    assert pow(n, (p - 1) // 2, p) == 1
    if n == 0:
        return 0
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    while t != 0 and t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 2**(m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r if t == 1 else None
```

And we call it with this 

```python
def get_y(x, a, b, p):
    rhs = (x**3 + a*x + b) % p
    y = tonelli_shanks(rhs, p) 
    if y is None:
        return None 
    return y
```

## The completed script

What a journey don't you think? Well i don't want to make you lose more time than i've already did let's see if our final solution works 🙏

```python
from pwn import *
from sage.all import *

def is_generator(element, p):
    order = p - 1
    factors = {2: 2, 5: 1, 2533393: 1, 635599: 1, 206740999513: 1, 4122411947: 1, 175521834973: 1, 1994957217983: 1, 215264178543783483824207: 1, 10254137552818335844980930258636403: 1}
    for prime_factor in factors:
        exponent = order // prime_factor
        result = pow(element, exponent, p)
        if result == 1:
            return 0
    return 1

def tonelli_shanks(n, p):
    assert pow(n, (p - 1) // 2, p) == 1
    if n == 0:
        return 0
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    while t != 0 and t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 2**(m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r if t == 1 else None

def get_y(x, a, b, p):
    rhs = (x**3 + a*x + b) % p
    y = tonelli_shanks(rhs, p)  
    if y is None:
        return None  
    return y

def lift(P, E, p):
    Px, Py = map(ZZ, P.xy())
    for point in E.lift_x(Px, all=True):
        _, y = map(ZZ, point.xy())
        if y % p == Py:
            return point

context.log_level='debug'
r=remote('94.237.54.21', 46987)
r.recv()
p=21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
r.sendlineafter(b'> ', str(len(bin(p))-2).encode())
print("Step 1 Completed")
result = "2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1"
r.sendlineafter(b'> ', result.encode())
print("Step 2 Completed")
r.recv()
command=r.recv().decode()
count=0
while "?" in command:
    command=command.split('?')
    element= int(command[0])
    result = is_generator(element, p)
    r.sendline(str(result).encode())
    print(f"Step 3.{count} Completed")
    count+=1
    command=r.recv().decode()
order = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
r.sendlineafter(b'> ', str(order).encode())
print("Step 4 Completed")
result = "2,2_7,2_21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061,1_2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019,1"
r.sendlineafter(b'> ', result.encode())
print("Step 5 Completed")
a = 408179155510362278173926919850986501979230710105776636663982077437889191180248733396157541580929479690947601351140
b = 8133402404274856939573884604662224089841681915139687661374894548183248327840533912259514444213329514848143976390134
r.recvuntil(b': ')
G_x = int(r.recvline(b'\n').strip().decode())
r.recvuntil(b': ')
A_x = int(r.recvline(b'\n').strip().decode())
A_y = get_y(A_x, a, b, p)
G_y = get_y(G_x, a, b, p)
E = EllipticCurve(GF(p), [a, b])
G = E(G_x,G_y)
A = E(A_x,A_y)
E_adic = EllipticCurve(Qp(p), [a+p*13, b+p*37]) 
G = p * lift(G, E_adic, p)
A = p * lift(A, E_adic, p)
Gx, Gy = G.xy()
Ax, Ay = A.xy()
d = int(GF(p)((Ax / Ay) / (Gx / Gy)))
r.sendlineafter(b'> ', str(d).encode())
print("Step 6 Completed")
print(r.recv().decode())
print(r.recv().decode())

```

Glad it worked...i'll go take a nap here's the flag dear reader 😴

> HTB{Welcome_to_CA_2k25!Here_is_your_anomalous_flag_for_this_challenge_and_good_luck_with_the_rest:)_2f664847bc320f905f4ba6a6ec7124b8}
