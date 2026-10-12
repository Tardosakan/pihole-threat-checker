import sqlite3

conn = sqlite3.connect("file:/etc/pihole/pihole-FTL.db?mode=ro", uri=True)

rows = conn.execute("""
	SELECT datetime(timestamp, 'unixepoch', 'localtime'), client, domain FROM queries WHERE timestamp > CAST(strftime('%s', 'now') AS INTEGER) - 86400 ORDER BY timestamp DESC
 LIMIT 10;
""")

for row in rows:
	print(row)
