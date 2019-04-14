#!/usr/bin/env bash
# Quit any currently running containers
docker rm vp-auto-run

# Run the container with name 'vp-auto-run' in detached mode
docker run --name=vp-auto-run -d vp-auto

# Tail logs
docker logs --follow vp-auto-run
