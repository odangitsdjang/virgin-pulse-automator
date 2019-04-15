#!/usr/bin/env bash
export $(grep -v '^#' secrets.env | xargs)
