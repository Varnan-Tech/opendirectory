#!/bin/bash
set -e

INSTANCE_IP="13.221.72.26"
KEY_FILE="tribe-persistent-key-1777196102.pem"

echo "Running Docker container remotely with explicit token..."
ssh.exe -i "$KEY_FILE" -o StrictHostKeyChecking=no ubuntu@"$INSTANCE_IP" "sudo docker ps -q | xargs -r sudo docker stop && sudo docker ps -aq | xargs -r sudo docker rm && sudo docker run -d -p 8000:8000 --gpus all -e HF_TOKEN=\"${HF_TOKEN}\" hook-analyzer"

echo "Waiting for /health endpoint..."
max_retries=360
retry_count=0
while true; do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://"$INSTANCE_IP":8000/health || echo "000")
    if [ "$STATUS_CODE" == "200" ]; then
        echo "Health check passed."
        break
    fi
    echo "Waiting for model to download and load... ($retry_count / $max_retries)"
    sleep 10
    retry_count=$((retry_count+1))
    if [ $retry_count -ge $max_retries ]; then
        echo "Error: Health check failed."
        exit 1
    fi
done

echo "Sending POST /analyze..."
curl -s -X POST http://"$INSTANCE_IP":8000/analyze \
    -H "Content-Type: application/json" \
    -d '{"text": "Discover the neuroscience secret to viral hooks."}'
