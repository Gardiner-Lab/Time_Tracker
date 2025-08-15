# Use Node.js official image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first for better caching
COPY package.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY server.js ./

# Create directory for database
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Start the server
CMD ["node", "server.js"]