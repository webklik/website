#!/bin/bash
# Run in cPanel Terminal — sync bare repo to GitHub main, then deploy in UI.
# Path: /home2/dykbsgmy/repositories/mw-website
set -e
cd /home2/dykbsgmy/repositories/mw-website
git fetch origin
git reset --hard origin/main
git clean -fd
echo ""
echo "Clone synced. HEAD is now:"
git log -1 --oneline
echo ""
echo "Next steps (cPanel UI):"
echo "  1. Git Version Control → Deploy HEAD Commit"
echo "  2. LiteSpeed Web Cache Manager → Purge All"
echo ""
echo "Expected Last Deployed SHA: cd12bc1 (includes SEO sprint f6e886c)"
