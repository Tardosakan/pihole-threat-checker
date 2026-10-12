import urllib.request

bad_domains = set()

URL = "https://urlhaus.abuse.ch/downloads/hostfile/"

text = urllib.request.urlopen(URL).read().decode()

for line in text.splitlines():
	if not line or line.startswith("#"):
		continue
	domain = line.split()[1]
	bad_domains.add(domain)

print(len(bad_domains))
