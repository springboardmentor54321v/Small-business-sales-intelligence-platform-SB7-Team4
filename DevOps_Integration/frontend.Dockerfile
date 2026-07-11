FROM nginx:alpine

# Copy custom Nginx configuration
COPY DevOps_Integration/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy static frontend dashboard assets
COPY DevOps_Integration/frontend/ /usr/share/nginx/html/

# Expose Nginx port
EXPOSE 3000

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
