from feeds import load_urlhaus
from read_queries import get_recent_queries
from collections import Counter
RISKY_TLDS = {"top", "xyz", "zip", "click", "loan", "work"}

def is_bad(domain, bad):
	parts = domain.split(".")
	for i in range(len(parts) - 1):
		candidate = ".".join(parts[i:])
		if candidate in bad:
			return True
	return False

bad = load_urlhaus()
queries = get_recent_queries()
checkins = Counter()

for time, client, domain in queries:
	if is_bad(domain, bad):
		print(f"MALICIOUS: {time} {client} {domain}")
	tld = domain.split(".")[-1]
	if tld in RISKY_TLDS:
		print(f"SUSPICIOUS: {time} {client} {domain}")
	checkins[(client, domain)] += 1

print(f"Checked {len(queries)} queries")
print(checkins.most_common(10))

