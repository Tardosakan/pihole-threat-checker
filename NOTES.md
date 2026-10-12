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

## Bugs and
