# FastAPI Health Check Microservice

A simple FastAPI microservice with health check endpoint, user management, and interactive API documentation.

## Features

- Health check endpoint for monitoring
- User management with mock data
- Interactive API documentation (Swagger UI)
- Endpoint discovery API
- Clean, modern React UI

## API Endpoints

### Health Check
- **GET** `/health` - Returns the health status of the service

### Users
- **GET** `/api/users` - Returns a list of 10 mock users

### Discovery
- **GET** `/api/v1/endpoints` - Returns a list of available API endpoints

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation (ReDoc)
- **GET** `/openapi.json` - OpenAPI schema

## Running the Application

### Backend (FastAPI)

1. Install dependencies: