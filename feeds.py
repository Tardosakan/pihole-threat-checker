import urllib.request

URL = "https://urlhaus.abuse.ch/downloads/hostfile/"

def load_urlhaus():
	bad_domains = set()
	text = urllib.request.urlopen(URL).read().decode()
	for line in text.splitlines():
		if not line or line.startswith("#"):
			continue
		domain = line.split()[1]
		bad_domains.add(domain)
	return bad_domains

if __name__ == "__main__":
	print(len(load_urlhaus()))
