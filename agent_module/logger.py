# logger.py
import json
from datetime import datetime


def log_requests(requests):
    with open("request_log.json", "a") as f:
        for r in requests:
            f.write(json.dumps(r) + "\n")


def log_results(results):
    with open("result_log.json", "a") as f:
        f.write(json.dumps(results) + "\n")


def log_round(round_num):
    with open("round_log.txt", "a") as f:
        f.write(f"\n=== ROUND {round_num} {datetime.now()} ===\n")
