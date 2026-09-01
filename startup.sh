#!/bin/bash
set -e

CONFIG_FILE="/home/site/default"

cp /etc/nginx/sites-enabled/default "$CONFIG_FILE"

awk '
    /location \/ \{/ { in_root_location = 1 }
    in_root_location && /try_files/ {
        print "        try_files $uri $uri/ /index.php?$args;";
        in_root_location = 0;
        next;
    }
    { print }
' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

cp "$CONFIG_FILE" /etc/nginx/sites-enabled/default
service nginx reload
