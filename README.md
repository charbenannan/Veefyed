# Skin Analysis API

A FastAPI-based backend service for image upload and mock skin analysis, designed for mobile integration.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Design Decisions](#design-decisions)
- [Production Improvements](#production-improvements)

## ✨ Features

- ✅ Image upload with validation (JPEG/PNG, max 5MB)
- ✅ Mock skin analysis with structured JSON response
- ✅ API key authentication
- ✅ Comprehensive error handling
- ✅ Request logging
- ✅ Interactive Swagger documentation
- ✅ Docker support
- ✅ Environment-based configuration

## 🛠 Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Language**: Python 3.9+
- **File Handling**: python-multipart, Pillow
- **Configuration**: python-dotenv

## 📁 Project Structure

```
veefyed/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py          # Image upload endpoint
│   │   └── analyze.py         # Analysis endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_service.py   # Image handling logic
│   │   └── analysis_service.py # Mock analysis logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py      # File validation utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   └── config.py              # Configuration settings
├── uploads/                    # Local storage for uploaded images
├── .env                        # Environment variables (not in Git)
├── .env.example                # Environment template
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd veefyed-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env (Powershell)
   copy .env.example .env (CMD)
   ```
   
   Edit `.env` and set your API key:
   ```env
   API_KEY=your-secret-api-key-here
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 🔐 Environment Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Secret key for API authentication | - | Yes |
| `HOST` | Server host address | `0.0.0.0` | No |
| `PORT` | Server port number | `8000` | No |
| `MAX_FILE_SIZE_MB` | Maximum upload file size in MB | `5` | No |
| `UPLOAD_DIR` | Directory for storing uploaded images | `uploads` | No |

### Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your configuration:
   ```env
   API_KEY=dev-api-key-12345
   HOST=0.0.0.0
   PORT=8000
   MAX_FILE_SIZE_MB=5
   UPLOAD_DIR=uploads
   ```

3. **Security Note**: Never commit the `.env` file to version control.

### Generating a Secure API Key

For production, generate a strong API key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🏃 Running the Application

### Using Virtual Environment (Recommended)

This is the **preferred method** for running the application locally.

1. **Ensure you're in the project directory**:
   ```bash
   cd veefyed
   ```

2. **Activate virtual environment**:
   
   **On Windows PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **On Windows CMD:**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`

4. **Stop the server**:
   Press `Ctrl+C` in the terminal

5. **Deactivate virtual environment** (when done):
   ```bash
   deactivate
   ```

### Production Mode (Without Auto-reload)

For production or testing without auto-reload:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Alternative: Using Docker

If you prefer containerization, see the [Docker Deployment](#docker-deployment) section below.

## 📚 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Authentication

All endpoints (except `/docs` and `/redoc`) require an API key in the header:

```
X-API-Key: your-api-key-here
```

### 1. Upload Image

**POST** `/upload`

Upload an image for analysis.

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: multipart/form-data
```

**Body:**
```
file: <image file> (JPEG or PNG, max 5MB)
```

**Success Response (200):**
```json
{
  "image_id": "abc123def456",
  "message": "Image uploaded successfully",
  "filename": "image.jpg",
  "size_bytes": 245678
}
```

**Error Responses:**
- `400` - Invalid file type or size exceeds limit
- `401` - Invalid or missing API key

### 2. Analyze Image

**POST** `/analyze`

Analyze a previously uploaded image.

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Body:**
```json
{
  "image_id": "abc123def456"
}
```

**Success Response (200):**
```json
{
  "image_id": "abc123def456",
  "skin_type": "Combination",
  "issues": ["Hyperpigmentation", "Fine Lines"],
  "confidence": 0.87,
  "analysis_timestamp": "2026-01-06T10:30:45.123456",
  "recommendations": [
    "Use sunscreen daily to prevent further pigmentation",
    "Consider retinol products for fine lines"
  ]
}
```

**Error Responses:**
- `404` - Image not found
- `401` - Invalid or missing API key

### 3. Health Check

**GET** `/health`

Check API health status.

**Response (200):**
```json
{
  "status": "healthy"
}
```

### 4. Root

**GET** `/`

Get API information.

**Response (200):**
```json
{
  "message": "Welcome to Skin Analysis API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "upload": "/upload",
    "analyze": "/analyze"
  }
}
```

## 🐳 Docker Deployment

### Using Docker Run

```bash
# Build the image
docker build -t veefyed-api .

# Run with environment file
docker run --env-file .env -p 8000:8000 veefyed-api
```

### Using Docker Compose (Recommended)

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The API will be available at `http://localhost:8000`

## 🧪 Testing

### Using cURL

**Upload an image:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "X-API-Key: dev-api-key-12345" \
  -F "file=@/path/to/image.jpg"
```

**Analyze an image:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123def456"}'
```

### Using Python

```python
import requests

API_KEY = "dev-api-key-12345"
BASE_URL = "http://localhost:8000"

# Upload
with open("test_image.jpg", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload",
        headers={"X-API-Key": API_KEY},
        files={"file": f}
    )
    image_id = response.json()["image_id"]

# Analyze
response = requests.post(
    f"{BASE_URL}/analyze",
    headers={"X-API-Key": API_KEY},
    json={"image_id": image_id}
)
print(response.json())
```

### Using Swagger UI

1. Visit http://localhost:8000/docs
2. Click "Authorize" and enter your API key
3. Test endpoints directly in the browser

## 🏗 Design Decisions

### Architecture

- **Clean separation of concerns**: Routes, services, and utilities are separated for maintainability
- **Dependency injection**: FastAPI's dependency system for authentication
- **Error handling**: Custom exceptions with global handlers for consistent error responses
- **Logging**: Request/response logging for debugging and monitoring

### File Storage

- **Local filesystem**: Suitable for development and demonstration
- **UUID-based naming**: Prevents filename conflicts and provides unique identifiers
- **In-memory metadata**: Simple storage for demo purposes

### Mock Analysis

The analysis service simulates AI processing by:
- Randomly selecting skin types and issues
- Generating realistic confidence scores (0.70-0.95)
- Providing contextual recommendations

This demonstrates the API structure and data flow without requiring a trained ML model.

### Security

- **API key authentication**: Protects endpoints from unauthorized access
- **File validation**: Checks file type and size before processing
- **Environment variables**: Keeps sensitive configuration out of source code

## 🚀 Production Improvements

If this were a production system, I would implement the following:

### High Priority

1. **Database Integration**
   - PostgreSQL for image metadata and user management
   - Proper indexing for efficient queries
   - Migration system (Alembic)

2. **Cloud Storage**
   - AWS S3 or Google Cloud Storage for images
   - Signed URLs for secure access
   - CDN integration for faster delivery

3. **Real AI Integration**
   - TensorFlow/PyTorch models for actual skin analysis
   - Async processing with Celery/RQ for long-running tasks
   - Model versioning and A/B testing

4. **Enhanced Security**
   - JWT-based authentication with refresh tokens
   - Rate limiting (e.g., 100 requests/hour per user)
   - CORS configuration
   - Input sanitization
   - HTTPS enforcement

### Medium Priority

5. **Monitoring & Observability**
   - Structured logging (JSON format)
   - Metrics collection (Prometheus)
   - Error tracking (Sentry)
   - Performance monitoring (APM)

6. **Testing**
   - Unit tests with pytest (>80% coverage)
   - Integration tests
   - Load testing (Locust/JMeter)
   - CI/CD pipeline (GitHub Actions)

7. **API Versioning**
   - Version endpoints (`/v1/upload`)
   - Deprecation strategy
   - Backward compatibility guarantees

8. **Caching**
   - Redis for frequent queries
   - Analysis result caching
   - Image thumbnail generation and caching

### Nice to Have

9. **User Management**
   - User registration and authentication
   - Role-based access control
   - Usage quotas and billing

10. **Advanced Features**
    - Batch image processing
    - Webhook notifications for async operations
    - Image history and comparison
    - Feedback loop for model improvement
    - Multi-language support

11. **Infrastructure**
    - Kubernetes deployment
    - Auto-scaling
    - Blue-green deployments
    - Disaster recovery plan

## 📝 Assumptions

- **Local storage** is sufficient for demonstration purposes
- **Mock analysis** adequately demonstrates the API structure
- **Simple API key auth** is acceptable for this technical task
- **In-memory storage** for metadata is temporary
- **Single-instance deployment** for development

## 📄 License

MIT License

## 👤 Author

Charles Bentum-Annan

## 📧 Contact

For questions or feedback, please contact annancharles772@gmail.com

---

**Development Time**: ~4-5 hours
- Initial setup and structure: 30 min
- Upload endpoint with validation: 1 hour
- Analysis endpoint with mock logic: 1 hour
- Error handling and logging: 45 min
- Authentication: 30 min
- Environment configuration: 30 min
- Docker setup: 30 min
- Documentation: 45 min
