import subprocess
import re
import pandas as pd
import os

def run_perf():
    result = subprocess.run(
        [
            "perf", "stat", "-a",
            "-e",
            "cpu_atom/cycles/,cpu_core/cycles/,"
            "cpu_atom/instructions/,cpu_core/instructions/,"
            "cpu_atom/cache-references/,cpu_core/cache-references/,"
            "cpu_atom/cache-misses/,cpu_core/cache-misses/,"
            "cpu_atom/branch-instructions/,cpu_core/branch-instructions/,"
            "cpu_atom/branch-misses/,cpu_core/branch-misses/,"
            "cpu_atom/bus-cycles/,cpu_core/bus-cycles/",
            "sleep", "1"
        ],
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stderr

def parse_perf_output(output):
    data = {}
    for line in output.splitlines():
        match = re.match(r"\s*([\d,]+)\s+([a-zA-Z0-9_\-/]+)", line)
        if match:
            try:
                value = int(match.group(1).replace(",", ""))
                event = match.group(2).strip("/")
                data[event] = value
            except ValueError:
                continue
    return data

def save_to_csv(data, filename="latency_results.csv"):
    df = pd.DataFrame([data])
    if not os.path.exists(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode="a", index=False, header=False)

if __name__ == "__main__":
    output = run_perf()
    parsed = parse_perf_output(output)

    print("\n=== Perf Results ===")
    if not parsed:
        print("No events parsed")
    else:
        for k, v in parsed.items():
            print(f"{k:30} {v}")

        save_to_csv(parsed)
