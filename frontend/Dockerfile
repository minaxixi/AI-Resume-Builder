# Use Node.js base image
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install serve
RUN npm install -g serve

# Command to serve the app
CMD serve -s build -l $PORT
