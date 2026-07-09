#!/usr/bin/env bash

set -euo pipefail

# ---------- User configuration (tune these) ----------
URL="${1:-}"                     # Target URL (required)
THREADS=6                        # wrk2 threads (increase for high RPS)
CONNECTIONS=300                 # "Maximum users" – adjust to your client limit
SCOUT_DURATION=60                # seconds for the breaking‑point test
SOAK_DURATION=300                # 5 minutes
SUSTAIN_PERCENT=0.80             # fraction of max RPS to use for the soak
# ----------------------------------------------------

if [[ -z "$URL" ]]; then
    echo "❌ ERROR: Please provide a URL as the first argument."
    echo "Usage: $0 <URL>"
    exit 1
fi

# Check if wrk2 is installed
if ! command -v wrk2 &> /dev/null; then
    echo "❌ wrk2 not found. Install it first:"
    echo "  - From source: https://github.com/giltene/wrk2"
    echo "  - Or via package manager (e.g., 'apt install wrk2' on some distros)"
    exit 1
fi

# Warn about OS limits if connections are high
if [[ "$CONNECTIONS" -gt 1024 ]]; then
    echo "⚠️  High connection count detected ($CONNECTIONS)."
    echo "   Ensure your OS limits are raised:"
    echo "   sudo ulimit -n 65535"
    echo "   Or add 'fs.file-max = 65535' to /etc/sysctl.conf"
    echo ""
fi

echo "=================================================="
echo " wrk2 Benchmark – Phase 1: Scout (finding ceiling)"
echo "=================================================="
echo "Target      : $URL"
echo "Connections : $CONNECTIONS (max users)"
echo "Duration    : ${SCOUT_DURATION}s"
echo "Target RPS  : 10,000,000 (intentionally over‑shot)"
echo "--------------------------------------------------"

# Run the scout with a ridiculously high -R to force max throughput.
# The tool will report the *actual* RPS it achieved.
SCOUT_OUTPUT=$(wrk2 -t"$THREADS" -c"$CONNECTIONS" -d"${SCOUT_DURATION}s" --latency -R10000000 "$URL" 2>&1)

# Extract the achieved Requests/sec from the output
MAX_RPS=$(echo "$SCOUT_OUTPUT" | grep -E "Requests/sec:" | awk '{print $2}')

if [[ -z "$MAX_RPS" ]]; then
    echo "❌ Failed to parse maximum RPS from scout run. Full output:"
    echo "$SCOUT_OUTPUT"
    exit 1
fi

# Check if the scout actually saturated the server
if (( $(echo "$MAX_RPS < 100" | bc -l) )); then
    echo "⚠️  Warning: Achieved RPS ($MAX_RPS) is very low. The server may be unreachable or rejecting connections."
    echo "   Please verify your URL and network."
    echo ""
fi

echo "✅ Scout complete. Maximum sustainable RPS = $MAX_RPS req/s"
echo ""

# ---------- Cooldown between phases ----------
echo "⏸️  Cooling down for 30s before soak phase..."
for i in $(seq 30 -1 1); do
    printf "\r   %2ds remaining..." "$i"
    sleep 1
done
printf "\r   ✅ Cooldown complete.        \n"
echo ""

# ---------- Phase 2: Long soak at ~90% capacity ----------
TARGET_RPS=$(echo "$MAX_RPS * $SUSTAIN_PERCENT" | bc | awk '{printf "%.0f", $0}')

echo "=================================================="
echo " wrk2 Benchmark – Phase 2: Soak (long‑term stability)"
echo "=================================================="
echo "Target      : $URL"
echo "Connections : $CONNECTIONS"
echo "Duration    : ${SOAK_DURATION}s"
SUSTAIN_PCT_DISPLAY=$(echo "$SUSTAIN_PERCENT * 100" | bc | awk '{printf "%.0f", $0}')
echo "Target RPS  : $TARGET_RPS (${SUSTAIN_PCT_DISPLAY}% of max)"
echo "--------------------------------------------------"
echo "⏳ Running soak test – this will take ${SOAK_DURATION}s..."
echo ""

# Run the actual soak test
# Tee output to a tmpfile so the user sees live progress AND we can parse results.
# Temporarily disable exit-on-error because wrk2 returns non-zero on timeouts/socket errors.
SOAK_TMPFILE=$(mktemp /tmp/wagtail-soak-XXXXXX.txt)
set +e
wrk2 -t"$THREADS" -c"$CONNECTIONS" -d"${SOAK_DURATION}s" --latency -R"$TARGET_RPS" "$URL" 2>&1 | tee "$SOAK_TMPFILE"
SOAK_EXIT_CODE=${PIPESTATUS[0]}
set -e
SOAK_OUTPUT=$(cat "$SOAK_TMPFILE")
rm -f "$SOAK_TMPFILE"

if [[ $SOAK_EXIT_CODE -ne 0 ]]; then
    echo ""
    echo "⚠️  wrk2 exited with code $SOAK_EXIT_CODE (due to timeouts/socket errors)."
    echo "   The results below reflect the test up until the failure point."
    echo ""
fi

# Extract key metrics from the soak run
# NOTE: || true prevents grep exit-code 1 (no match) from killing the script under set -e / pipefail
ACTUAL_RPS=$(echo "$SOAK_OUTPUT" | grep -E "Requests/sec:" | awk '{print $2}' || true)
LATENCY_AVG=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*Latency[[:space:]]+[0-9]" | awk '{print $2}' || true)
LATENCY_STDEV=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*Latency[[:space:]]+[0-9]" | awk '{print $3}' || true)
LATENCY_MAX=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*Latency[[:space:]]+[0-9]" | awk '{print $4}' || true)
LATENCY_50P=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*50\.000%" | awk '{print $2}' || true)
LATENCY_90P=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*90\.000%" | awk '{print $2}' || true)
LATENCY_99P=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*99\.000%" | awk '{print $2}' || true)
LATENCY_999P=$(echo "$SOAK_OUTPUT" | grep -E "^[[:space:]]*99\.900%" | awk '{print $2}' || true)
ERRORS=$(echo "$SOAK_OUTPUT" | grep -E "Socket errors" | head -1 | sed 's/.*Socket errors: //' || true)
TOTAL_REQ=$(echo "$SOAK_OUTPUT" | grep -E "requests in" | awk '{print $1}' || true)
TRANSFER=$(echo "$SOAK_OUTPUT" | grep -E "Transfer/sec:" | awk '{print $2}' || true)

echo ""
echo "================= FINAL RESULTS ================="
echo "Max RPS (ceiling)      : ${MAX_RPS:-N/A} req/s"
echo "Soak RPS (target)      : ${TARGET_RPS:-N/A} req/s"
echo "Soak RPS (achieved)    : ${ACTUAL_RPS:-N/A} req/s"
echo "Total requests         : ${TOTAL_REQ:-N/A}"
echo "Transfer rate          : ${TRANSFER:-N/A}/s"
echo ""
echo "Latency (average)      : ${LATENCY_AVG:-N/A}"
echo "Latency (stdev)        : ${LATENCY_STDEV:-N/A}"
echo "Latency (max)          : ${LATENCY_MAX:-N/A}"
echo "Latency (p50)          : ${LATENCY_50P:-N/A}"
echo "Latency (p90)          : ${LATENCY_90P:-N/A}"
echo "Latency (p99)          : ${LATENCY_99P:-N/A}"
echo "Latency (p99.9)        : ${LATENCY_999P:-N/A}"
echo "Socket errors          : ${ERRORS:-None}"
echo "✅ Benchmark complete."
