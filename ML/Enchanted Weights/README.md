# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Enchanted Weights
> In the depths of Eldoria's Crystal Archives, you've discovered a mystical artifact—an enchanted neural crystal named eldorian_artifact.pth. Legends speak of a hidden incantation—an ancient secret flag—imbued directly within its crystalline structure.


- **Category**: ML 
- **Difficulty**: Easy
- **Author**: Alexct549

## Writeup

God I love machine learning ❤️

We see an hidden weight in the model, which is a string of characters, we can decode it to get the flag.

```python
import torch

model = torch.load("eldorian_artifact.pth", map_location="cpu")
print(model)
for key, value in model.items():
    arr = value.numpy().flatten()
    decoded = "".join([chr(int(x)) for x in arr if 32 <= x <= 126])
    print(decoded)
```

> HTB{Cry5t4l_RuN3s_0f_Eld0r1a}
