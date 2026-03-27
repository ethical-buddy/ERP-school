#!/usr/bin/env python3
import concurrent.futures
import statistics
import time
import urllib.request

URL = "http://127.0.0.1:8000/api/v1/health/"
REQUESTS = 100
WORKERS = 20


def fetch(_):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(URL, timeout=5) as response:
            response.read()
            code = response.getcode()
    except Exception:
        code = 0
    return (time.perf_counter() - start) * 1000, code


def main():
    durations = []
    success = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for duration, code in executor.map(fetch, range(REQUESTS)):
            durations.append(duration)
            if 200 <= code < 300:
                success += 1
    print(f"requests={REQUESTS} workers={WORKERS} success={success}")
    if durations:
        print(f"avg_ms={statistics.mean(durations):.2f} p95_ms={statistics.quantiles(durations, n=20)[18]:.2f} max_ms={max(durations):.2f}")


if __name__ == "__main__":
    main()
