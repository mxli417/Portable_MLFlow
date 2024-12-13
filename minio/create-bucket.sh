#!/bin/sh
# Configure MinIO Client
echo "Starting sleep to nap until the host arises..."
sleep 10;
echo "Now executing minio setup commands..."
mc alias set minioserver http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Create the MLFlow bucket
mc mb minioserver/ml-flow-bucket

echo "DONE"