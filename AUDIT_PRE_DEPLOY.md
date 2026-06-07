# Mister Wok — Pre-Deployment Audit Report
**Site:** misterwok.net  
**Conducted:** 2026-05-26  
**Mode:** READ-ONLY. No files were modified.  
**Auditor:** Claude (Lead Architect)  

---

## PHASE 1 — Directory Inventory

### Root-Level Files

| File | Status |
|---|---|
| `index.html` | ✅ APPROVED |
| `robots.txt` | ✅ APPROVED |
| `llms.txt` | ✅ APPROVED |
| `sitemap.xml` | ✅ APPROVED |
| `.htaccess` | ✅ APPROVED |
| `favicon.ico` | ✅ APPROVED |
| `404.html` | ✅ APPROVED (referenced by ErrorDocument) |
| `menu.html` | ✅ APPROVED (301 redirect stub → parklands/menu.html) |
| `catering.html` | ✅ APPROVED (published content page) |
| `social-proof.html` | ✅ APPROVED (published content page) |
| `videos.html` | ✅ APPROVED (published content page) |
| `menu.jsonld` | ✅ APPROVED (machine-readable asset, referenced in robots.txt) |
| `food-images.jsonld` | ⚠️ REVIEW — Include if referenced in production HTML; otherwise optional |
| `posts.json` | ⚠️ REVIEW — Verify if consumed by any client-side JS; if not, EXCLUDE |
| `DEPLOY_GIT.md` | 🚫 EXCLUDE FROM ZIP — Developer documentation, not web content |
| `_frag_sig_grid_cc.html` | 🚫 EXCLUDE FROM ZIP — HTML fragment, not a served page |
| `_includes/` | 🚫 EXCLUDE FROM ZIP — Build-time include fragments, not served |
| `__pycache__/` | 🚫 EXCLUDE FROM ZIP — Python bytecode |
| `.git/` | 🚫 EXCLUDE FROM ZIP — Version control internals |
| `.cpanel.yml` | ⚠️ REVIEW — Only needed for cPanel Git deployment; exclude for manual ZIP upload |
| `*.py` (12 scripts) | 🚫 EXCLUDE FROM ZIP — Local patch/audit scripts, never served |

### Root-Level Directories

| Directory | Status |
|---|---|
| `assets/` | ✅ APPROVED |
| `parklands/` | ✅ APPROVED |
| `capital-centre/` | ✅ APPROVED |
| `two-rivers/` | ✅ APPROVED |
| `journal/` | ✅ APPROVED |
| `images/` | ✅ INCLUDE — Not in approved list spec but contains all production WebP assets |
| `media/` | ⚠️ REVIEW — Contains only `.gitkeep` files; include only if video/reel files are added before deploy |

---

## PHASE 2 — robots.txt Audit

```
# Mister Wok — robots.txt
# Static HTML site crawl directives
# Last updated: 2026-05-10

# Default: allow crawl of public pages
User-agent: *
Allow: /
Disallow: /api/
Disallow: /cgi-bin/
Disallow: /tmp/

# AI/LLM crawlers are explicitly welcome to public content
User-agent: GPTBot
Allow: /
Allow: /llms.txt
Allow: /menu.jsonld

User-agent: ClaudeBot
Allow: /
Allow: /llms.txt
Allow: /menu.jsonld

User-agent: PerplexityBot
Allow: /
Allow: /llms.txt
Allow: /menu.jsonld

User-agent: OAI-SearchBot
Allow: /
Allow: /llms.txt
Allow: /menu.jsonld

# Keep discovery explicit for all crawlers
Sitemap: https://misterwok.net/sitemap.xml
```

| Check | Verdict |
|---|---|
| File exists at root | ✅ PASS |
| `User-agent: *` block present | ✅ PASS |
| Disallows sensitive paths | ✅ PASS (`/api/`, `/cgi-bin/`, `/tmp/`) |
| `Sitemap:` directive to live domain | ✅ PASS (`https://misterwok.net/sitemap.xml`) |
| No localhost references | ✅ PASS |
| No `Disallow: /` blocking whole site | ✅ PASS |
| Dev files disallowed (`_includes/`, `*.py`) | ⚠️ WARN — Not disallowed, but these files should not be in the ZIP so the server will never serve them |

**Overall: PASS**

---

## PHASE 3 — llms.txt Audit

*(Full contents above — 350+ lines. Key sections verified below.)*

