Mister Wok — Git Deploy via cPanel (GitHub → Live)
===================================================

**Stop using ZIP uploads to `public_html`.** Use this pipeline instead.

```
Your PC (edit files)
    → git commit + push
        → GitHub (webklik/website)
            → cPanel Git clone (repositories/mw-website)
                → Deploy HEAD Commit (.cpanel.yml runs rsync)
                    → public_html (https://misterwok.net)
```

| Layer | Path / URL |
|-------|------------|
| GitHub repo | https://github.com/webklik/website.git |
| cPanel clone (do **not** edit live here manually) | `/home2/dykbsgmy/repositories/mw-website` |
| Live site (what visitors see) | `/home2/dykbsgmy/public_html/` → https://misterwok.net/ |
| Local PC folder | `Mister_Wok_MNFVSS/` |

---

## Why Git deploy beats ZIP upload

| ZIP upload to File Manager | Git + `.cpanel.yml` |
|----------------------------|---------------------|
| Overwrites everything you select | **rsync** copies only changed files |
| Resets `Last-Modified` on all touched files | Untouched live files keep old dates |
| No history / hard to rollback | Every release is a Git commit |
| Easy to miss `.htaccess` or dotfiles | Dotfiles deploy automatically |
| Manual, error-prone | Repeatable 4-step workflow |

---

## One-time cPanel setup (already done — verify)

In cPanel → **Git Version Control** → **Manage** `mw-website`:

| Field | Value |
|-------|-------|
| Clone URL | `https://github.com/webklik/website.git` |
| Repository path | `/home2/dykbsgmy/repositories/mw-website` |
| Branch | `main` |

Confirm `.cpanel.yml` exists at:

`/home2/dykbsgmy/repositories/mw-website/.cpanel.yml`

(File Manager → Show Hidden Files → open `repositories/mw-website`)

---

## Fix “The system cannot deploy” (run once if button is greyed out)

cPanel requires **both**:

1. Valid `.cpanel.yml` at repo root — already on GitHub and in your clone.
2. **Clean working tree** — no uncommitted changes in the server clone.

In cPanel → **Terminal**:

```bash
cd /home2/dykbsgmy/repositories/mw-website
git status
```

If anything shows as modified or untracked:

```bash
git fetch origin
git reset --hard origin/main
git clean -fd
git status
```

Expected: `nothing to commit, working tree clean`

Then in **Git Version Control → Pull or Deploy**:

1. **Update from Remote** (pulls latest from GitHub)
2. **Deploy HEAD Commit** (should now be enabled)
3. **LiteSpeed Web Cache Manager → Purge All**

`git reset --hard` only resets the **clone** under `repositories/mw-website`. It does not change `public_html` until you click **Deploy HEAD Commit**.

---

## Your workflow for every change (4 steps)

### Step 1 — Edit on your PC

Work in `Mister_Wok_MNFVSS/`. Do **not** edit files directly in cPanel `public_html` for routine changes.

Dev-only files (never go live — excluded by `.cpanel.yml`):

- `*.py`, `__pycache__/`, `_includes/`, `DEPLOY_GIT.md`

### Step 2 — Commit and push to GitHub

In PowerShell, from the project folder:

```powershell
cd "C:\Users\HUSSEIN\Desktop\Mister_Wok_Website\Mister_Wok_MNFVSS"
git add path/to/changed/files
git status
git commit -m "Describe what changed and why"
git push origin main
```

Use `git add` on specific files (not blind `git add .`) to avoid committing dev junk.

### Step 3 — Pull and deploy in cPanel

1. **Git Version Control** → Manage `mw-website`
2. **Pull or Deploy** tab
3. **Update from Remote** — HEAD should match your latest GitHub commit
4. **Deploy HEAD Commit** — runs rsync into `public_html`
5. If deploy fails with “uncommitted changes”, run the Terminal fix above, then retry

### Step 4 — Purge cache and verify

1. **LiteSpeed Web Cache Manager → Purge All**
2. Hard-refresh browser (Ctrl+Shift+R)
3. Spot-check:

```powershell
curl.exe -sI "https://misterwok.net/" | findstr "HTTP"
curl.exe -s "https://misterwok.net/parklands/" | Select-String "LocalBusiness"
curl.exe -sI "https://misterwok.net/llms.txt" | findstr "X-Robots-Tag"
```

Use `curl.exe` — not PowerShell `curl` (that alias hangs).

---

## What `.cpanel.yml` does on Deploy HEAD Commit

