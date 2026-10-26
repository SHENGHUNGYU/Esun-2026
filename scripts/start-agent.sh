#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
uv sync --frozen
agent_tunnel_pid=''
cleanup() {
    if [ -n "$agent_tunnel_pid" ]; then kill "$agent_tunnel_pid" 2>/dev/null || true; fi
}
trap cleanup EXIT HUP INT TERM
if ! curl --fail --silent --max-time 3 http://127.0.0.1:11435/api/tags >/dev/null; then
    ssh -N -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=8 \
        -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 \
        -L 127.0.0.1:11435:127.0.0.1:11434 nelson@120.107.172.133 &
    agent_tunnel_pid=$!
    agent_ready=false
    for agent_attempt in 1 2 3 4 5 6 7 8 9 10; do
        if curl --fail --silent --max-time 2 http://127.0.0.1:11435/api/tags >/dev/null; then agent_ready=true; break; fi
        sleep 1
    done
    if [ "$agent_ready" != true ]; then echo '模型 SSH 通道未建立，請依 AGENTS.md 檢查連線。' >&2; exit 1; fi
fi
uv run --frozen esun-agent --root "${ESUN_DATA_ROOT:-artifacts/live-20261024}" --port "${ESUN_APP_PORT:-8766}" --ssh-host 120.107.172.133 --history-root "${ESUN_HISTORY_ROOT:-artifacts/history-202604-202609}"
