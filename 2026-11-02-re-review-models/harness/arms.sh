#!/usr/bin/env bash
# arm label -> "engine model effort"
arm() {
  case "$1" in
    S-high)    echo "base claude-sonnet-5-5 high" ;;
    S-medium)  echo "base claude-sonnet-5-5 medium" ;;
    H-high)    echo "base claude-haiku-5-5 high" ;;
    C-S-high)  echo "compact claude-sonnet-5-5 high" ;;
    S-high-2)  echo "base claude-sonnet-5-5 high" ;;
    S-medium-2) echo "base claude-sonnet-5-5 medium" ;;
    H-high-2)  echo "base claude-haiku-5-5 high" ;;
    C-S-high-2) echo "compact claude-sonnet-5-5 high" ;;
    *) return 1 ;;
  esac
}
