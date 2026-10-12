# Pi-hole DNS Threat Checker

A Python tool that reviews my home network's DNS traffic every day and flags
anything suspicious. It reads the query log of my self-hosted Pi-hole, checks
every domain against a live malware feed, looks for suspicious patterns, writes
a daily report, and sends a summary to Discord.

Built on my [Pi-hole home lab](https://github.com/Tardosakan/pihole-home-lab),
running on an old Asus laptop with Linux Mint.

## Why

DNS is one of the best places to spot trouble on a network: almost everything
a device does starts with a DNS lookup, including malware contacting its
controller. This project automates the first steps of what a SOC analyst does
with DNS logs: collect, enrich with threat intelligence, detect, and report.

## Features

- **Reads Pi-hole's DNS log** directly from its SQLite database (read-only), covering the last 24 hours
- **Known-bad check:** matches every domain against the [abuse.ch URLhaus](https://urlhaus.abuse.ch/) hostfile, downloaded fresh on each run, including subdomains (`www.bad.com` is caught when `bad.com` is listed)
- **Risky TLD check:** flags domains on top-level domains often used for abuse (`.top`, `.xyz`, `.zip`, ...)
- **Check-in counting:** counts how often each device queries each domain, to spot repeated "calling home"; an allowlist removes known-good services so the rest is worth a look
- **Daily report** saved to `reports/YYYY-MM-DD.txt`
- **Discord summary** with the number of malicious and suspicious hits
- **Runs automatically** every morning via cron

## Sample output

Daily report (shortened):

    Checked 7517 queries
    TOP check-ins:
      158 127.0.0.1       firefox.settings.services.mozilla.com
       78 127.0.0.1       mozilla-ohttp.fastly-edge.com
       65 127.0.0.1       safebrowsing.googleapis.com
       36 127.0.0.1       cdn.fwupd.org
       32 127.0.0.1       packages.linuxmint.com

Discord summary:

    Pi-hole report 2026-10-12
    Malicious: 0
    Suspicious: 0
    Checked 7517 queries

A detection looks like this (format only, not a real hit):

    MALICIOUS:  <time> <device IP> <domain>
    SUSPICIOUS: <time> <device IP> <domain>

## Setup

**Requirements:** a running Pi-hole (v6), Python 3, no extra packages needed (only the standard library).

1. Give your user read-only access to Pi-hole's database, instead of running as root:

        sudo usermod -aG pihole $USER

   Log out and back in for the group change to take effect.

2. Clone the repo:

        git clone https://github.com/Tardosakan/pihole-threat-checker.git
        cd pihole-threat-checker

3. (Optional) Discord alerts: create a webhook in your server (Server Settings → Integrations → Webhooks), then save its URL:

        nano discord_webhook.txt
        chmod 600 discord_webhook.txt

   The file is in `.gitignore`, so it's never committed.

4. Run it:

        python3 check.py

   The report is printed and saved to `reports/YYYY-MM-DD.txt`.

5. Schedule it daily with cron (`crontab -e`):

        47 7 * * * cd /path/to/pihole-threat-checker && /usr/bin/python3 check.py >> reports/cron.log 2>&1

## Design decisions

- **Least privilege:** the database is opened read-only (`mode=ro`), through group membership instead of root.
- **Allowlist only affects check-in counting.** Known-bad and risky-TLD checks always run on every query, because attackers can hide behind trusted services.
- **Secrets stay out of git:** the Discord webhook URL lives in a `chmod 600` file listed in `.gitignore`.
- **Reports stay local:** they contain browsing history, so `reports/` is never committed; Discord only gets a short summary.
- **Detections tested with known positives** (temporarily listing a harmless domain), never by visiting real malware sites.

## First investigation

The check-in count
