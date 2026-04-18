# Nginx Configuration Templates

Reference for `vps-deploy-playbook`. The skill reads this file before writing any Nginx config to the VPS.

---

## Template 1 — HTTP Only (Pre-SSL)

Use this when provisioning a new domain before the SSL cert exists. Certbot requires an HTTP-accessible `/.well-known/acme-challenge/` path to validate domain ownership.

```nginx
server {
    listen 80;
    server_name DEPLOY_DOMAIN;

    # Required for Certbot HTTP-01 challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://localhost:APP_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Replace before use:**
- `DEPLOY_DOMAIN` → the actual domain (e.g. `test.myapp.com`)
- `APP_PORT` → the port Docker exposes (e.g. `3000`)

---

## Template 2 — HTTPS with HTTP Redirect (Post-SSL)

Use this after the SSL cert is provisioned. Replaces the HTTP-only config.

```nginx
# HTTP → HTTPS redirect
server {
    listen 80;
    server_name DEPLOY_DOMAIN;
    return 301 https://$host$request_uri;
}

# HTTPS with SSL termination
server {
    listen 443 ssl;
    server_name DEPLOY_DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DEPLOY_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DEPLOY_DOMAIN/privkey.pem;

    # Modern SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS (optional — remove if not sure)
    # add_header Strict-Transport-Security "max-age=63072000" always;

    # Proxy to Docker container
    location / {
        proxy_pass http://localhost:APP_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}
```

**Replace before use:**
- Both instances of `DEPLOY_DOMAIN` → actual domain
- `APP_PORT` → container port

---

## Template 3 — Static Files (No Docker)

Use when deploying a pre-built static site (HTML/CSS/JS) rather than a running container.

```nginx
server {
    listen 80;
    server_name DEPLOY_DOMAIN;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name DEPLOY_DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DEPLOY_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DEPLOY_DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    root /opt/static/DEPLOY_DOMAIN;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Aggressive caching for static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Nginx Commands Reference

### Containerized Nginx (Docker)
```bash
# Test config syntax
docker exec nginx nginx -t

# Reload config (zero-downtime)
docker exec nginx nginx -s reload

# Full restart (causes brief downtime)
docker restart nginx

# View error logs
docker exec nginx tail -50 /var/log/nginx/error.log

# List loaded config files
docker exec nginx ls /etc/nginx/conf.d/
```

### System Nginx (systemctl)
```bash
# Test config syntax
nginx -t

# Reload config (zero-downtime)
systemctl reload nginx

# Full restart
systemctl restart nginx

# View error logs
journalctl -u nginx -n 50 --no-pager
```

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `nginx: [emerg] unknown directive` | Typo in config | Run `nginx -t`, check the line number reported |
| `connect() failed (111: Connection refused)` | App container not running | `docker ps`, check container status, read logs |
| `SSL_ERROR_RX_RECORD_TOO_LONG` | Port 443 serving HTTP | Check `listen 443 ssl` is correct, not just `listen 443` |
| `upstream timed out` | App too slow to respond | Check `proxy_read_timeout`, investigate app performance |
| Certbot `challeng` failed | HTTP-01 path not reachable | Ensure `/.well-known/acme-challenge/` location block exists and `/var/www/certbot` is mounted |
