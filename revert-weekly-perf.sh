#!/bin/bash
# Revert the weekly perf report to its pre-week-switcher state.
# Restores the canonical w/e 31 May report from its index-original.html backup
# and removes the in-progress folder.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$DIR/31may2026/index-original.html" ]; then
  cp "$DIR/31may2026/index-original.html" "$DIR/31may2026/index.html"
  echo "✓ restored $DIR/31may2026/index.html from backup"
fi
if [ -d "$DIR/wip-2jun2026" ]; then
  rm -rf "$DIR/wip-2jun2026"
  echo "✓ removed $DIR/wip-2jun2026/"
fi
echo "Done. To re-enable the week switcher, rerun:"
echo "  python3 ~/Downloads/handover-report-kit/add_week_switcher.py"
