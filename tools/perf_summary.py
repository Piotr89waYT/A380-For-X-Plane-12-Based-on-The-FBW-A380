"""Average the plugin's `perf:` lines from X-Plane's Log.txt, to compare display settings.

    python tools/perf_summary.py <Log.txt> [label] [--skip N]

Skips the first N perf lines (default 3: loading and settling) and lines under 10 fps (pauses, loading).
"""
import re
import sys

FIELDS = {
    "fps": r"X-Plane ([\d.]+) fps",
    "frame_ms": r"\(frame ([\d.]+) ms",
    "gpu_ms": r"GPU ([\d.]+) ms",
    "worst_ms": r"worst frame ([\d.]+) ms",
    "xp_cores": r"CPU X-Plane (\d+)% of a core",
    "xphfbw_cores": r"XPHFBW (\d+)% of a core",
    "plugin_ms": r"([\d.]+) ms per frame in the plugin",
    "upload_mb": r"([\d.]+) MB of screen pixels uploaded per frame",
    "screens_ms": r"screens \(draw callbacks\) ([\d.]+)",
}


def parse(lines):
    rows = []
    for line in lines:
        if "FBW A380 systems: perf:" not in line:
            continue
        row = {}
        for key, pat in FIELDS.items():
            m = re.search(pat, line)
            row[key] = float(m.group(1)) if m else 0.0
        for key in ("xp_cores", "xphfbw_cores"):
            row[key] /= 100
        rows.append(row)
    return rows


def summary(rows, skip):
    rows = [r for r in rows[skip:] if r["fps"] >= 10]
    if not rows:
        return None
    return {k: sum(r[k] for r in rows) / len(rows) for k in FIELDS} | {"samples": len(rows)}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skip = int(sys.argv[sys.argv.index("--skip") + 1]) if "--skip" in sys.argv else 3
    if "--skip" in sys.argv:
        args.remove(str(skip))
    path, label = args[0], (args[1] if len(args) > 1 else "")
    with open(path, encoding="utf-8", errors="replace") as f:
        s = summary(parse(f), skip)
    if s is None:
        sys.exit(f"{path}: no perf lines at 10 fps or more after skipping {skip}")
    print(f"{label or path}: " + ", ".join(f"{k} {v:.2f}" if k != "samples" else f"{k} {v}" for k, v in s.items()))


if __name__ == "__main__":
    main()


def _selftest():
    line = ("FBW A380 systems: perf: X-Plane 32.2 fps (frame 31.0 ms, GPU 14.7 ms, worst frame 36.3 ms), CPU X-Plane 422% of a core, "
            "XPHFBW 211% of a core, cefclient 0% of a core; 6.52 ms per frame in the plugin, 8.6 MB of screen pixels uploaded per frame "
            "(DU_NDR 2.7); ms per frame: screens (draw callbacks) 2.55, of the draw callbacks: uploads 2.11")
    s = summary(parse(["noise", line, line.replace("32.2 fps", "1.0 fps")]), 0)
    assert s["samples"] == 1 and s["fps"] == 32.2 and s["xphfbw_cores"] == 2.11 and s["screens_ms"] == 2.55, s
