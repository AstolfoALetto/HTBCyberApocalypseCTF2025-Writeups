# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Encrypted Scroll
> Elowen Moonsong, an Elven mage of great wisdom, has discovered an ancient scroll rumored to contain the location of The Dragon’s Heart. However, the scroll is enchanted with an old magical cipher, preventing Elowen from reading it.

- **Category**: Rev
- **Difficulty**: Very Easy
- **Author**: Massandre

## Summary & Consideration

In this challenge we are given only the executable file.

## Writeup

Executing the challenge asks us for an input:


```bash
      ___________________________
    /                             \
    |  **Ancient Elven Scroll**   |
    |-----------------------------|
    |  The knowledge you seek is  |
    |  hidden within the old runes|
    |  of the Elven mages...      |
    |  Speak the words of power.  |
    \_____________________________/

The ancient scroll hums with magical energy. Enter the mage’s spell:
```

And it seems that any input given results in the same message:

```bash
The scroll remains unreadable... Try again.
```

So now that we know that by executing the challenge we can't do much we open it up on ghidra and go in the main function:


```C
undefined8 main(void)
{
  long in_FS_OFFSET;
  undefined1 local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  anti_debug();
  display_scroll();
  printf(&DAT_00102220);
  __isoc99_scanf(&DAT_00102268,local_48);
  decrypt_message(local_48);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

We see that it asks for input with:

```C
__isoc99_scanf(&DAT_00102268,local_48);
```

So we have our input in the variable local_48.

Then we see that it gets called the function decrypt_message that as parameter has local_48 so we can suppose that there is where the input is checked.

```C
void decrypt_message(char *param_1)
{
  int iVar1;
  long in_FS_OFFSET;
  int local_3c;
  char local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  builtin_strncpy(local_38,"IUC|t2nqm4`gm5h`5s2uin4u2d~",0x1c);
  for (local_3c = 0; local_38[local_3c] != '\0'; local_3c = local_3c + 1) {
    local_38[local_3c] = local_38[local_3c] + -1;
  }
  iVar1 = strcmp(param_1,local_38);
  if (iVar1 == 0) {
    puts("The Dragon\'s Heart is hidden beneath the Eternal Flame in Eldoria.");
  }
  else {
    puts("The scroll remains unreadable... Try again.");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

In the function we see that this call is made:

```C
builtin_strncpy(local_38,"IUC|t2nqm4`gm5h`5s2uin4u2d~",0x1c);
```

So the string "IUC|t2nqm4`gm5h`5s2uin4u2d~" gets copied in local_38.

Then we see that our input param_1 is compared to local_38 so we can suppose that local_38 must be the flag so analyzing the code before we see that to every character of local_38 is subtracted 1:

```C
for (local_3c = 0; local_38[local_3c] != '\0'; local_3c = local_3c + 1) {
   local_38[local_3c] = local_38[local_3c] + -1;
}
```

So the flag must be the string "IUC|t2nqm4`gm5h`5s2uin4u2d~" but with every character in ascii subtracted by 1.

```py
>>> a="IUC|t2nqm4`gm5h`5s2uin4u2d~"
>>> flag=""
>>> for x in a:
...     flag+=chr(ord(x)-1)
>>> flag
'HTB{s1mpl3_fl4g_4r1thm3t1c}'
```

> HTB{s1mpl3_fl4g_4r1thm3t1c}