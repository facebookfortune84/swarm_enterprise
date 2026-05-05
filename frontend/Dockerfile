# ==============================================================================
# SOVEREIGN SDK: FRONTEND DOCKERFILE
# Version: 1.0.1-Alpha
# Description: Dynamic multi-stage React/Static build engine with SRE routing.
# ==============================================================================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy the entire frontend context
COPY . .

# SRE HARDENING: Dynamic Compilation Matrix
# If package.json exists, it executes a strict React build.
# If missing, it safely stages the static assets to prevent a launch crash.
RUN if [ -f package.json ]; then \
        echo "[*] React environment detected. Compiling..." && \
        npm install && npm run build; \
    else \
        echo "[*] Static environment detected. Staging raw assets..." && \
        mkdir -p build && \
        cp -r public/* build/ 2>/dev/null || true && \
        cp -r src/* build/ 2>/dev/null || true; \
    fi

# Stage 2: Hardened Nginx Perimeter
FROM nginx:alpine

# Pull compiled or statically staged assets from the builder node
COPY --from=builder /app/build /usr/share/nginx/html

# Inject SRE optimized SPA (Single Page Application) routing & Security Headers
RUN echo "server { \
    listen 80; \
    server_name localhost; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html lander.html; \
        try_files \$uri \$uri/ /index.html; \
    } \
    add_header X-Frame-Options \"SAMEORIGIN\"; \
    add_header X-XSS-Protection \"1; mode=block\"; \
    add_header X-Content-Type-Options \"nosniff\"; \
}" > /etc/nginx/conf.d/default.conf

EXPOSE 80

# Execute Nginx in the foreground to maintain container state
CMD ["nginx", "-g", "daemon off;"]