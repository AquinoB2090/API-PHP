#!/bin/bash
set -e

if [ -f /home/site/wwwroot/nginx.conf ]; then
    cp /home/site/wwwroot/nginx.conf /etc/nginx/sites-enabled/default
elif [ -f /home/site/repository/nginx.conf ]; then
    cp /home/site/repository/nginx.conf /etc/nginx/sites-enabled/default
else
    sed -i 's#try_files .*#try_files $uri $uri/ /index.php?$args;#' /etc/nginx/sites-enabled/default
fi

service nginx reload
