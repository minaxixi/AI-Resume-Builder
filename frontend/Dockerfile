# Build stage
FROM node:16-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Make port 80 available to the world outside this container
EXPOSE 80

# Add bash for DigitalOcean App Platform
RUN apk add --no-cache bash

# Add startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start Nginx server
CMD ["/start.sh"]
