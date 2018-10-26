#!/usr/bin/env bash
#
# setup_aws_backend.sh
# v2.0.0
#
# input params
# 1 = s3 bucket name, this version of the script imposes the '-tf-state' name ending requirement
# 2 = bucket key, or folder path and filename for tf state file
# 3 = aws region
# 4 = ~/.aws/credentials profile to use

set -euo pipefail

# add check for valid number of parameters
if [ $# != 4 ]; then
    echo "error: setup_aws_backend.sh: incorrect number of parameters"
    exit 1
fi

cat <<EOF > backend.conf
bucket="$1-tf-state"
key="$2"
region="$3"
profile="$4"
EOF