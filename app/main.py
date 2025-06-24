import re
import ipaddress
from pymongo import MongoClient
from pathlib import Path
import time
import os

# Delay to allow MongoDB to initialize if needed
time.sleep(2)

# Dynamically get MongoDB host
mongo_host = os.getenv("MONGO_HOST", "host.docker.internal")
mongo_url = f"mongodb://{mongo_host}:27017/"

# Connect to MongoDB
try:
    print(f"Connecting to MongoDB at: {mongo_url}")
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection test
    print("Successfully connected to MongoDB.")
except Exception as e:
    print("Could not connect to MongoDB:", e)
    exit(1)

db = client["ip_db"]
collection = db["ip_addresses"]
collection.delete_many({})  # Optional: clear old data

def extract_ips_from_line(line):
    return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)

def is_private(ip):
    return ipaddress.ip_address(ip).is_private

def process_log_file(file_path):
    private_ips = set()
    public_ips = set()

    with open(file_path, 'r') as file:
        for line in file:
            ips = extract_ips_from_line(line)
            for ip in ips:
                if is_private(ip):
                    private_ips.add(ip)
                else:
                    public_ips.add(ip)

    print("Public IPs to insert:", public_ips)
    print("Private IPs to insert:", private_ips)

    if public_ips:
        collection.insert_one({"type": "public", "ips": list(public_ips)})
        print("Public IPs inserted.")

    if private_ips:
        collection.insert_one({"type": "private", "ips": list(private_ips)})
        print("Private IPs inserted.")

if __name__ == "__main__":
    log_file_path = Path(__file__).parent / "test.log"
    print(f"Processing log file: {log_file_path}")
    process_log_file(log_file_path)
    print("Log processing completed.")
