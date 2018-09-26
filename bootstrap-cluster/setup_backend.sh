#!/usr/bin/env bash
#
# input params
# 1 = organization or delivery platform team name
# 2 = aws account name
# 3 = aws region

set -euo pipefail

# add check for valid number of parameters
if [ $# != 3 ]; then
    echo "error: setup_backend.sh: incorrect number of parameters"
    exit 1
fi

cat <<EOF > backend.conf
key="$1-aws-bootstrap/bootstrap/$2-secure-state.tfstate"
bucket="$1-$2-bootstrap-state"
region="$3"
profile="default"
EOF