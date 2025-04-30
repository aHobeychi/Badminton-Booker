#!/bin/bash

set -o allexport
source .env set
+o allexport

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
  echo "Error: TELEGRAM_BOT_TOKEN is not set."
  exit 1
fi

curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
| jq '.result[].message.chat.id' | sort -u