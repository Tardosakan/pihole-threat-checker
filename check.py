from feeds import load_urlhaus
from read_queries import get_recent_queries
from collections import Counter
from datetime import date
from notify import send_discord
import os
RISKY_TLDS = {"top", "xyz", "zip", "click", "loan", "work"}
ALLOWLIST = {"claude.ai", "anthropic.com", "ubuntu.com", "mozilla.org",
             "firefox-portal-detection.com", "flathub.org", "github.com",
             "google.com", "ipv4only.arpa", "mozilla.com", "wttr.in", "example.org"}	# Conky weather widget (~/.config/conky/weather.sh)

def matches(domain, bad):
	parts = domain.split(".")
	for i in range(len(parts) - 1):
		candidate = ".".join(parts[i:])
		if candidate in bad:
			return True
	return False

bad = load_urlhaus()
queries = get_recent_queries()
checkins = Counter()
lines = []
malicious_count = 0
suspicious_count = 0

for time, client, domain in queries:
	if matches(domain, bad):
		lines.append(f"MALICIOUS: {time} {client} {domain}")
		malicious_count += 1
	tld = domain.split(".")[-1]
	if tld in RISKY_TLDS:
		lines.append(f"SUSPICIOUS: {time} {client} {domain}")
		suspicious_count += 1
	if not matches(domain, ALLOWLIST):
		checkins[(client, domain)] += 1

lines.append(f"Checked {len(queries)} queries")
lines.append("TOP check-ins:")
for (client, domain), count in checkins.most_common(10):
	lines.append(f"{count:>5} {client:<15} {domain}")

today = date.today().isoformat()
os.makedirs("reports", exist_ok=True)
with open(f"reports/{today}.txt", "w") as f:
	f.write("\n".join(lines))
print("\n".join(lines))

summary = (f"Pi-hole report {today}\n"
           f"Malicious: {malicious_count}\n"
           f"Suspicious: {suspicious_count}\n"
           f"Checked {len(queries)} queries")
if os.path.exists("discord_webhook.txt"):
	send_discord(summary)
