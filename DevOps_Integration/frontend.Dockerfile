# Step 1: Build Vite React project
FROM node:18-alpine AS build

WORKDIR /app

# Copy package configurations and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source files and compile
COPY frontend/ .
RUN npm run build

# Step 2: Serve compiled assets using Nginx
FROM nginx:alpine

# Copy compiled static assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose standard web traffic port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
