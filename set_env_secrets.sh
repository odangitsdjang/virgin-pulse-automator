#!/usr/bin/env bash
# Run me as 'source ./set_env_secrets.sh'
export $(grep -v '^#' secrets.env)
