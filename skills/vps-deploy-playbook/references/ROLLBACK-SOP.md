# Rollback SOP

Standard operating procedure for rolling back a failed VPS deployment. Read this when a deployment breaks production.

---

## Decision Tree: Which Rollback to Use?

```
Did the app container crash after deploy?
  YES → Section 1: Container Rollback (fast, no code change)
  NO  →
    Is Nginx returning 502/404 for the domain?
      YES → Section 2: Nginx Config Rollback
      NO  →
        Is the app running but showing bad data or broken features?
          YES → Section 3: Code Rollback (git revert + redeploy)
          NO  →
            Did the SSL cert fail?
              YES → Section 4: SSL Recovery
```

---

## Section 1: Container Rollback (Fastest — 2 minutes)

Roll back to the previous Docker image without touching code.

**Step 1: Check available images**
```bash
ssh $VPS_USER@$VPS_HOST "docker images $SERVICE_NAME --format 'table {{.Tag}}\t{{.CreatedAt}}\t{{.ID}}'"
```

**Step 2: Stop the broken container**
```bash
ssh $VPS_USER@$VPS_HOST "docker stop $SERVICE_NAME && docker rm $SERVICE_NAME"
```

**Step 3: Start the previous image**

If using Docker Compose with explicit tags:
```bash
ssh $VPS_USER@$VPS_HOST "cd $APP_DIR && IMAGE_TAG=previous docker compose up -d $SERVICE_NAME"
```

If using standalone Docker with image ID (replace `IMAGE_ID` with the previous image ID from Step 1):
```bash
ssh $VPS_USER@$VPS_HOST "docker run -d \
  --name $SERVICE_NAME \
  --restart unless-stopped \
  -p $APP_PORT:$APP_PORT \
  --env-file $APP_DIR/.env \
  IMAGE_ID"
```

**Step 4: Verify**
```bash
curl -sf --max-time 15 https://$DEPLOY_DOMAIN -o /dev/null -w "HTTP %{http_code}\n"
```

---

## Section 2: Nginx Config Rollback

If Nginx was reconfigured during the deploy and is now serving errors.

**Step 1: Check current config**
```bash
ssh $VPS_USER@$VPS_HOST "cat /etc/nginx/conf.d/$DEPLOY_DOMAIN.conf"
```

**Step 2: Check Nginx error logs**
```bash
# Containerized Nginx
ssh $VPS_USER@$VPS_HOST "docker exec nginx tail -50 /var/log/nginx/error.log"

# System Nginx
ssh $VPS_USER@$VPS_HOST "tail -50 /var/log/nginx/error.log"
```

**Step 3: Restore config from backup**

If a `.bak` file exists (created automatically if you used the playbook before):
```bash
ssh $VPS_USER@$VPS_HOST "cp /etc/nginx/conf.d/$DEPLOY_DOMAIN.conf.bak /etc/nginx/conf.d/$DEPLOY_DOMAIN.conf"
```

If no backup — rewrite the HTTP-only config manually (use NGINX-TEMPLATE.md Template 1).

**Step 4: Test and reload**
```bash
# Containerized
ssh $VPS_USER@$VPS_HOST "docker exec nginx nginx -t && docker exec nginx nginx -s reload"

# System
ssh $VPS_USER@$VPS_HOST "nginx -t && systemctl reload nginx"
```

---

## Section 3: Code Rollback (Git Revert + Redeploy)

When the container runs but the code has a bug that broke production.

**Step 1: Identify the last known-good commit**
```bash
git log --oneline -10
```

**Step 2: Create a revert commit (preferred — non-destructive)**
```bash
git revert HEAD --no-edit
git push origin main
```

**Step 3: Re-run the deploy skill from main**
The skill will detect `main` branch and deploy to production automatically.

**Alternative: Hard reset (destructive — only if revert is not possible)**
```bash
# WARNING: this rewrites git history
git reset --hard PREVIOUS_COMMIT_HASH
git push --force origin main
```

Only use force-push if the broken commit introduced secrets or there is no other option.

---

## Section 4: SSL Recovery

**Symptom: SSL cert provisioning failed, domain served over HTTP only**

**Step 1: Verify HTTP-01 challenge path is reachable**
```bash
curl -sf http://$DEPLOY_DOMAIN/.well-known/acme-challenge/test -o /dev/null -w "HTTP %{http_code}\n"
```

- `404` → the `/.well-known/acme-challenge/` location block is missing from Nginx config (add it from NGINX-TEMPLATE.md Template 1)
- `000` → Nginx is not running or port 80 is blocked by firewall

**Step 2: Check firewall allows port 80**
```bash
ssh $VPS_USER@$VPS_HOST "ufw status | grep 80"
# If missing: ufw allow 80
```

**Step 3: Re-run Certbot**
```bash
# Containerized Certbot
ssh $VPS_USER@$VPS_HOST "docker exec certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d $DEPLOY_DOMAIN \
  --email $SSL_EMAIL \
  --agree-tos \
  --non-interactive"

# System Certbot
ssh $VPS_USER@$VPS_HOST "certbot certonly \
  --webroot -w /var/www/certbot \
  -d $DEPLOY_DOMAIN \
  --agree-tos \
  --non-interactive"
```

**Step 4: If hitting Let's Encrypt rate limits**

Rate limit: 5 duplicate certificates per domain per week.

Use staging to test the flow without consuming rate limit quota:
```bash
ssh $VPS_USER@$VPS_HOST "docker exec certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d $DEPLOY_DOMAIN \
  --staging \
  --agree-tos \
  --non-interactive"
```

When staging works — delete the staging cert and re-run without `--staging`.

---

## Emergency: Restore from Last Working Nginx Config

If Nginx is completely broken and cannot be fixed quickly, serve a maintenance page:

```bash
ssh $VPS_USER@$VPS_HOST "cat > /etc/nginx/conf.d/$DEPLOY_DOMAIN.conf << 'EOF'
server {
    listen 80;
    server_name $DEPLOY_DOMAIN;
    location / {
        return 503 'Service temporarily unavailable';
        add_header Content-Type text/plain;
    }
}
EOF
docker exec nginx nginx -t && docker exec nginx nginx -s reload"
```

This returns a 503 (which is better than a connection timeout) while you debug.

---

## Post-Rollback Checklist

After any rollback:

- [ ] Verify the site is responding at `https://$DEPLOY_DOMAIN`
- [ ] Check the container logs have no new errors: `docker logs $SERVICE_NAME --tail 20`
- [ ] Notify stakeholders that a rollback occurred
- [ ] Create a GitHub issue or post-mortem documenting what failed
- [ ] Fix the root cause on a feature branch before attempting the deploy again
