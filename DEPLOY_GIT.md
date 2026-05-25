Mister Wok — Git Deploy via cPanel
====================================

Repo: https://github.com/webklik/website.git  
Deploy root (live): `/home2/dykbsgmy/public_html/` → https://misterwok.net/  
Git repo root: this folder (`Mister_Wok_MNFVSS/`)

---

## DEPLOYPATH verification

Before the first deploy, confirm the path in Bluehost cPanel:

1. Log in to cPanel → **File Manager**
2. Open **public_html**
3. Check the path shown at the top of File Manager

It should be `/home2/dykbsgmy/public_html/`. If it differs, edit `.cpanel.yml` in this folder and update `DEPLOYPATH` before deploying.

---

## One-time cPanel setup (pull deployment)

1. **Backup** current `/public_html` (File Manager → select all → Compress → download zip).
2. cPanel → **Git Version Control** → **Create**.
3. Clone URL: `https://github.com/webklik/website.git`
4. Repository path: `/home2/dykbsgmy/repositories/website` (do **not** clone into `public_html`).
5. Ensure `.cpanel.yml` is on `main` in GitHub (see below).
6. Open the repo → **Pull or Deploy** tab:
   - Click **Update from Remote**
   - Click **Deploy HEAD Commit**
7. Purge LiteSpeed / full-page cache in cPanel.
8. Run the post-deploy checklist (bottom of this file).

---

## Ongoing workflow

On your PC (in this folder):

```bash
git add .
git commit -m "Describe your change"
git push origin main
```

In cPanel (each release):

1. Git Version Control → **Manage** your repo
2. **Pull or Deploy** → **Update from Remote**
3. **Deploy HEAD Commit**
4. Purge site cache
5. Spot-check live URLs (checklist below)

---

## What `.cpanel.yml` does

After **Deploy HEAD Commit**, cPanel runs:

- `rsync` from the cloned repo into `public_html`
- Includes dotfiles (e.g. `.htaccess`)
- Excludes: `.git`, `*.py` dev scripts, `_includes/`, `_frag_sig_grid_cc.html`, stray Capital duplicate

No `--delete` on first deploys — files on the server that are not in the repo are left in place. Add `--delete` to the rsync line only after the repo fully matches live content.

---

## Post-deploy verification

1. **Homepage:** https://misterwok.net/ loads
2. **Cache / IP policy:** after deploy, purge cache; verify:
   ```
   curl -s https://misterwok.net/ | findstr /i llms
   curl -s "https://misterwok.net/?deploy_check=1" | findstr /i llms
   ```
   Expect **no** output for both.
3. **Journal:** `/journal/` and article pages load
4. **Branch menus:** `/parklands/menu.html`, `/capital-centre/menu.html`, `/two-rivers/menu.html`
5. **Utility files:** `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/posts.json`
6. **Clean URLs:** a page without `.html` should work (`.htaccess` deployed)

---

## Optional: push deployment (auto on push to cPanel)

1. Create an **empty** repo in cPanel Git Version Control.
2. Add cPanel clone URL as a second remote: `git remote add cpanel <cpanel-clone-url>`
3. Push: `git push cpanel main`

After `.cpanel.yml` is present, pushes to the cPanel remote auto-run deploy tasks. Keep GitHub as `origin` for history.

---

## Troubleshooting

- **Deploy button missing:** ensure `.cpanel.yml` is committed at repo root on `main`.
- **404 on clean URLs:** `.htaccess` not copied — confirm rsync deploy ran; enable “Show Hidden Files” in File Manager.
- **Stale homepage:** purge LiteSpeed cache in cPanel, hard-refresh browser.
- **Deploy log:** `~/.cpanel/logs/vc_*_git_deploy.log` on the server (via SSH or cPanel terminal if available).
