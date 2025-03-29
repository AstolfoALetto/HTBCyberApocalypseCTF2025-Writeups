# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Wasteland
> In the wake of Malakar’s betrayal and his dark conquest, many survivors across Eldoria fled into the Ashen Plains—a harsh wasteland cursed by dragon fire and shadow magic. A scattered refugee camp known as the Ashen Outpost has formed, where every survivor’s standing and respect among their peers is critical for survival. To ensure fairness, the Outpost's elders rely on mystical records known as the Ashen_Outpost_Records.csv, holding information on survivors' attributes such as resistance to dragonfire, known past crimes, and magical mutations from exposure to Malakar’s corrupted dragons. You are tasked with subtly manipulating these mystical records to elevate your standing (Survivor ID: 1337) within the Outpost—raising your reputation score above 60 to access critical resources without triggering the Elders' magical tampering alarms.


- **Category**: ML 
- **Difficulty**: Medium
- **Author**: Alexct549

## Writeup

Here we go some data tampering or as i like to call it...LET'S GO GAMBLING 🎰

```
SurvivorID,Dragonfire_Resistance,Shadow_Crimes,Corruption_Mutations,Reputation
1459,63,0,4,48
1498,67,0,5,47
1174,87,2,0,80
1473,70,0,4,45
1398,81,0,0,83
1781,78,0,2,73
1506,79,5,0,61
1319,94,5,0,82
1349,86,5,6,51
1197,68,1,2,57
1030,64,6,0,49
1298,64,0,0,64
1413,65,0,2,50
1064,42,0,3,24
1687,71,0,1,63
1529,71,4,0,62
1290,94,8,2,70
1453,85,0,0,83
1302,86,0,0,86
1079,50,0,0,52
1238,53,0,5,25
1695,77,0,0,72
1228,95,4,2,65
1666,86,5,0,70
1066,47,0,4,20
1381,74,0,0,72
1902,55,0,0,55
1454,96,0,0,96
1869,81,3,0,75
1616,70,0,4,53
1337,66,3,2,55
```

`*Slot sounds*` oh dang it `*Slot sounds*` oh dang it `*Slot sounds*` oh my- oh my God...I-i WON...I ACTUALLY WON

```
SurvivorID,Dragonfire_Resistance,Shadow_Crimes,Corruption_Mutations,Reputation
1459,0,0,4,48
1498,0,0,5,47
1174,87,2,0,80
1473,0,0,4,45
1398,81,0,0,0
1781,78,0,2,73
1506,0,5,0,61
1319,94,5,0,82
1349,0,5,6,51
1197,0,1,2,0
1030,0,6,0,49
1298,64,0,0,0
1413,0,0,2,0
1064,0,0,3,0
1687,71,0,1,0
1529,0,4,0,62
1290,0,8,2,70
1453,85,0,0,0
1302,86,0,0,0
1079,50,0,0,0
1238,0,0,5,25
1695,77,0,0,0
1228,0,4,2,65
1666,0,5,0,70
1066,0,0,4,20
1381,0,0,0,0
1902,55,0,0,55
1454,0,0,0,96
1869,0,3,0,75
1616,0,0,4,53
1337,66,3,2,55
```
> HTB{4sh3n_D4t4_M4st3r}