| Check | Verdict |
|---|---|
| File exists at root | ✅ PASS |
| `# Mister Wok` title block | ✅ PASS |
| Branch context with phones | ✅ PASS (Parklands +254 724 100 100, Capital Centre +254 722 248 248, Two Rivers +254 753 222 222) |
| GloriaFood order links per branch | ✅ PASS (67_y_m / d_yq_g / k8_d_z) |
| Menu data pointers / RAG content | ✅ PASS (menu.jsonld reference + 11-dish signature table with prices) |
| No placeholder / TODO text | ✅ PASS |
| Canonical domain `https://misterwok.net` | ✅ PASS |
| **Stale dish count in Website Pages table** | ⚠️ WARN — Line reads `138 dishes, KES prices` for the Full Menu entry. Should reference 229 dishes (Parklands) and note branch menus exist. Non-blocking for deploy. |

**Overall: PASS with 1 WARN**

---

## PHASE 4 — JPEG / Non-WebP Image Audit

### No `.jpg`/`.jpeg`/`.png`/`.gif` files exist on disk ✅

All 47 raster image files in `images/food/` and `images/restaurant/` are `.webp`. Clean.

### JPEG references found in HTML meta tags (not `<img src>`)

These are OG/Twitter social share `<meta>` tags. They do not affect page rendering but will produce broken social preview cards if the referenced files are not on the server.

| File | Line | Reference | Impact |
|---|---|---|---|
| `catering.html` | 43 | `og:image` → `images/mister-wok-catering.jpg` | Broken social preview |
| `catering.html` | 48 | `twitter:image` → `images/mister-wok-catering.jpg` | Broken social preview |
| `index.html` | 82 | JSON-LD `logo` → `images/logo.png` | ⚠️ Schema logo missing |
| `journal/ntv-am-live-mister-wok-2014.html` | 44 | `og:image` → `images/mister-wok-ntv-thumb.jpg` | Broken social preview |
| `journal/ntv-am-live-mister-wok-2014.html` | 49 | `twitter:image` → `images/mister-wok-ntv-thumb.jpg` | Broken social preview |
| `social-proof.html` | 43 | `og:image` → `images/mister-wok-nairobi.jpg` | Broken social preview |
| `social-proof.html` | 48 | `twitter:image` → `images/mister-wok-nairobi.jpg` | Broken social preview |
| `videos.html` | 43 | `og:image` → `images/mister-wok-nairobi.jpg` | Broken social preview |
| `videos.html` | 48 | `twitter:image` → `images/mister-wok-nairobi.jpg` | Broken social preview |

**Verdict: WARN** — No `<img src>` JPEG references (pages render correctly). Social share images and JSON-LD logo reference non-existent files. Recommend converting/creating `.webp` equivalents before deploy if social sharing matters.

> **Action required:** Create `images/mister-wok-catering.webp`, `images/mister-wok-nairobi.webp`, `images/mister-wok-ntv-thumb.webp`, `images/logo.webp` and update the 9 meta tag references. Or upload the JPGs/PNGs as-is if already available. The logo.png is particularly important for Google rich results.

---

## PHASE 5 — .htaccess Audit

*(Full contents in project file — 180 lines. Key checks below.)*

| Check | Verdict | Notes |
|---|---|---|
| `RewriteEngine On` | ✅ PASS | Present |
| HTTPS redirect (HTTP → HTTPS) | ✅ PASS | `RewriteCond %{HTTPS} off` + `R=301,L` |
| www → non-www canonical redirect | ✅ PASS | `RewriteCond %{HTTP_HOST} ^www\.` + `R=301,L` |
| Trailing slash removal | ✅ PASS | `RewriteCond !-d` + `/$1 [R=301,L]` |
| Browser caching — WebP, CSS, JS, fonts | ✅ PASS | `mod_expires` + `Cache-Control` headers, 1yr for CSS/JS/fonts, 30d for images |
| GZIP compression (`mod_deflate`) | ✅ PASS | Covers HTML, CSS, JS, JSON, LD+JSON, SVG, XML |
| `X-Content-Type-Options: nosniff` | ✅ PASS | Present |
| `X-Frame-Options: SAMEORIGIN` | ✅ PASS | Present |
| `Referrer-Policy: strict-origin-when-cross-origin` | ✅ PASS | Present |
| `Permissions-Policy` header | ❌ FAIL | Absent — add to harden browser feature policy. Non-blocking for deploy. |
| HSTS (`Strict-Transport-Security`) | ⚠️ WARN | Commented out — intentional (awaiting HTTPS stability confirmation). Uncomment after 30 days live. |
| Custom 404 error page | ✅ PASS | `ErrorDocument 404 /404.html` |
| No cPanel default paths | ✅ PASS | No `/home/username/` references |
| `X-Robots-Tag: noindex` on llms.txt | ✅ PASS | `<Files "llms.txt">` block present |
| Stale comment: "138-dish menu" | ⚠️ WARN | Line 36 comment reads "canonical 138-dish menu" — cosmetic, non-functional |

