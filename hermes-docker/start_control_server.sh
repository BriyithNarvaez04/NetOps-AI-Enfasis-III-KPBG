#!/bin/bash
pkill -f control_server.py 2>/dev/null
sleep 1
nohup python3 ~/hermes-docker/control_server.py > ~/hermes-docker/control_server.log 2>&1 &
echo "Control server iniciado (PID: $!)"
