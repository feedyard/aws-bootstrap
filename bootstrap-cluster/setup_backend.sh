#!/usr/bin/env bash
#
# setup_backup.sh
# v1.2.0
#
# input params
# 1 = product or delivery platform team name (required)
# 2 = aws account name (required)
# 3 = aws region (required)
# 4 = Infrastructure environment name (optional)

set -euo pipefail

# add check for valid number of parameters
if [ $# == 0 ] || [ $# == 2 ] || [ $# -gt 4 ]; then
    echo "error: setup_backend.sh: incorrect number of parameters"
    exit 1
fi

CLUSTER_NAME='bootstrap-cluster'

if [ $# == 4 ]; then
    CLUSTER_NAME=$(echo $CLUSTER_NAME-test)
fi

cat <<EOF > backend.conf
key="$1-aws-bootstrap/$CLUSTER_NAME/state.tfstate"
bucket="$1-$2-tf-state"
region="$3"
profile="default"
EOF