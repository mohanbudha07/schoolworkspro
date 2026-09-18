#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export SWP_DB="${SWP_DB:-/tmp/schoolworkspro.db}"

echo "Starting API on :8000"
cd "$ROOT/backend"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
API_PID=$!

echo "Starting web on :5173"
cd "$ROOT/frontend"
npm run dev -- --host 127.0.0.1 --port 5173 &
WEB_PID=$!

trap 'kill $API_PID $WEB_PID 2>/dev/null || true' EXIT
wait