```yaml
---
deployment:
  tasks:
    - export DEPLOYPATH=/home2/dykbsgmy/public_html/
    - /usr/bin/rsync -av ... ./ $DEPLOYPATH
```

- Copies repo files → `public_html`
- **Incremental:** only changed files transfer; unchanged server files keep old timestamps
- **Includes** dotfiles (`.htaccess`, etc.)
- **Excludes:** `.git`, `*.py`, `_includes/`, stray duplicates
- **No `--delete` yet** — orphan files on the server that aren't in the repo are left in place

---

## Sitemap tip (preserve “dynamic site” signals)

Do **not** run `generate_sitemap.py` before every deploy unless you want all `<lastmod>` dates refreshed.

Instead: update `<lastmod>` in `sitemap.xml` only for URLs whose HTML actually changed.

---

## Rollback

**Option A — Git revert (preferred)**

```powershell
git revert HEAD
git push origin main
```

Then cPanel: Update from Remote → Deploy HEAD Commit → purge cache.

**Option B — Restore from backup zip**

Use your pre-deploy zip only for emergency restore of specific files — not for routine releases.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Deploy button greyed out | Terminal: `git reset --hard origin/main && git clean -fd` |
| HEAD commit old after pull | Confirm branch = `main`; click Update from Remote again |
| Live site stale after deploy | Purge LiteSpeed cache; hard-refresh |
| 404 on clean URLs | `.htaccess` missing from `public_html` — redeploy; Show Hidden Files in File Manager |
| Changes on PC not on live | Did you push to GitHub **and** Deploy HEAD Commit in cPanel? Both are required |
| Deploy log | cPanel Terminal: `ls -lt ~/.cpanel/logs/vc_*_git_deploy.log \| head -3` |

---

## Optional: auto-deploy on push (advanced)

Add cPanel as a second Git remote so push triggers deploy without clicking in cPanel:

```powershell
git remote add cpanel <cpanel-clone-url-from-Git-Version-Control>
git push cpanel main
```

Keep `origin` → GitHub for history. Only set this up after manual deploy works reliably.

The `cpanel` remote is already configured locally:

```powershell
git remote -v
# cpanel  ssh://dykbsgmy@misterwok.net/home2/dykbsgmy/repositories/mw-website
```

If push fails with "Too many authentication failures", use an explicit key:

```powershell
$env:GIT_SSH_COMMAND = 'ssh -i C:\Users\HUSSEIN\.ssh\YOUR_KEY -o IdentitiesOnly=yes'
git push cpanel main
```

---

## SHA verification (every release)

Before considering a release live, confirm all three layers show the **same commit SHA**:

```powershell
# Local PC
git log -1 --oneline

# GitHub (after push)
git ls-remote origin main

# cPanel — Git Version Control → Last Deployed SHA
```

**Golden rule:** Never click **Deploy HEAD Commit** without **Update from Remote** first. Deploying a stale SHA re-pushes old `.htaccess` and can cause a site-wide 403.

If cPanel SHA ≠ GitHub SHA, reset the server clone before deploy:

```bash
cd /home2/dykbsgmy/repositories/mw-website
git fetch origin
git reset --hard origin/main
git clean -fd
git log -1 --oneline
```

Then **Deploy HEAD Commit** in cPanel UI (or `git push cpanel main` if SSH auto-deploy is configured).

---

## Current release status

Latest commit on GitHub `main`:

`f6e886c` — SEO remediation sprint + LiteSpeed-safe `.htaccess` (Files blocks for AI assets)

Includes commits since Phase 1B deploy (`1786cda`):

- `eb1305c` — fix sensitive-files `FilesMatch` (403)
- `6cb439b` — ASCII-only `.htaccess` comments (403)
- `f44d427` — halal-assured copy, 229 dishes, sitemap cleanup, noindex pages
- `f6e886c` — per-file `<Files>` for llms.txt / menu.jsonld / entity-map.json

After cPanel **Deploy HEAD Commit**, verify live:

```powershell
curl.exe -sI "https://misterwok.net/" | Select-String "HTTP"
curl.exe -sI "https://misterwok.net/sitemap.xml" | Select-String "HTTP"
curl.exe -s "https://misterwok.net/parklands/" | Select-String "Halal-assured wok kitchen"
curl.exe -s "https://misterwok.net/parklands/" | Select-String "<strong>229</strong> dishes"
curl.exe -s "https://misterwok.net/sitemap.xml" | Select-String "locations"
```

Expected: site and sitemap return **200**; Parklands shows Halal-assured meta and 229 dishes; sitemap has `/locations/` and no `llms.txt`, `menu.jsonld`, or `entity-map.json`.
