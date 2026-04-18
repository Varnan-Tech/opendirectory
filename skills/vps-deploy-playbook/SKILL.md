---
name: vps-deploy-playbook
description: Full Docker + Nginx + SSL deployment to a Linux VPS. Transfers your app, spins up a Docker container, configures Nginx as reverse proxy, provisions an SSL certificate, and verifies the deployment is live. Supports a two-environment strategy (test subdomain on master branch, production domain on main branch). Use when asked to "deploy to VPS", "ship to server", "set up nginx + SSL", "deploy this app", or "push to production".
compatibility: [claude-code, gemini-cli, github-copilot, opencode]
author: zeroone-dots-ai
version: 1.0.0
---

# VPS Deploy Playbook

Transfer your app to a Linux VPS, containerize it with Docker, route traffic through Nginx, and lock it down with a free SSL certificate. One skill, complete deployment.

Supports a two-environment branching model:
- **master branch** → `test.yourdomain.com` (test environment)
- **main branch** → `yourdomain.com` (production)

Always target test first. Only promote to production after verifying on the test subdomain.

---

## Step 1: Environment Check

Confirm all required env vars are present:

```bash
echo "VPS_HOST:       ${VPS_HOST:+set}"
echo "VPS_USER:       ${VPS_USER:+set}"
echo "SERVICE_NAME:   ${SERVICE_NAME:+set}"
echo "DOMAIN:         ${DOMAIN:+set}"
echo "APP_PORT:       ${APP_PORT:+set}"
echo "APP_DIR:        ${APP_DIR:-/opt/services/$SERVICE_NAME}"
```

**If VPS_HOST, VPS_USER, SERVICE_NAME, DOMAIN, or APP_PORT is missing:**
Stop. Tell the user which variables are missing and point them to `.env.example` for the full list.

**Determine deployment target from current git branch:**
```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
if [ "$CURRENT_BRANCH" = "main" ]; then
  DEPLOY_DOMAIN="${DOMAIN}"
  DEPLOY_ENV="production"
else
  DEPLOY_DOMAIN="test.${DOMAIN}"
  DEPLOY_ENV="test"
fi
echo "Branch: $CURRENT_BRANCH → deploying to $DEPLOY_ENV ($DEPLOY_DOMAIN)"
```

Confirm with the user before proceeding if DEPLOY_ENV is "production":
> "You are on `main`. This will deploy to **production** at `$DOMAIN`. Continue? (yes/no)"

If the user says no — stop and suggest branching off `master` first.

---

## Step 2: SSH Connectivity Check

Verify the VPS is reachable before doing any file transfer:

```bash
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "echo 'SSH OK'"
```

**If SSH fails:**
Stop. Tell the user:
- Check that `VPS_HOST` is correct (the raw IP or hostname, no protocol prefix)
- Check that their SSH key is added: `ssh-add ~/.ssh/id_rsa`
- Check that the VPS allows their IP if a firewall is in use

**Check Docker is running on VPS:**
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker info > /dev/null 2>&1 && echo 'Docker OK' || echo 'Docker NOT running'"
```

If Docker is not running: stop and ask the user to start it (`sudo systemctl start docker`).

**Check Nginx container is running (if using containerized Nginx):**
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker ps --filter 'name=nginx' --format '{{.Names}}' | grep -q nginx && echo 'Nginx OK' || echo 'Nginx container not found'"
```

If Nginx is not found: warn the user. Ask whether they use containerized Nginx or a system Nginx (`systemctl status nginx`). Adjust Step 6 commands accordingly.

---

## Step 3: Build Locally

Detect the package manager and run the production build:

```bash
if [ -f "bun.lockb" ]; then
  bun run build
elif [ -f "pnpm-lock.yaml" ]; then
  pnpm run build
elif [ -f "yarn.lock" ]; then
  yarn build
else
  npm run build
fi
```

**If no `build` script exists in package.json:** skip this step and proceed directly to Docker build.

**If build fails:** stop. Do not transfer a broken build to the VPS. Show the error output to the user.

---

## Step 4: Transfer Files to VPS

Sync the app directory to the VPS, excluding build artifacts and dev files:

```bash
APP_DIR="${APP_DIR:-/opt/services/${SERVICE_NAME}}"

rsync -avz --progress \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude '.next' \
  --exclude '.turbo' \
  --exclude '*.log' \
  --exclude '.env*' \
  ./ ${VPS_USER}@${VPS_HOST}:${APP_DIR}/
```

**Note:** `.env` files are excluded from rsync deliberately — they contain secrets. Transfer the env file separately:

```bash
if [ -f ".env" ]; then
  scp .env ${VPS_USER}@${VPS_HOST}:${APP_DIR}/.env
  echo "Transferred .env"
fi
```

After transfer, confirm the app directory exists and has files:
```bash
ssh ${VPS_USER}@${VPS_HOST} "ls ${APP_DIR}/ | head -20"
```

---

## Step 5: Build and Start Docker Container

Check if a `docker-compose.yml` exists on the VPS. If it does, use Compose. If not, create one from the template in `references/DOCKER-COMPOSE-TEMPLATE.md`.

**With docker-compose.yml present:**
```bash
ssh ${VPS_USER}@${VPS_HOST} "cd ${APP_DIR} && docker compose build ${SERVICE_NAME} && docker compose up -d ${SERVICE_NAME}"
```

