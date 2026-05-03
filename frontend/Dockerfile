FROM node:18-alpine as builder
WORKDIR /app
# Note: Since we use public/index.html currently, we prepare for future React expansion
COPY . .

# Stage 2: Serve via Nginx
FROM nginx:alpine
# Copy the dashboard directly to the web root
COPY ./public /usr/share/nginx/html
# Standard Nginx security configuration
RUN echo "server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files \\\$uri \\\$uri/ /index.html; } }" > /etc/nginx/conf.d/default.conf
EXPOSE 80