#!/bin/bash

# For this to work, set:
# FERRY_VO=<experiment>
# FERRY_URL=<url>

echo "Communicating with ${FERRY_URL}"
echo "Synchronizing users for VO ${FERRY_VO}"
python3 /rucio-ferry-sync.py