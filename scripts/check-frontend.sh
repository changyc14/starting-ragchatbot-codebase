#!/usr/bin/env bash
# Frontend quality checks: formatting + linting
set -e

FRONTEND_DIR="$(cd "$(dirname "$0")/../frontend" && pwd)"

echo "=== Frontend Quality Checks ==="
echo ""

cd "$FRONTEND_DIR"

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
  echo ""
fi

echo "--- Prettier (format check) ---"
npx prettier --check "*.{js,css,html}"
echo "Formatting: OK"
echo ""

echo "--- ESLint (lint check) ---"
npx eslint *.js
echo "Linting: OK"
echo ""

echo "=== All checks passed ==="