#!/bin/sh
set -eu

echo "[*] FreeBSD tuning (512MB MAX PERFORMANCE SAFE MODE)"

LOADER="/boot/loader.conf"
SYSCTL="/etc/sysctl.conf"

add_loader() {
    grep -q "^$1=" "$LOADER" 2>/dev/null || echo "$1=\"$2\"" >> "$LOADER"
}

add_sysctl() {
    grep -q "^$1=" "$SYSCTL" 2>/dev/null || echo "$1=$2" >> "$SYSCTL"
}

# =========================
# PHASE 1 — BOOT (CRITICAL)
# =========================
echo "[*] loader.conf tuning"

# ---- ZFS ARC (reduced for safety) ----
add_loader vfs.zfs.arc.max 96M

# ---- mbufs (controlled) ----
add_loader kern.ipc.nmbclusters 131072

# ---- accept queue ----
add_loader kern.ipc.soacceptqueue 8192

# ---- syncache (burst protection) ----
add_loader net.inet.tcp.syncache.hashsize 4096
add_loader net.inet.tcp.syncache.bucketlimit 200

# ---- TCP hash tuning ----
add_loader net.inet.tcp.tcbhashsize 4096

# ---- nginx accept filters ----
add_loader accf_http_load YES
add_loader accf_data_load YES

# ---- ISR (CRITICAL for 1 CPU) ----
add_loader net.isr.bindthreads 1


# =========================
# PHASE 2 — RUNTIME
# =========================
echo "[*] sysctl.conf tuning"

# ---- ISR (CRITICAL for 1 CPU) ----
add_sysctl net.isr.dispatch direct

# ---- backlog alignment ----
add_sysctl kern.ipc.somaxconn 8192

# ---- SYN protection ----
add_sysctl net.inet.tcp.syncookies 1

# ---- TCP Fast Open ----
add_sysctl net.inet.tcp.fastopen.server_enable 1

# ---- socket buffers ----
add_sysctl net.inet.tcp.sendspace 131072
add_sysctl net.inet.tcp.recvspace 131072
add_sysctl net.local.stream.sendspace 131072
add_sysctl net.local.stream.recvspace 131072

# ---- latency optimization ----
add_sysctl net.inet.tcp.delayed_ack 0

# ---- congestion control ----
add_sysctl net.inet.tcp.cc.algorithm cubic

# ---- TIME_WAIT handling ----
add_sysctl net.inet.tcp.fast_finwait2_recycle 1
add_sysctl net.inet.tcp.msl 15000
add_sysctl net.inet.tcp.nolocaltimewait 1

# ---- port exhaustion ----
add_sysctl net.inet.ip.portrange.first 1024
add_sysctl net.inet.ip.portrange.last 65535

echo "[*] Applying sysctl"
sysctl -f "$SYSCTL"

echo ""
echo "[✓] DONE"
echo ""
echo ">>> REBOOT REQUIRED <<<"
