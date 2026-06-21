# SiftBlock

*Sift any keyword. Block what matches.*

SiftBlock is a configurable DNS blocklist aggregator and generator. Clone it, edit `config/keywords.txt` with terms relevant to you, and it aggregates matching domains from public threat-intelligence feeds into your own `blocklist.txt` — automatically, on a schedule, via GitHub Actions.

It isn't tied to any one brand or event. The most common use is **brand monitoring**: watch for domains impersonating your company, product, or an upcoming launch, and turn that into a blocklist you (or your org) can actually subscribe to.

---

## Quick start

1. Fork or clone this repo.
2. Edit [`config/keywords.txt`](config/keywords.txt) — replace the example terms with your own (your brand name, product name, launch codename, etc).
3. Optionally edit [`config/whitelist.txt`](config/whitelist.txt) — domains that match a keyword but are actually yours/legitimate, so they're never blocked.
4. Optionally edit [`config/meta.txt`](config/meta.txt) — the Title/Description shown in your blocklist's header.
5. Push. The next scheduled GitHub Actions run builds `blocklist.txt` automatically — no code changes needed.

The repo ships with a working example (World Cup 2026 phishing terms) so you can see real output immediately, before you've customized anything. See [`docs/DEPLOY.md`](docs/DEPLOY.md) for full step-by-step deployment instructions.

---

## Subscribe

```
https://raw.githubusercontent.com/zer0lightning/siftblock/main/blocklist.txt
```

| Platform | Instructions |
|---|---|
| **Pi-hole** | Group Management → Adlists → paste URL → Update Gravity |
| **AdGuard Home** | Filters → DNS Blocklists → Add blocklist → Custom |
| **uBlock Origin** | Settings → Filter lists → Import → paste URL |
| **Little Snitch** | New Rule Group → Subscribe → paste URL |

---

## Repo layout

```
siftblock/
├── README.md
├── DISCLAIMER.md
├── blocklist.txt                       ← generated output, always at repo root (stable subscribe URL)
├── blocklist-snapshot.txt              ← previous-day reference (auto-managed)
├── daily/YYYY-MM-DD.txt                ← new domains observed per day (auto-managed)
│
├── config/                             ← EVERYTHING YOU EDIT
│   ├── keywords.txt                        your match terms
│   ├── whitelist.txt                       your exclusions
│   ├── meta.txt                            your title/description
│   └── sources.txt                         threat-intel feed URLs
│
├── src/                                ← the engine — you shouldn't need to touch this
│   ├── generate_blocklist.py               fetch + sift engine
│   └── build_daily_header.py               header builder used by the daily workflow
│
├── docs/
│   └── DEPLOY.md                       ← step-by-step deployment guide
│
└── .github/workflows/
    ├── blocklist.yml                   ← hourly: generates blocklist.txt
    └── blocklist-daily.yml             ← daily: new-domain diff
```

Everything under `config/` is the only thing most users ever need to edit. `src/` and `.github/` are the machinery.

---

## Files you customize

| File | Required? | Purpose |
|---|---|---|
| `config/keywords.txt` | **yes** | Match terms, one per line, case-insensitive substring match. This is the whole point — point it at your brand. |
| `config/whitelist.txt` | optional | Domains always excluded, even if they match a keyword (and their subdomains). Delete or leave empty if you don't need it. |
| `config/meta.txt` | optional | `Title:` / `Description:` shown in `blocklist.txt`'s header. Falls back to a generic default if omitted. |

**Example — watching for a fictional "Acme" product launch:**

```
config/keywords.txt:
    acme2027
    acmelaunch

config/whitelist.txt:
    acme.com
    launch.acme.com

config/meta.txt:
    Title: Acme Threat Intelligence DNS Blocklist
    Description: Blocks phishing and scam domains themed around the Acme related domains
```

The output is always named `blocklist.txt` at the repo root, regardless of what your keywords are — so your subscribe URL never changes even if you update your keyword list later.

---

## Sources

Source threat-intel feeds are listed in [`config/sources.txt`](config/sources.txt) (not hardcoded in the script), currently aggregating:

- [BlocklistProject Phishing](https://github.com/blocklistproject/Lists)
- [NoTracking Hosts Blocklists](https://github.com/notracking/hosts-blocklists)
- [Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database)
- [UT1 Blacklists (phishing)](https://github.com/olbat/ut1-blacklists)
- [UT1 Blacklists (malware)](https://github.com/olbat/ut1-blacklists)
- [Maltrail](https://github.com/stamparm/maltrail)
- [Ultimate Hosts Blacklist](https://github.com/Ultimate-Hosts-Blacklist/MalwareDomainList.com)
- [StevenBlack Hosts](https://github.com/StevenBlack/hosts)
- [HaGeZi DNS Blocklists](https://github.com/hagezi/dns-blocklists)

---

## Example Output Format

Plain domain list, one entry per line, with a descriptive header:

```
# Title: World Cup 2026 Threat Intelligence DNS Blocklist
# Description: Blocks phishing, scam, and malware domains themed around the 2026 World Cup.
# Keywords: fifa, fwc26, wc2026, worldcup
# Last modified: 20 Jun 2026 10:00 UTC
# Number of entries: 1521
#
worldcup-tickets-scam.com
fake-worldcup26.net
...
```

---

## How it works

`src/generate_blocklist.py` fetches every source in `config/sources.txt` **concurrently**, filters every domain against `config/keywords.txt`, removes anything covered by `config/whitelist.txt`, deduplicates, sorts, and writes `blocklist.txt` at the repo root. A GitHub Actions workflow runs this every hour and commits the result only if the content changed.

### Reliability guards

The script aborts **without touching `blocklist.txt`** if either looks like a partial-data failure rather than a real change:

- Fewer than 50% of the configured sources returned data (e.g. a GitHub outage or rate limit).
- The new entry count is less than 50% of the previous run's count.

This stops a transient network blip from wiping out a good blocklist with an empty or near-empty one.

### Workflow scheduling

The hourly and daily workflows share a single GitHub Actions concurrency group (`siftblock-write`), so they can never run — or push — at the same time, even when their crons land on the same minute (midnight UTC). The daily-diff job also doesn't re-fetch sources itself; it reuses the `blocklist.txt` the hourly job just generated.

### Daily diff

Every day at midnight UTC, a second workflow compares the current blocklist against the previous day's snapshot and writes only the **newly observed domains** to `daily/YYYY-MM-DD.txt` — a running log of when domains first appeared.

---

## False positives

If a legitimate domain has been blocked, please [open an issue](https://github.com/zer0lightning/siftblock/issues) with the domain and a brief reason it should be removed — or add it to `config/whitelist.txt` yourself if it's your own fork.

---

## License & Disclaimer

See [DISCLAIMER.md](DISCLAIMER.md). Output is provided as-is with no warranty. Credit for the underlying threat-intel data belongs entirely to the upstream source maintainers.