**Suggested addition for `Permissions-Policy`:**
```apache
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
```

**Overall: PASS with 1 FAIL (non-blocking) + 2 WARNs**

---

## PHASE 6 — Journal / Article Pages Audit

| File | Content Chars | Empty Shell? | Chin Present? | Gold Token | DM Sans | JPEG in `<img>`? |
|---|---|---|---|---|---|---|
| `birthday-catering-guide.html` | 6,038 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `decade-at-the-flame.html` | 4,993 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `halal-wok-nairobi.html` | 4,434 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `index.html` (journal hub) | 2,845 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `long-grain-aromatic-rice.html` | 4,737 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `ntv-am-live-mister-wok-2014.html` | 935 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ⚠️ OG/Twitter meta only (lines 44, 49) |
| `spring-rolls-gold-prosperity.html` | 5,052 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |
| `wok-hei-physics.html` | 8,267 | ✅ NO | ✅ YES | ✅ PASS | ✅ YES | ✅ CLEAN |

**All 8 journal pages: PASS**  
Single note: `ntv-am-live-mister-wok-2014.html` has OG/Twitter JPEG meta refs (already flagged in Phase 4). No `<img src>` JPEG references on any journal page.

---

## PHASE 7 — Branch Menu Pages Audit

| Check | `capital-centre/menu.html` | `two-rivers/menu.html` |
|---|---|---|
| File exists | ✅ YES | ✅ YES |
| `<details name="menu-groups">` accordion | ✅ YES (20 instances) | ✅ YES (17 instances) |
| The Chin sticky bottom nav | ✅ YES (8 elements) | ✅ YES (8 elements) |
| `page_type` DataLayer push | ✅ `'menu'` | ✅ `'menu'` |

**Both branch menus: PASS — fully upgraded, not out-of-scope**

---

## PHASE 8 — ZIP Exclusion Manifest

### FILES / FOLDERS TO EXCLUDE FROM DEPLOYMENT ZIP

```
EXCLUDE  .git/                              # Version control — never upload
EXCLUDE  __pycache__/                       # Python bytecode cache
EXCLUDE  .cursor/                           # IDE metadata
EXCLUDE  _includes/                         # Build-time HTML fragments — not served
EXCLUDE  _frag_sig_grid_cc.html            # HTML fragment — not a routable page
EXCLUDE  DEPLOY_GIT.md                     # Developer documentation
EXCLUDE  AUDIT_PRE_DEPLOY.md               # Pre-deploy audit report
EXCLUDE  cpanel-sync-deploy.sh             # Deploy helper script
EXCLUDE  serve_local.py                    # Local dev server
EXCLUDE  .cpanel.yml                       # cPanel Git deploy config — not needed for ZIP upload
EXCLUDE  *.py (all scripts)                # Local patch/generation/audit scripts
EXCLUDE  kula_cooler_transcripts.json      # Pipeline output (~3.5 MB)
EXCLUDE  kula_cooler_failed.json           # Pipeline output
EXCLUDE  mw_mentions.json                  # Pipeline output
EXCLUDE  mw_mentions_output.txt            # Pipeline output
EXCLUDE  playlist_urls.txt                 # Pipeline output
EXCLUDE  posts.json                        # No runtime consumer in HTML/JS
EXCLUDE  food-images.jsonld                # Not linked from production HTML
EXCLUDE  assets/css/.gitkeep              # Git placeholder — empty file
EXCLUDE  assets/js/.gitkeep               # Git placeholder — empty file
EXCLUDE  images/food/.gitkeep             # Git placeholder — empty file
EXCLUDE  images/restaurant/.gitkeep       # Git placeholder — empty file
EXCLUDE  images/social/.gitkeep           # Git placeholder — empty file
EXCLUDE  images/team/.gitkeep             # Git placeholder — empty file
EXCLUDE  media/reels/.gitkeep             # Git placeholder — empty file
EXCLUDE  media/videos/.gitkeep            # Git placeholder — empty file
REVIEW   media/                            # Include only if video files exist; currently empty
```

### AFFIRMATIVE KEEP LIST (everything that SHOULD be in the ZIP)

