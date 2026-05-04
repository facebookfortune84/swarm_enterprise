FROM node:18-alpine as builder
WORKDIR /app
# Context is the 'frontend' folder, so we copy everything inside it
COPY . .

FROM nginx:alpine
# Path fix: In this context, 'public' is at the root
COPY ./public /usr/share/nginx/html
RUN echo "server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files \$uri \$uri/ /index.html; } }" > /etc/nginx/conf.d/default.conf
EXPOSE 80
