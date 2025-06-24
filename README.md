# IP Address Extractor

This Docker-based project processes a log file to extract IP addresses, categorizes them into public and private, and stores them in a MongoDB collection.

## Features

- Extracts IPv4 addresses from a log file.
- Categorizes IPs into public and private ranges.
- Stores results in MongoDB with no duplicate entries per type.
- Designed to run inside Docker.
- Compatible with external MongoDB containers using environment variables.



## Setup Instructions

Precondition: git clone this repo and proceed with below steps:

1. Start MongoDB Container
Start MongoDB in Docker: 
docker run -d --name mongodb -p 27017:27017 mongo

2. Build the IP Extractor Docker Image : 
docker build -t ip_extractor .

3. Find the MongoDB Container's IP Address : 
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb

4. Run the IP Extractor Container with the IP address u get in the previous step(mostly it will be same) : 
docker run --rm -e MONGO_HOST=172.17.0.2 -v "$(pwd)/app:/app" ip_extractor

5. Check Stored Data in MongoDB
docker exec -it mongodb mongosh
use ip_db
db.ip_addresses.find().pretty()
