# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Stoneforge's Domain
> Garrick is a hardworking craftsman working in Eastmarsh to cheer the local and avail amazing tools and trinkets. As much as his desire to use his craft for other things, there is no place is like home. To thank the local folks, he created a system for adventurers to easily acquire tools and trinkets but it appears there are some small vulnerabilities since it launched as beta testing site. Can you undertake this crucial task and assist us to give the adventurers this unique experience ? A handsome reward awaits ;)


- **Category**: Secure Coding 
- **Difficulty**: Easy
- **Author**: Cioppo

## Writeup


Looking at ``exploit.py``
```py
def exploit():
    # Get the file
    r = requests.get(f"{URL}/static../{FILE}")

    # Save the file
    with open(f"/tmp/{FILE}", 'wb') as f:
        f.write(r.content)

    print(f"File {FILE} downloaded to /tmp/{FILE}")
```
the problem is a path traversal from the ``static`` folder, let's look at the alias in the ``nginx.conf``
```
    location /static {
        alias /www/application/app/static/;
    }
```
We are missing the trailing ``/`` in the alias, let's put it there!
```
    location /static/ {
        alias /www/application/app/static/;
    }
```
This is enough to get the flag ;)

>HTB{W4LK1N9_7H3_570N3F0R93_P47H_45_R3QU1R3D_80dec0cff56f1104f9d12fd63702f818}