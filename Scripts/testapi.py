import requests
import json
import random 

gifurl = "https://api.giphy.com/v1/gifs/search"

querystring = {"api_key": "kwz8Oi8yrggYBqp0C05LXtyOlcUw0kLq", "q": "welcome", "limit": 20}
response = requests.request("GET", gifurl, params=querystring)

response_gifs_urls = json.loads(response.text)['data']
random_gif_url = random.choice(response_gifs_urls)

a = random_gif_url["images"]['original']['url'].split("?")

print(a[0])