import sqlite3

def get_recent_queries():
	conn = sqlite3.connect("file:/etc/pihole/pihole-FTL.db?mode=ro", uri=True)

	rows = conn.execute("""
		SELECT datetime(timestamp, 'unixepoch', 'localtime'), client, domain FROM queries WHERE timestamp > CAST(strftime('%s', 'now') AS INTEGER) - 86400 ORDER BY timestamp DESC
	""").fetchall()
	conn.close()
	return rows

if __name__ == "__main__":
    for row in get_recent_queries():
        print(row)
