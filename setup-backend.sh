#!/usr/bin/env bash

cat <<EOF > backend.conf
key="bootstrap-cluster/state.tfstate"
bucket="$1-$2-state"
region="$3"
profile="$4"
EOF