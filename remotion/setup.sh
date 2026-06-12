#!/usr/bin/env bash
# Run this from inside the remotion/ directory:
#   cd remotion && bash setup.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGES_SRC="$REPO_ROOT/players/images"
PUBLIC_DIR="$SCRIPT_DIR/public"

echo "=== 1. Copying player images to public/ ==="
mkdir -p "$PUBLIC_DIR"
count=0
for img in "$IMAGES_SRC"/*.jpg "$IMAGES_SRC"/*.jpeg "$IMAGES_SRC"/*.png; do
  [ -f "$img" ] || continue
  cp "$img" "$PUBLIC_DIR/"
  echo "  ✓ $(basename "$img")"
  ((count++)) || true
done
echo "  Copied $count images."

echo ""
echo "=== 2. Installing npm dependencies ==="
npm install

echo ""
echo "=== 3. Ready! ==="
echo "To preview:  npm start"
echo "To render:   npm run render"
echo ""
echo "Output will be at: out/world_cup_short.mp4"