**Without docker-compose.yml (standalone container):**
```bash
ssh ${VPS_USER}@${VPS_HOST} "cd ${APP_DIR} && \
  docker build -t ${SERVICE_NAME}:latest . && \
  docker stop ${SERVICE_NAME} 2>/dev/null || true && \
  docker rm ${SERVICE_NAME} 2>/dev/null || true && \
  docker run -d \
    --name ${SERVICE_NAME} \
    --restart unless-stopped \
    -p ${APP_PORT}:${APP_PORT} \
    --env-file .env \
    ${SERVICE_NAME}:latest"
```

Verify the container started:
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker ps --filter 'name=${SERVICE_NAME}' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

If the container is not running: fetch its logs and show them to the user.
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker logs ${SERVICE_NAME} --tail 50"
```

---

## Step 6: Configure Nginx

Read `references/NGINX-TEMPLATE.md` for the server block templates before writing any config.

**Check if an Nginx config already exists for this domain:**
```bash
ssh ${VPS_USER}@${VPS_HOST} "ls /etc/nginx/conf.d/ | grep ${DEPLOY_DOMAIN}"
```

**If no config exists** — create one using the HTTP template from `references/NGINX-TEMPLATE.md`. Write it to the VPS:

```bash
ssh ${VPS_USER}@${VPS_HOST} "cat > /etc/nginx/conf.d/${DEPLOY_DOMAIN}.conf << 'NGINX_EOF'
server {
    listen 80;
    server_name ${DEPLOY_DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://localhost:${APP_PORT};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
NGINX_EOF"
```

**Test and reload Nginx:**

For containerized Nginx:
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker exec nginx nginx -t && docker exec nginx nginx -s reload"
```

For system Nginx:
```bash
ssh ${VPS_USER}@${VPS_HOST} "nginx -t && systemctl reload nginx"
```

If the config test fails: show the error. Do not reload. Ask the user to inspect `/etc/nginx/conf.d/${DEPLOY_DOMAIN}.conf` for syntax issues.

---

## Step 7: Provision SSL Certificate

Skip this step if the user confirms SSL is already provisioned for this domain.

**Check if cert exists:**
```bash
ssh ${VPS_USER}@${VPS_HOST} "[ -d /etc/letsencrypt/live/${DEPLOY_DOMAIN} ] && echo 'cert exists' || echo 'no cert'"
```

**If no cert — provision via Certbot:**

For Certbot in Docker:
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker exec certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d ${DEPLOY_DOMAIN} \
  --email ${SSL_EMAIL:-admin@${DOMAIN}} \
  --agree-tos \
  --non-interactive"
```

For system Certbot:
```bash
ssh ${VPS_USER}@${VPS_HOST} "certbot certonly \
  --webroot -w /var/www/certbot \
  -d ${DEPLOY_DOMAIN} \
  --email ${SSL_EMAIL:-admin@${DOMAIN}} \
  --agree-tos \
  --non-interactive"
```

**If Certbot fails with DNS or rate limit error:**
- DNS not propagated yet: tell the user to wait and try again in 5-10 minutes
- Rate limit (too many certs): suggest using `--staging` flag to test, then re-run without it when rate limits reset

**After cert is provisioned — replace the HTTP nginx config with the HTTPS config from `references/NGINX-TEMPLATE.md`:**

```bash
ssh ${VPS_USER}@${VPS_HOST} "cat > /etc/nginx/conf.d/${DEPLOY_DOMAIN}.conf << 'NGINX_EOF'
server {
    listen 80;
    server_name ${DEPLOY_DOMAIN};
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name ${DEPLOY_DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${DEPLOY_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DEPLOY_DOMAIN}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:${APP_PORT};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
NGINX_EOF"
```

Reload Nginx again after updating to HTTPS config.

---

## Step 8: Verify Deployment

Run a health check against the live URL:

```bash
curl -sf --max-time 15 https://${DEPLOY_DOMAIN} -o /dev/null -w "HTTP %{http_code}\n"
```

**If status is 200 or 30x:** deployment is healthy.

**If status is 502:** the app container is not responding. Check:
```bash
ssh ${VPS_USER}@${VPS_HOST} "docker logs ${SERVICE_NAME} --tail 30"
```

**If status is 000 (connection refused):** Nginx is not routing traffic. Check that port 80/443 is open on the VPS firewall:
```bash
ssh ${VPS_USER}@${VPS_HOST} "ufw status | grep -E '80|443'"
```
If blocked: `ssh ${VPS_USER}@${VPS_HOST} "ufw allow 80 && ufw allow 443"`

**If SSL cert error:** the cert may not have propagated yet. Wait 30 seconds and retry.

---

## Step 9: Output Deployment Report

Print a summary:

```
DEPLOYMENT COMPLETE
===================
Environment:  $DEPLOY_ENV
URL:          https://$DEPLOY_DOMAIN
Service:      $SERVICE_NAME (Docker container)
Branch:       $CURRENT_BRANCH
SSL:          provisioned / existing / skipped
Nginx config: /etc/nginx/conf.d/$DEPLOY_DOMAIN.conf
App dir:      $APP_DIR

Next steps (if test):
  1. Verify the app at https://$DEPLOY_DOMAIN
  2. When ready: git checkout main && git merge master
  3. Re-run this skill on main to promote to production

Rollback:
  See references/ROLLBACK-SOP.md
```

---

## Rules

- Never delete `.env` from the VPS. Always `scp` it separately, never rsync it.
- Never deploy to `main` / production without first asking the user to confirm.
- If any step fails, stop and explain the failure. Do not skip ahead.
- If `APP_DIR` is not set, default to `/opt/services/$SERVICE_NAME`.
- For rollback procedures, read `references/ROLLBACK-SOP.md` in full.
