# Deploying SiftBlock

This walks through taking the SiftBlock files and getting a live, self-updating blocklist running on GitHub Actions.

---

## 1. Prerequisites

- A GitHub account
- Git installed locally (or you can drag-and-drop files via the GitHub web UI instead — see note in Step 2)

---

## 2. Create the repository

Create a new **public** repository on GitHub (private repos work too, but `raw.githubusercontent.com` subscribe URLs require authentication for private repos — public is simplest for a DNS blocklist you intend to subscribe to from Pi-hole/AdGuard/etc).

```bash
git init
git remote add origin https://github.com/<your-username>/siftblock.git
git add .
git commit -m "Initial SiftBlock setup"
git branch -M main
git push -u origin main
```

> No git CLI? You can also create the repo on github.com, then use "Add file → Upload files" in the web UI to drag in everything, preserving the folder structure: `README.md`, `DISCLAIMER.md`, the `config/` folder, the `src/` folder, the `docs/` folder, and the `.github/workflows/` folder (the leading dot makes it hidden in some file pickers — make sure it actually uploads, GitHub's web uploader does support it).

The repo should end up looking like:

```
siftblock/
├── README.md
├── DISCLAIMER.md
├── config/
│   ├── keywords.txt
│   ├── whitelist.txt
│   ├── meta.txt
│   └── sources.txt
├── src/
│   ├── generate_blocklist.py
│   └── build_daily_header.py
├── docs/
│   └── DEPLOY.md
└── .github/
    └── workflows/
        ├── blocklist.yml
        └── blocklist-daily.yml
```

---

## 3. Give the workflow permission to commit

By default, GitHub Actions' built-in token is often read-only, which will make the "Commit and push" step fail. Fix it once:

1. Repo → **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **"Read and write permissions"**
4. **Save**

If this repo started life as a **fork**, GitHub also disables Actions by default — go to the **Actions** tab and click **"I understand my workflows, go ahead and enable them"** first.

---

## 4. Customize your keywords

Before (or after) your first run, edit the files under `config/`:

- **`config/keywords.txt`** — replace the example World Cup 2026 terms with your own brand/product/event terms
- **`config/whitelist.txt`** *(optional)* — domains that match a keyword but are actually legitimate/yours
- **`config/meta.txt`** *(optional)* — the Title/Description shown in your blocklist's header

Commit and push the changes (or edit directly on github.com — each save is a commit).

---

## 5. Trigger the first run

Two scheduled workflows are already configured (hourly build, daily diff), but you don't need to wait an hour to see it work:

1. Go to the **Actions** tab
2. Click **"Generate SiftBlock Blocklist"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"** (the green button)
4. Wait roughly 15–30 seconds, then refresh — the run should show a green checkmark

---

## 6. Verify

Open:

```
https://github.com/<your-username>/siftblock/blob/main/blocklist.txt
```

You should see a header block followed by a sorted domain list. Check the `# Number of entries:` line looks reasonable for your keywords. Note `blocklist.txt` is generated at the repo **root**, not inside `config/` or `src/` — that's intentional, so its URL never moves.

---

## 7. Subscribe

```
https://raw.githubusercontent.com/<your-username>/siftblock/main/blocklist.txt
```

| Platform | Instructions |
|---|---|
| **Pi-hole** | Group Management → Adlists → paste URL → Update Gravity |
| **AdGuard Home** | Filters → DNS Blocklists → Add blocklist → Custom |
| **uBlock Origin** | Settings → Filter lists → Import → paste URL |
| **Little Snitch** | New Rule Group → Subscribe → paste URL |

---

## 8. Ongoing operation

Nothing further to do — from here it runs itself:

- **Hourly:** `blocklist.yml` regenerates `blocklist.txt` and commits only if it changed
- **Daily (midnight UTC):** `blocklist-daily.yml` diffs against the previous day and writes `daily/YYYY-MM-DD.txt`
- **To change targets later:** just edit the files in `config/` anytime — no workflow or code changes needed, the next scheduled run picks it up

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Push step fails with a permissions error | Revisit Step 3 — workflow permissions not set to read/write |
| Workflow doesn't appear in the Actions tab at all | If this is a fork, Actions are disabled by default — enable them in the Actions tab |
| Run fails: `config/keywords.txt is missing or empty` | Add at least one keyword to `config/keywords.txt`, one per line |
| Run fails: `Only X/12 sources returned data` | A transient network issue or an upstream source being temporarily down — this is a safety guard, not a bug; nothing was overwritten, it'll just try again next hour |
| Run fails: `New entry count is less than 50% of the previous count` | The drop-ratio safety guard tripped — could be a real change or a fluke; check the Actions log for details. If you intentionally want to reset the baseline (e.g. after a big keyword change), you can manually delete `blocklist.txt` from the repo so there's no previous count to compare against |
| `blocklist.txt` didn't change after a run | Normal — the workflow only commits when the content actually changed |

---

## Optional: running locally instead of (or in addition to) GitHub Actions

```bash
git clone https://github.com/<your-username>/siftblock.git
cd siftblock
python3 src/generate_blocklist.py
```

Run this from the repo root (not from inside `src/`) — the script expects `config/` and writes `blocklist.txt` relative to your current directory. No extra dependencies beyond Python 3.10+. You could run this on your own cron instead of (or alongside) GitHub Actions if you'd rather self-host.
