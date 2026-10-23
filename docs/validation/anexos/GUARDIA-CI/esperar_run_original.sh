#!/bin/sh
# Espera a que el run de la CI termine y dice su estado.
run="$1"
while true; do
  estado=$(gh run view "$run" --json status,conclusion --jq '.status + " " + .conclusion' 2>/dev/null || echo "error")
  case "$estado" in
    completed*) echo "run $run: $estado"; exit 0 ;;
  esac
  sleep 30
done
