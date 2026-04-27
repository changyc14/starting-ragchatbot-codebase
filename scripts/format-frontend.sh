#!/usr/bin/env bash
# Auto-format frontend files with Prettier
set -e

FRONTEND_DIR="$(cd "$(dirname "$0")/../frontend" && pwd)"

echo "=== Formatting Frontend Files ==="
echo ""

cd "$FRONTEND_DIR"

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
  echo ""
fi

echo "Running Prettier..."
npx prettier --write "*.{js,css,html}"
echo ""
echo "=== Done ==="