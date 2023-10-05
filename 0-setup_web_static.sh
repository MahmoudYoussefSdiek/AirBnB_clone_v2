#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Update package lists and install nginx
apt-get update
apt-get install -y nginx

# Create directories for web_static
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create index.html file with content
echo "Welcome to ALX" > /data/web_static/releases/test/index.html

# create a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership and permissions to /data/
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Create a Nginx configuration
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
EOF

# Restart Nginx service
service nginx restart
