import json
import urllib.request

def load_webhook():
	with open("discord_webhook.txt") as f:
		return f.read().strip()

def send_discord(message):
	data = json.dumps({"content": message}).encode()
	headers = {"Content-Type": "application/json",
	           "User-Agent": "pihole-threat-checker"}
	request = urllib.request.Request(load_webhook(), data=data, headers=headers)
	urllib.request.urlopen(request)

if __name__ == "__main__":
	send_discord("Test from Pi-hole checker")
