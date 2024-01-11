#!/bin/bash

# For this to work, you must set:
# FERRY_VO=<experiment>

# Optionally set
# FERRY_URL=<url>
# [CERTIFICATE|KEY|CA]_PATH=<path>

echo "Communicating with ${FERRY_URL}"
echo "Synchronizing users for VO ${FERRY_VO}"
python3 /rucio-ferry-sync.py