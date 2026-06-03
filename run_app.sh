#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"
mkdir -p "$RUN_DIR"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

BACKEND_PID_FILE="$RUN_DIR/backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/frontend.pid"
BACKEND_LOG="$RUN_DIR/backend.log"
FRONTEND_LOG="$RUN_DIR/frontend.log"

is_port_listening() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -i :"$port" -sTCP:LISTEN -t >/dev/null 2>&1
  elif command -v nc >/dev/null 2>&1; then
    nc -z 127.0.0.1 "$port" >/dev/null 2>&1
  elif command -v ss >/dev/null 2>&1; then
    ss -ltn "( sport = :$port )" 2>/dev/null | tail -n +2 | grep -q .
  else
    python3 -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', $port))" >/dev/null 2>&1
  fi
}

start_backend() {
  if is_port_listening "$BACKEND_PORT"; then
    echo "Backend already listening on :$BACKEND_PORT"
    return
  fi

  (
    cd "$ROOT_DIR/backend"
    PORT="$BACKEND_PORT" bash ./start.sh >"$BACKEND_LOG" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
  )

  local count=0
  local max_wait=15
  while ! is_port_listening "$BACKEND_PORT"; do
    if [ "$count" -ge "$max_wait" ]; then
      echo "Backend failed to start within ${max_wait}s. Check log: $BACKEND_LOG"
      exit 1
    fi
    sleep 1
    count=$((count + 1))
  done
  echo "Started backend on :$BACKEND_PORT"
}

start_frontend() {
  if is_port_listening "$FRONTEND_PORT"; then
    echo "Frontend already listening on :$FRONTEND_PORT"
    return
  fi

  (
    cd "$ROOT_DIR/frontend"
    VITE_API_URL="http://localhost:$BACKEND_PORT" npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT" >"$FRONTEND_LOG" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"
  )

  local count=0
  local max_wait=15
  while ! is_port_listening "$FRONTEND_PORT"; do
    if [ "$count" -ge "$max_wait" ]; then
      echo "Frontend failed to start within ${max_wait}s. Check log: $FRONTEND_LOG"
      exit 1
    fi
    sleep 1
    count=$((count + 1))
  done
  echo "Started frontend on :$FRONTEND_PORT"
}

stop_by_pid_file() {
  local pid_file="$1"
  local name="$2"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name pid file not found."
    return
  fi

  local pid
  pid="$(cat "$pid_file" || true)"
  if [[ -z "$pid" ]]; then
    rm -f "$pid_file"
    return
  fi

  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
    echo "Stopped $name (pid: $pid)"
  else
    echo "$name process not running (stale pid: $pid)"
  fi
  rm -f "$pid_file"
}

status() {
  echo "Backend URL : http://localhost:$BACKEND_PORT"
  echo "Frontend URL: http://localhost:$FRONTEND_PORT"
  echo

  if is_port_listening "$BACKEND_PORT"; then
    echo "Backend: UP"
    curl -sS "http://127.0.0.1:$BACKEND_PORT/health" || true
    echo
  else
    echo "Backend: DOWN"
  fi

  if is_port_listening "$FRONTEND_PORT"; then
    echo "Frontend: UP"
  else
    echo "Frontend: DOWN"
  fi
}

show_logs() {
  echo "=== Backend Log ($BACKEND_LOG) ==="
  tail -n 40 "$BACKEND_LOG" 2>/dev/null || echo "No backend log yet."
  echo
  echo "=== Frontend Log ($FRONTEND_LOG) ==="
  tail -n 40 "$FRONTEND_LOG" 2>/dev/null || echo "No frontend log yet."
}

start_all() {
  start_backend
  start_frontend
  echo
  status
}

stop_all() {
  stop_by_pid_file "$FRONTEND_PID_FILE" "frontend"
  stop_by_pid_file "$BACKEND_PID_FILE" "backend"
}

usage() {
  cat <<EOF
Usage: ./run_app.sh [start|stop|restart|status|logs]

Env overrides:
  BACKEND_PORT (default: 8000)
  FRONTEND_PORT (default: 5173)
EOF
}

ACTION="${1:-start}"
case "$ACTION" in
  start)
    start_all
    ;;
  stop)
    stop_all
    ;;
  restart)
    stop_all
    start_all
    ;;
  status)
    status
    ;;
  logs)
    show_logs
    ;;
  *)
    usage
    exit 1
    ;;
esac
