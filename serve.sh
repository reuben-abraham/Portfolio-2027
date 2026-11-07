#!/usr/bin/env bash
# Local static server for the recovered redesign (redesign-recovered @ ff26894).
# Usage: ./serve.sh            # default http://127.0.0.1:8080/
#        PORT=8090 ./serve.sh
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8080}"
BIND="${BIND:-127.0.0.1}"
echo "Serving $(pwd) at http://${BIND}:${PORT}/  (ctrl-c to stop)"
exec python3 -m http.server "$PORT" --bind "$BIND"
