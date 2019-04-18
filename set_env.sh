#!/usr/bin/env bash
# Run me with this command: source ./set_env.sh
source ./secrets.env
export $(cut -d= -f1 ./secrets.env)
