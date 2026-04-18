# Docker Compose Templates

Reference for `vps-deploy-playbook`. Use these templates when the VPS does not already have a `docker-compose.yml`, or when adding a new service to an existing one.

---

## Template 1 — Single App Service

Minimal template for a single containerized app with an external Nginx + Certbot setup.

```yaml
version: '3.8'

services:
  SERVICE_NAME:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: SERVICE_NAME
    restart: unless-stopped
    ports:
      - "APP_PORT:APP_PORT"
    env_file:
      - .env
    networks:
      - services

networks:
  services:
    external: true
```

**Replace:**
- `SERVICE_NAME` → your service name (e.g. `my-app`)
- `APP_PORT` → the port the app listens on (e.g. `3000`)

---

## Template 2 — App + Nginx + Certbot (All-in-One)

Use this when setting up Nginx and Certbot as Docker containers for the first time on a fresh VPS.

```yaml
version: '3.8'

services:
  SERVICE_NAME:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: SERVICE_NAME
    restart: unless-stopped
    env_file:
      - .env
    networks:
      - services
    expose:
      - "APP_PORT"

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - certbot-webroot:/var/www/certbot:ro
      - certbot-certs:/etc/letsencrypt:ro
    networks:
      - services
    depends_on:
      - SERVICE_NAME

  certbot:
    image: certbot/certbot:latest
    container_name: certbot
    volumes:
      - certbot-webroot:/var/www/certbot
      - certbot-certs:/etc/letsencrypt
    networks:
      - services
    # Run manually: docker exec certbot certbot certonly --webroot ...
    entrypoint: /bin/sh -c "trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done"

volumes:
  certbot-webroot:
  certbot-certs:

networks:
  services:
    name: services
```

---

## Template 3 — Next.js Standalone Output

Optimized for Next.js apps using `output: 'standalone'` in `next.config.js`.

**`Dockerfile` (place in project root):**
```dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* bun.lockb* ./
RUN \
  if [ -f bun.lockb ]; then npm install -g bun && bun install --frozen-lockfile; \
  elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install --frozen-lockfile; \
  else npm ci; \
  fi

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN \
  if [ -f bun.lockb ]; then bun run build; \
  elif [ -f pnpm-lock.yaml ]; then pnpm run build; \
  else npm run build; \
  fi

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000

RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Required in `next.config.js`:**
```js
module.exports = {
  output: 'standalone',
}
```

---

## Template 4 — Python FastAPI / Flask

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Useful Docker Commands

```bash
# Build and start a service
docker compose build SERVICE_NAME && docker compose up -d SERVICE_NAME

# View running containers
docker ps

# Tail logs for a service
docker logs SERVICE_NAME -f --tail 50

# Restart a service without rebuilding
docker compose restart SERVICE_NAME

# Rebuild from scratch (clears cache)
docker compose build --no-cache SERVICE_NAME && docker compose up -d SERVICE_NAME

# Stop and remove a container (keeps image)
docker compose stop SERVICE_NAME && docker compose rm -f SERVICE_NAME

# List all images
docker images

# Remove dangling images (free disk space)
docker image prune -f

# Check disk usage by Docker
docker system df
```

---

## Adding a New Service to an Existing Compose File

1. SSH into the VPS and open the compose file:
   ```bash
   nano /opt/services/docker-compose.yml
   ```

2. Add the new service block under `services:` (use Template 1 format).

3. If the service needs to communicate with Nginx, ensure it's on the same network as the `nginx` container.

4. Run from `/opt/services/`:
   ```bash
   docker compose build NEW_SERVICE && docker compose up -d NEW_SERVICE
   ```
