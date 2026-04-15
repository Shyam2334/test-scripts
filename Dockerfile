# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ ./

# Build the React app
RUN npm run build

# Stage 2: Python Backend
FROM python:3.9-slim-buster

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app/ ./app/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./app/static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]