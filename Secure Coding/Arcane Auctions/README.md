# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Arcane Auctions
> In a shattered world where digital decay meets mystical forces, The Arcane Auction House stands as a beacon of hope. Amid the ruins of civilization, survivors gather in this virtual marketplace to barter enchanted relics and futuristic artifacts. Here, relics of forgotten magic blend with remnants of cyber technology, offering weapons, armor, and mysterious items that promise to restore power and balance. Every bid ignites fierce competition among desperate souls, as each transaction could unlock secrets to reclaim lost glory. With rogue AIs lurking in the neon shadows and crumbling infrastructures all around, this auction house is more than a trading platform—it’s a lifeline in a cyber apocalypse, where every artifact holds the potential to rewrite destiny in a world on the brink.


- **Category**: Secure Coding 
- **Difficulty**: Easy
- **Author**: Cioppo


## Writeup

The exploit sends the following payload to the ``/api/filter`` endpoint
```py
def exploit_filter_password_leak():
    print("Attempting to exploit the filter endpoint to leak seller passwords...")
    payload = {
        "filter": {
            "select": {
                "seller": {
                    "select": {
                        "password": True
                    }
                }
            }
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/filter", json=payload)
    except Exception as e:
        print("Request failed:", e)
```

The endpoint is defined in the ``routes.js`` file as follows:
```js
// Filtering Endpoint: Accepts a Prisma-style filter object from the client in req.body.filter.
router.post('/api/filter', async (req, res) => {
  try {
    const filter = req.body.filter || {};
    const items = await prisma.item.findMany(filter);
    res.json(items);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Filtering error' });
  }
});
```
we notice that there is no filtering present on the body of the request, so anyone can make every kind of request they want.
By reading the rest of the code we know that this endpoint is only used when filtering the times in the main page, it's never used in any kind of password check (as it should). 
We can just add a check to the request body and send an error page if the request asks for passwords:
```js
// Filtering Endpoint: Accepts a Prisma-style filter object from the client in req.body.filter.
router.post('/api/filter', async (req, res) => {
  try {
    const filter = req.body.filter || {};
    try {
      if ( filter["select"]["seller"]["select"]["password"]) {
        res.status(500).json({ error: 'Naughty Naughty!' });
        return;
      }
    } catch(error) {}
    console.log(filter)
    const items = await prisma.item.findMany(filter);
    res.json(items);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Filtering error' });
  }
});
```
This is a pretty weak check, but in this challenge context it's enough ;)

>HTB{l00k_0ut_f0r_0rm_l34k_bug_cut13_b1620adc5848d23cce6f04bff87b1437}