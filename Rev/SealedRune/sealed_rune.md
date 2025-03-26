# Cyber Apocalypse CTF 2025: Tales from Eldoria


## SealedRune
> Elowen has reached the Ruins of Eldrath, where she finds a sealed rune stone glowing with ancient power. The rune is inscribed with a secret incantation that must be spoken to unlock the next step in her journey to find The Dragon’s Heart.

- **Category**: Rev 
- **Difficulty**: Very Easy
- **Author**: Ventilatore

## Writeup

```C
undefined8 main(void)
{
  long in_FS_OFFSET;
  undefined1 local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  anti_debug();
  display_rune();
  puts(&DAT_00102750);
  printf("Enter the incantation to reveal its secret: ");
  __isoc99_scanf(&DAT_001027c5,local_48);
  check_input(local_48);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
```c
void check_input(char *param_1)
{
  int iVar1;
  char *__s2;
  long lVar2;
  
  __s2 = (char *)decode_secret();
  iVar1 = strcmp(param_1,__s2);
  if (iVar1 == 0) {
    puts(&DAT_00102050);
    lVar2 = decode_flag();
    printf("\x1b[1;33m%s\x1b[0m\n",lVar2 + 1);
  }
  else {
    puts("\x1b[1;31mThe rune rejects your words... Try a gain.\x1b[0m");
  }
  free(__s2);
  return;
}
```
```c
undefined8 decode_secret(void)
{
  undefined8 uVar1;
  
  uVar1 = base64_decode(incantation);
  reverse_str(uVar1);
  return uVar1;
}
```

```
incantation = 656d46795a6d5a31626b64735a57465700
```

decode from base64
```
zarffunGleaV
```

reversed
```
VaelGnuffraz
```

input into the executable
```bash
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠀⠘⠃⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢠⡀⠀⢀⣤⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣷⣾⡷⠞⠛⠙⣛⣷⣤⣤⣄⡀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⢀⣤⣾⣿⣯⡁⠀⠀⠀⠀⠀⠀⠀⠀⣈⣿⣿⣦⣤⡀⠀⠀⠀⠀
       ⠀⠀⠀⢠⣾⡿⠛⠁⠀⠙⢿⡄⠀⠀⠀⠀⠀⠀⣸⡿⠋⠀⠙⠛⢿⣦⡀⠀⠀
       ⠀⠀⣴⡿⠁⠀⠀⠀⠀⠀⠈⣿⣶⣤⣀⣀⣤⣶⣿⠁⠀⠀⠀⠀⠀⠙⢿⣦⠀
       ⠀⣾⡟⠀⠀⠀⠀⠀⠀⠀⢰⡟⠉⠛⠿⠿⠛⠉⢻⡆⠀⠀⠀⠀⠀⠀⠘⣷  
       ⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⢹  
       ⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⣸⠇  
        ⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⢰⠇⠀⠀⠀⠀⠀⠀⣰⠏    
         ⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣄⠀⠀⣀⡾⠀⠀⠀⠀⠀⣠⠞⠁    
           ⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠙⠓⠚⠋⠀⠀⠀⠀⣠⡾⠁      
              ⠙⠳⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡤⠖⠋        
                 ⠈⠛⠶⣤⣄⡀⠀⠀⢀⣠⡤⠖⠛⠁          
                     ⠉⠛⠛⠉
🔮 The ancient rune shimmers with magical energy... 🔮
Enter the incantation to reveal its secret: VaelGnuffraz
The rune glows with power... The path to The Dragon’s Heart is revealed!
The secret spell is `HTB{run3_m4g1c_r3v34l3d}`.
```

>HTB{run3_m4g1c_r3v34l3d}