import requests # pip install requests
import random

while True:
    typ = random.choice(['INCREMENT', 'DECREMENT'])
    value = random.randrange(1, 6)
    eve = {"Type": typ, "Value": value}
    requests.post('http://127.0.0.1:5000/event', eve)

