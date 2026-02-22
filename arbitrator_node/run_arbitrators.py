import subprocess
import os
import time

# Load arbitrator keys from file
KEY_FILE = "trust_layer/accountMaintain/AccountDetails.txt"

def load_arbitrator_keys():
    keys = []
    capture = False

    with open(KEY_FILE, "r") as f:
        for line in f:
            line = line.strip()

            # Only start capturing after first Arbitrator section
            if line.startswith("Arbitrator"):
                capture = True

            if capture and line.startswith("Private Key:"):
                key = line.split(":")[1].strip()
                keys.append(key)

    return keys

def start_arbitrators():

    keys = load_arbitrator_keys()

    processes = []

    for index, key in enumerate(keys):

        env = os.environ.copy()
        env["ARBITRATOR_KEY"] = key
        env["ARBITRATOR_NAME"] = f"Arbitrator-{index+1}"

        print(f"Starting Arbitrator-{index+1}")

        process = subprocess.Popen(
            ["python", "-m", "arbitrator_node.arbitrator_service"],
            env=env
        )

        processes.append(process)
        time.sleep(1)  # small delay for clean startup

    return processes


if __name__ == "__main__":

    processes = start_arbitrators()

    print("\nAll arbitrators started.\nPress CTRL+C to stop all.")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopping arbitrators...")
        for p in processes:
            p.terminate()
        print("All stopped.")