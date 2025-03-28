import requests

with open(f"Ashen_Outpost_Records.csv", "r") as f:
	r = requests.post("http://IP:PORT/score", files={"csv_file": f})
	print(r.text)