```
KEEP  index.html
KEEP  404.html
KEEP  robots.txt
KEEP  llms.txt
KEEP  sitemap.xml
KEEP  .htaccess
KEEP  favicon.ico
KEEP  catering.html
KEEP  social-proof.html
KEEP  videos.html
KEEP  menu.html                            (redirect stub)
KEEP  menu.jsonld
KEEP  assets/css/site-footer.css
KEEP  assets/css/site-nav.css
KEEP  assets/js/engine.js
KEEP  assets/js/menu-photos.js
KEEP  images/food/*.webp                   (40 files)
KEEP  images/restaurant/*.webp             (7 files)
KEEP  parklands/index.html
KEEP  parklands/menu.html
KEEP  capital-centre/index.html
KEEP  capital-centre/menu.html
KEEP  two-rivers/index.html
KEEP  two-rivers/menu.html
KEEP  journal/index.html
KEEP  journal/birthday-catering-guide.html
KEEP  journal/decade-at-the-flame.html
KEEP  journal/halal-wok-nairobi.html
KEEP  journal/long-grain-aromatic-rice.html
KEEP  journal/ntv-am-live-mister-wok-2014.html
KEEP  journal/spring-rolls-gold-prosperity.html
KEEP  journal/wok-hei-physics.html
```

**Total: ~58 files + 47 WebP images**

---

## PHASE 9 — Deployment Readiness Verdict

| Check | Status | Blocker? | Notes |
|---|---|---|---|
| robots.txt valid | ✅ PASS | Yes | Sitemap directive present, no `Disallow: /` |
| llms.txt valid | ⚠️ WARN | No | Stale "138 dishes" count in pages table |
| No JPEG `<img src>` references | ✅ PASS | Yes | All `<img>` tags use `.webp` |
| OG/Twitter meta images exist on disk | ❌ FAIL | No | 4 referenced jpg/png files not on disk — social previews will break |
| JSON-LD logo file exists | ❌ FAIL | No | `images/logo.png` referenced in index.html schema, file absent |
| .htaccess HTTPS redirect | ✅ PASS | Yes | HTTP→HTTPS + www→non-www both present |
| .htaccess caching rules | ✅ PASS | No | 1yr CSS/JS/fonts, 30d images |
| .htaccess security headers | ⚠️ WARN | No | `Permissions-Policy` absent; HSTS commented out |
| Custom 404 page | ✅ PASS | Yes | `ErrorDocument 404 /404.html` |
| No empty journal shells | ✅ PASS | No | All 8 articles have 900+ characters of content |
| Chin present on all journal pages | ✅ PASS | Yes | 6–8 chin elements on every journal page |
| Gold token consistent | ✅ PASS | No | No orange rgba values detected in any page |
| Branch menus upgraded | ✅ PASS | No | Both capital-centre and two-rivers fully upgraded with accordion + chin |
| ZIP exclusion list ready | ✅ PASS | Yes | See Phase 8 |

---

### PRE-DEPLOY ACTION LIST (ordered by priority)

| # | Action | Priority |
|---|---|---|
| 1 | Create or upload `images/logo.png` (or `.webp` + update JSON-LD ref) | HIGH — affects Google rich results |
| 2 | Create/upload `images/mister-wok-nairobi.jpg`, `mister-wok-catering.jpg`, `mister-wok-ntv-thumb.jpg` OR update meta tags to existing `.webp` equivalents | MEDIUM — social share previews |
| 3 | Delete `.git/index.lock` from Windows, then run `git add -A && git commit` | HIGH — locks out git until cleared |
| 4 | Update `llms.txt` Website Pages table: "138 dishes" → "229 dishes (Parklands), 138 dishes (Capital Centre / Two Rivers)" | LOW |
| 5 | Add `Permissions-Policy` header to `.htaccess` | LOW |
| 6 | After 30 days HTTPS stable, uncomment HSTS line in `.htaccess` | POST-DEPLOY |
| 7 | Fix `.htaccess` comment line 36: "138-dish menu" → "229-dish menu" (cosmetic) | LOW |

---

## OVERALL VERDICT

> **⚠️ READY TO DEPLOY WITH KNOWN GAPS — 0 hard blockers found**

The site is deployable as-is. Pages render correctly, all images resolve, menus are complete, security headers are in place, and the Chin nav is present throughout. The two FAILs (missing OG image files and logo.png) are pre-existing gaps that affect social sharing and Google schema logo display respectively — neither will cause a broken page load or white screen.

Recommend uploading the missing social image assets alongside the ZIP for a clean launch.

---

*Audit conducted by Claude Code — Read-only. No files were modified.*
