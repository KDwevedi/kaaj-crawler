# Use Node.js as a base image
FROM node:18-slim

# Set the working directory
WORKDIR /app

# Copy dependency files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the application code
COPY src ./src
COPY public ./public

# Expose the development server port
EXPOSE 3000

# Start the React development server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
