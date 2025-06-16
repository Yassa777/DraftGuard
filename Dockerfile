# Stage 1: Build Frontend
FROM node:18 as frontend

WORKDIR /app/frontend

# Copy frontend package.json and install dependencies
COPY frontend/package.json ./
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ ./

# Build the frontend (assuming a build script in package.json)
# RUN npm run build

# Stage 2: Build Backend
FROM python:3.11-slim as backend

WORKDIR /app/backend

# Install poetry
RUN pip install poetry

# Copy backend dependency files and install
COPY backend/pyproject.toml backend/poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-root

# Copy the backend application code
COPY backend/app ./app

# Stage 3: Final Image with Nginx
FROM nginx:stable-alpine

# Copy the built frontend from the 'frontend' stage
# COPY --from=frontend /app/frontend/dist /usr/share/nginx/html

# Copy Nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the backend from the 'backend' stage
COPY --from=backend /app/backend /app/backend

WORKDIR /app/backend

# Expose port 80 for Nginx
EXPOSE 80

# Start Gunicorn and Nginx
# CMD ["/start-services.sh"] 