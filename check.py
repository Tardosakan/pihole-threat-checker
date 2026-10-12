from feeds import load_urlhaus
from read_queries import get_recent_queries

bad = load_urlhaus()
queries = get_recent_queries()

for time, client, domain in queries:
	if domain in bad:
		print(f"MALICIOUS: {time} {client} {domain}")

print(f"Checked {len(queries)} queries")
