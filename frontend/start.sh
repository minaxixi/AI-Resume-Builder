#!/bin/bash

# Replace environment variables in the built JS files
find /usr/share/nginx/html -type f -name "*.js" -exec sed -i "s|REACT_APP_API_URL|${REACT_APP_API_URL}|g" {} +

# Start nginx
nginx -g 'daemon off;'
