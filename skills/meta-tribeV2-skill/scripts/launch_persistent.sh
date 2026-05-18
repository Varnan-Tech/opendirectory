#!/bin/bash
set -e
export AWS_DEFAULT_REGION="us-east-1"
export AWS_REGION="us-east-1"

echo "Finding default VPC..."
VPC_ID=$(aws.exe --region us-east-1 ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text | tr -d '\r')

echo "Finding Subnet in VPC..."
SUBNET_ID=$(aws.exe --region us-east-1 ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=availability-zone,Values=*b" --query "Subnets[0].SubnetId" --output text | tr -d '\r')

SG_NAME="tribe-persistent-sg-$(date +%s)"
echo "Creating Security Group: $SG_NAME..."
SG_ID=$(aws.exe --region us-east-1 ec2 create-security-group --group-name "$SG_NAME" --description "Persistent SG for TRIBE" --vpc-id "$VPC_ID" --query "GroupId" --output text | tr -d '\r')

echo "Authorizing ingress for port 22 and 8000..."
aws.exe --region us-east-1 ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr "0.0.0.0/0" > /dev/null
aws.exe --region us-east-1 ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 8000 --cidr "0.0.0.0/0" > /dev/null

KEY_NAME="tribe-persistent-key-$(date +%s)"
KEY_FILE="${KEY_NAME}.pem"
echo "Creating Key Pair: $KEY_NAME..."
aws.exe --region us-east-1 ec2 create-key-pair --key-name "$KEY_NAME" --query "KeyMaterial" --output text | tr -d '\r' > "$KEY_FILE"

echo "Finding Deep Learning AMI..."
AMI_ID=$(aws.exe --region us-east-1 ec2 describe-images --owners amazon --filters "Name=name,Values=*Deep Learning OSS Nvidia Driver AMI GPU PyTorch*Ubuntu*" "Name=state,Values=available" --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text | tr -d '\r')

echo "Launching PERSISTENT g5.12xlarge instance..."
INSTANCE_ID=$(aws.exe --region us-east-1 ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type g5.12xlarge \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SG_ID" \
    --subnet-id "$SUBNET_ID" \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":150,"VolumeType":"gp3"}}]' \
    --query "Instances[0].InstanceId" \
    --output text | tr -d '\r')

echo "Waiting for instance to run..."
aws.exe --region us-east-1 ec2 wait instance-running --instance-ids "$INSTANCE_ID"

INSTANCE_IP=$(aws.exe --region us-east-1 ec2 describe-instances --instance-ids "$INSTANCE_ID" --query "Reservations[0].Instances[0].PublicIpAddress" --output text | tr -d '\r')

echo ""
echo "=========================================="
echo "SUCCESS! Persistent Instance Created."
echo "INSTANCE_ID: $INSTANCE_ID"
echo "INSTANCE_IP: $INSTANCE_IP"
echo "KEY_FILE: $KEY_FILE"
echo "=========================================="