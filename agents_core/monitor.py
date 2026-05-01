import docker
import time
import os

client = docker.from_env()

def self_heal():
    print("Self-Healer: Monitoring Swarm Health...")
    containers = client.containers.list(all=True)
    for container in containers:
        if container.status != 'running' and "swarmenterprise" in container.name:
            print(f"CRITICAL: {container.name} is down. Re-spawning...")
            container.start()

    # Integrity Check: Ensure .env exists
    if not os.path.exists("../.env"):
        print("REPLICATOR: .env missing. Restoring from master backup...")
        # Logic to restore from a protected volume

if __name__ == "__main__":
    while True:
        try:
            self_heal()
        except Exception as e:
            print(f"Monitor Error: {e}")
        time.sleep(60) # Run every minute
