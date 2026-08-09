#!/usr/bin/env python3
"""Prometheus exporter for Aoraki queue wait times and GRES allocation.

Fills three gaps left by prometheus-slurm-exporter, which exposes job *counts* and CPU
capacity but nothing about how long jobs wait and nothing about GPUs at all:

  aoraki_job_wait_seconds        histogram  how long jobs waited before starting
  aoraki_pending_job_seconds_*   gauge      how long the current queue has been waiting
  aoraki_gres_{gpu,shard}_*      gauge      GPUs allocated vs available, by type

Standard library only. Serves the Prometheus text format on /metrics.
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Sized from the measured distribution of 72,185 jobs over 7 days: 35% of jobs start within
# a minute, but the tail runs to 15 days. Both ends need resolution.
BUCKETS = [5, 15, 30, 60, 300, 900, 1800, 3600, 7200, 21600, 43200, 86400, 259200, 604800]

# Pending reasons where the job is waiting on something other than the cluster being busy.
# Counting these as contention would badly overstate how loaded Aoraki is.
BLOCKED_REASONS = {
    "Dependency",
    "DependencyNeverSatisfied",
    "JobHeldUser",
    "JobHeldAdmin",
    "BeginTime",
}

STATE_VERSION = 1
TIME_FMT = "%Y-%m-%dT%H:%M:%S"

# gpu:A100:2(S:0-1) / gpu:A100:2(IDX:0-1) / gpu:0 / shard:A100:16 / (null)
GRES_RE = re.compile(r"\b(gpu|shard):(?:([A-Za-z0-9_.\-]+):)?(\d+)")

# sinfo StateLong values meaning the node cannot currently accept work.
UNAVAILABLE_STATES = ("down", "drain", "drng", "fail", "maint", "unk", "inval", "resv", "boot")


def run(cmd, timeout=120):
    """Run a Slurm command and return stdout, or None if it failed."""
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        log("command failed: %s: %s" % (" ".join(cmd), exc))
        return None
    if p.returncode != 0:
        log("command exited %d: %s: %s" % (p.returncode, " ".join(cmd), p.stderr.strip()[:200]))
        return None
    return p.stdout


def log(msg):
    print("slurm-wait-exporter: %s" % msg, file=sys.stderr, flush=True)


def parse_time(value):
    """Parse a Slurm timestamp. Unknown/None/empty all mean 'did not happen'."""
    value = (value or "").strip()
    if not value or value in ("Unknown", "None", "N/A"):
        return None
    try:
        return datetime.strptime(value, TIME_FMT)
    except ValueError:
        return None


def parse_gres(field):
    """Return {('gpu'|'shard', type): count} from a sinfo Gres or GresUsed field."""
    out = {}
    for kind, gres_type, count in GRES_RE.findall(field or ""):
        out[(kind, gres_type or "unknown")] = out.get((kind, gres_type or "unknown"), 0) + int(count)
    return out


# --------------------------------------------------------------------------- state


def empty_state():
    return {"version": STATE_VERSION, "last_run": None, "buckets": {}, "sum": {}, "count": {}, "seen": {}}


def load_state(path):
    if not path or not os.path.exists(path):
        return empty_state()
    try:
        with open(path) as fh:
            state = json.load(fh)
    except (OSError, ValueError) as exc:
        log("could not read state from %s (%s); starting fresh" % (path, exc))
        return empty_state()
    if state.get("version") != STATE_VERSION:
        log("state file version %r is not %d; starting fresh" % (state.get("version"), STATE_VERSION))
        return empty_state()
    return state


def save_state(path, state):
    """Write atomically so a crash mid-write cannot leave a truncated state file."""
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".state-")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh)
        os.replace(tmp, path)
    except OSError as exc:
        log("could not write state to %s: %s" % (path, exc))
        if os.path.exists(tmp):
            os.unlink(tmp)


# --------------------------------------------------------------------- collectors


def collect_waits(state, backfill, overlap, now=None):
    """Fold newly started jobs into the cumulative wait histogram held in `state`.

    Counters must only ever go up, so this accumulates into `state` rather than recomputing.
    Each run re-queries with an overlap and dedupes on JobIDRaw, so a missed or slow run
    cannot drop jobs or count them twice.
    """
    now = now or datetime.now()
    if state.get("last_run"):
        since = parse_time(state["last_run"]) or (now - backfill)
        since -= overlap
    else:
        # First run: seed from history so the dashboard is useful immediately rather than
        # after a week of accumulation.
        since = now - backfill
        log("no previous state; backfilling from %s" % since.strftime(TIME_FMT))

    out = run([
        "sacct", "-a", "-X", "-P", "--noconvert",
        "-S", since.strftime(TIME_FMT),
        "-E", now.strftime(TIME_FMT),
        "-o", "JobIDRaw,Partition,Eligible,Start,State",
    ])
    if out is None:
        return state

    seen = state.get("seen", {})
    added = 0
    for line in out.strip().splitlines()[1:]:
        parts = line.split("|")
        if len(parts) < 5:
            continue
        job_id, partition, eligible, start, _job_state = parts[:5]
        if not job_id or job_id in seen:
            continue

        eligible_at, started_at = parse_time(eligible), parse_time(start)
        if eligible_at is None or started_at is None:
            continue  # never started, or never became eligible

        # Wait is Start - Eligible, not Start - Submit. A job held by --begin or by a
        # dependency has not been waiting on the cluster, and charging that time here would
        # blame Aoraki for the user's own scheduling.
        wait = (started_at - eligible_at).total_seconds()
        if wait < 0:
            continue

        # A job submitted to several partitions records them comma-separated; a started job
        # ran in exactly one, which Slurm lists first.
        partition = (partition or "unknown").split(",")[0]

        buckets = state["buckets"].setdefault(partition, {})
        for edge in BUCKETS:
            if wait <= edge:
                buckets[str(edge)] = buckets.get(str(edge), 0) + 1
        buckets["+Inf"] = buckets.get("+Inf", 0) + 1
        state["sum"][partition] = state["sum"].get(partition, 0.0) + wait
        state["count"][partition] = state["count"].get(partition, 0) + 1

        seen[job_id] = started_at.strftime(TIME_FMT)
        added += 1

    # Keep the dedupe set bounded: anything older than two overlap windows can no longer be
    # returned by the next query, so it cannot be double-counted.
    cutoff = now - (overlap * 2)
    state["seen"] = {
        jid: ts for jid, ts in seen.items() if (parse_time(ts) or now) >= cutoff
    }
    state["last_run"] = now.strftime(TIME_FMT)
    if added:
        log("recorded %d newly started jobs" % added)
    return state


def collect_pending():
    """How long the jobs currently queued have been waiting, per partition."""
    out = run([
        "squeue", "-a", "-h", "-t", "PD",
        "-O", "Partition:40,PendingTime:20,Reason:40",
    ])
    if out is None:
        return None

    waiting, counts = {}, {}
    for line in out.splitlines():
        fields = line.split()
        if len(fields) < 2:
            continue
        partition, pending = fields[0], fields[1]
        reason = fields[2] if len(fields) > 2 else ""
        partition = partition.split(",")[0]
        try:
            seconds = float(pending)
        except ValueError:
            continue

        blocked = "true" if reason in BLOCKED_REASONS else "false"
        counts[(partition, blocked)] = counts.get((partition, blocked), 0) + 1
        if blocked == "false":
            waiting.setdefault(partition, []).append(seconds)

    return {"waiting": waiting, "counts": counts}


def collect_gres():
    """GPUs and shards allocated vs configured, deduped by node.

    `sinfo -N` emits one row per node *per partition* — aoraki11 appears three times, under
    aoraki_short, aoraki_gpu and aoraki_gpu_A100_80GB. Summing the raw rows triple-counts it.
    """
    out = run(["sinfo", "-h", "-N", "-O", "NodeList:30,Gres:60,GresUsed:60,StateLong:30"])
    if out is None:
        return None

    nodes = {}
    for line in out.splitlines():
        fields = line.split()
        if len(fields) < 4:
            continue
        node, gres, gres_used, node_state = fields[0], fields[1], fields[2], fields[3]
        nodes[node] = (parse_gres(gres), parse_gres(gres_used), node_state.lower())

    total, alloc, unavailable = {}, {}, {}
    for configured, used, node_state in nodes.values():
        offline = any(s in node_state for s in UNAVAILABLE_STATES)
        for key, count in configured.items():
            total[key] = total.get(key, 0) + count
            if offline:
                unavailable[key] = unavailable.get(key, 0) + count
        for key, count in used.items():
            alloc[key] = alloc.get(key, 0) + count

    # Nodes with no GPUs still report "gpu:0" in GresUsed while leaving Gres as "(null)",
    # which would otherwise invent an untyped series that is always zero. The configured
    # set is the authority: report exactly those types, and report them even when zero so
    # a fully idle GPU type is a flat line rather than a gap.
    alloc = {key: alloc.get(key, 0) for key in total}
    unavailable = {key: unavailable.get(key, 0) for key in total}

    return {"total": total, "alloc": alloc, "unavailable": unavailable}


# ------------------------------------------------------------------------ rendering


def escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def labels(**kwargs):
    return "{%s}" % ",".join('%s="%s"' % (k, escape(v)) for k, v in sorted(kwargs.items()))


def render(state, pending, gres):
    lines = []
    add = lines.append

    add("# HELP aoraki_job_wait_seconds Seconds between a job becoming eligible and starting.")
    add("# TYPE aoraki_job_wait_seconds histogram")
    for partition in sorted(state["buckets"]):
        buckets = state["buckets"][partition]
        for edge in [str(b) for b in BUCKETS] + ["+Inf"]:
            add("aoraki_job_wait_seconds_bucket%s %d" % (
                labels(partition=partition, le=edge), buckets.get(edge, 0)))
        add("aoraki_job_wait_seconds_sum%s %f" % (
            labels(partition=partition), state["sum"].get(partition, 0.0)))
        add("aoraki_job_wait_seconds_count%s %d" % (
            labels(partition=partition), state["count"].get(partition, 0)))

    if pending is not None:
        add("# HELP aoraki_pending_job_seconds_max Longest current wait among queued jobs.")
        add("# TYPE aoraki_pending_job_seconds_max gauge")
        for partition, waits in sorted(pending["waiting"].items()):
            add("aoraki_pending_job_seconds_max%s %f" % (labels(partition=partition), max(waits)))

        add("# HELP aoraki_pending_job_seconds_median Median current wait among queued jobs.")
        add("# TYPE aoraki_pending_job_seconds_median gauge")
        for partition, waits in sorted(pending["waiting"].items()):
            add("aoraki_pending_job_seconds_median%s %f" % (
                labels(partition=partition), statistics.median(waits)))

        add('# HELP aoraki_pending_jobs Queued jobs. blocked="true" means held by a '
            "dependency, a hold or --begin rather than by contention.")
        add("# TYPE aoraki_pending_jobs gauge")
        for (partition, blocked), count in sorted(pending["counts"].items()):
            add("aoraki_pending_jobs%s %d" % (
                labels(partition=partition, blocked=blocked), count))

    if gres is not None:
        for kind in ("gpu", "shard"):
            for metric, key, help_text in (
                ("total", "total", "configured on the cluster"),
                ("alloc", "alloc", "currently allocated to jobs"),
                ("unavailable", "unavailable", "on nodes that are down, drained or reserved"),
            ):
                name = "aoraki_gres_%s_%s" % (kind, metric)
                add("# HELP %s %ss %s." % (name, kind.upper(), help_text))
                add("# TYPE %s gauge" % name)
                for (gres_kind, gres_type), count in sorted(gres[key].items()):
                    if gres_kind != kind:
                        continue
                    add("%s%s %d" % (name, labels(gpu_type=gres_type), count))

    add("# HELP aoraki_wait_exporter_last_scrape_timestamp_seconds Unix time of last refresh.")
    add("# TYPE aoraki_wait_exporter_last_scrape_timestamp_seconds gauge")
    add("aoraki_wait_exporter_last_scrape_timestamp_seconds %f" % time.time())

    return "\n".join(lines) + "\n"


# -------------------------------------------------------------------------- serving


class Exporter:
    def __init__(self, args):
        self.args = args
        self.lock = threading.Lock()
        self.payload = "# exporter starting\n"

    def refresh(self):
        state = load_state(self.args.state)
        state = collect_waits(
            state,
            backfill=timedelta(seconds=self.args.backfill),
            overlap=timedelta(seconds=self.args.overlap),
        )
        if not self.args.dry_run:
            save_state(self.args.state, state)
        payload = render(state, collect_pending(), collect_gres())
        with self.lock:
            self.payload = payload
        return payload

    def read(self):
        with self.lock:
            return self.payload


def serve(exporter, port):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            if self.path.split("?")[0] not in ("/metrics", "/"):
                self.send_error(404)
                return
            body = exporter.read().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass  # journald already records the unit; per-scrape lines are noise

    ThreadingHTTPServer(("", port), Handler).serve_forever()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=9341)
    ap.add_argument("--interval", type=int, default=60, help="seconds between refreshes")
    ap.add_argument("--state", default="/var/lib/aoraki-wait-exporter/state.json",
                    help="where cumulative histogram counters are persisted")
    ap.add_argument("--backfill", type=int, default=7 * 86400,
                    help="seconds of history to seed the histogram from on first run")
    ap.add_argument("--overlap", type=int, default=2 * 3600,
                    help="seconds of re-query overlap, to survive a missed run")
    ap.add_argument("--oneshot", action="store_true", help="print metrics once and exit")
    ap.add_argument("--dry-run", action="store_true", help="do not persist state")
    args = ap.parse_args()

    exporter = Exporter(args)

    if args.oneshot:
        sys.stdout.write(exporter.refresh())
        return 0

    exporter.refresh()

    def loop():
        while True:
            time.sleep(args.interval)
            try:
                exporter.refresh()
            except Exception as exc:  # a bad scrape must not kill the exporter
                log("refresh failed: %r" % exc)

    threading.Thread(target=loop, daemon=True).start()
    log("listening on :%d" % args.port)
    serve(exporter, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
