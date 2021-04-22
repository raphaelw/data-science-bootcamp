# pip install pyjokes
import pyjokes
import requests

webhook_url = open('webhook.txt').read()

joke = pyjokes.get_joke()

data = {'text': joke}
requests.post(url=webhook_url, json = data)
