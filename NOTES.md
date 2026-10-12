# Development notes

## 2026-10-12: First investigation (Conky weather widget)

**Detection**
The check-in count flagged two unknown domains queried by the laptop (127.0.0.1):
`wttr.in` (124 queries/24h) and `example.org` (125 queries/24h).
Near-identical counts suggested one program behind both.

**Triage**
The average (~1 query every 11–12 min) suggested a steady beacon.
The timeline showed otherwise: short bursts of many queries within one second,
first seen 2026-10-11 15:48:17, then quiet for ~3 hours.
Bursts point to an event trigger (e.g. network change, wake from sleep, widget refresh),
not a timer. Lesson: averages hide patterns, so always check the timeline.

**Attribution**
Searched the home folder for the domain:
`grep -rl "wttr.in" ~ 2>/dev/null`
Found `~/.config/conky/weather.sh`, the weather script of my Conky desktop widget.
(`example.org` link to the script: still to confirm by reading it.)

**Verdict**
Benign, self-installed software. Both domains added to the allowlist,
with a comment saying why.

## Design decisions

- **Read-only, least privilege:** the tool opens `pihole-FTL.db` with `mode=ro`,
  and my user reads it through the `pihole` group instead of running as root.
- **Subdomain matching:** a visited domain is checked together with its parents
  (`a.b.bad.com` → `b.bad.com` → `bad.com`), so subdomains of listed domains are caught.
- **Allowlist only affects check-in counting.** Known-bad (URLhaus) and risky-TLD checks
  still run on every query, because attackers can hide on trusted services.
- **Risky TLDs are a hardcoded heuristic** (`.top`, `.xyz`, `.zip`, ...), not a live feed,
  because TLD abuse changes slowly and is a judgment call. Possible later: a config file.
- **Testing with known positives:** detections were verified by temporarily adding a
  harmless domain (`google.com`) or TLD (`hu`), never by visiting real malware sites.
- **Webhook URL is treated as a secret:** stored in `discord_webhook.txt`, listed in
  `.gitignore` before the file was created, and set to `chmod 600` so only my user can read it.
  The code only knows where to find the secret, never the secret itself.
- **Discord gets a short summary, the full report stays local:** Discord messages are limited
  to 2,000 characters, and the full report contains my browsing history.
- **Report file is written before the Discord message is sent:** if Discord is down,
  the report is still saved.
- **Reports are kept out of GitHub:** `reports/` is in `.gitignore`, because the reports
  list every domain my devices visited.

## Automation

Runs daily at 07:47 via cron (crontab, not part of the repo):

    47 7 * * * cd /home/tardos/pihole-threat-checker && /usr/bin/python3 check.py >> reports/cron.log 2>&1

- `cd` first, because the script uses relative paths (imports, `reports/`), and cron starts in the home folder
- Full paths everywhere, because cron runs with a minimal environment
- `>> reports/cron.log 2>&1` appends both normal output and errors to a log, since cron has no screen
- Tested by temporarily scheduling it a few minutes ahead, checking the log, then setting it back
- 07:47 instead of 08:00: avoids the busy top of the hour, and the report is ready in the morning

## Bugs and
