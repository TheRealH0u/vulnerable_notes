## Multi-stage Dockerfile for frontend
## Stage 1: build the Vite app using Node
FROM node:18-alpine AS build
WORKDIR /app

# Install only production dependencies needed for building
COPY package.json package-lock.json* ./
RUN npm ci --silent || npm install --silent

# Copy source and build
COPY . .
RUN npm run build

## Stage 2: serve the built files with nginx
FROM nginx:stable-alpine AS runtime

# Remove default nginx static files and copy our built app
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist /usr/share/nginx/html

# Use the provided nginx config if present (compose mounts may override)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
