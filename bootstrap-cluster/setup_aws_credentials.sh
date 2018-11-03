#!/usr/bin/env bash
#
# setup_aws_credentials.sh
# v2.0.0
#
# input params
# 1 = aws access key id for the pipeline service account identity
# 2 = aws secret access key for the pipeline service account identity
# 3 = aws region
# 4 = aws role to assume

set -euo pipefail

# add check for valid number of parameters
if [ $# != 4 ]
    echo "error: setup_aws_credentials.sh: incorrect number of parameters $#"
    exit 1
fi

mkdir -p ~/.aws

cat <<EOF >  ~/.aws/credentials
[default]
aws_access_key_id=$1
aws_secret_access_key=$2
region=$3
EOF

if [ $4 != "none" ]; then
    TMP="$(aws sts assume-role --output json --role-arn ${4} --role-session-name $CIRCLE_PROJECT_REPONAME || { echo 'sts failure!' ; exit 1; })"

    ACCESS_KEY=$(echo $TMP | jq -r ".Credentials.AccessKeyId")
    SECRET_KEY=$(echo $TMP | jq -r ".Credentials.SecretAccessKey")
    SESSION_TOKEN=$(echo $TMP | jq -r ".Credentials.SessionToken")
    EXPIRATION=$(echo $TMP | jq -r ".Credentials.Expiration")

    cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id=${ACCESS_KEY}
aws_secret_access_key=${SECRET_KEY}
aws_session_token=${SESSION_TOKEN}
region=$3
EOF
fi
