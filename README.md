# Bank Statement Parser API

A powerful FastAPI-based service for extracting structured data from bank statements using OCR technology.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Endpoints](#endpoints)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **OCR Processing**: Leverages Veryfi's advanced OCR engine for accurate data extraction
- **Multiple Format Support**: Accepts PDF, JPEG, and PNG files
- **Async Processing**: Fully asynchronous endpoints for optimal performance
- **File Validation**: Automatic validation of file types and sizes
- **Structured Output**: Returns JSON responses with extracted data and confidence scores
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc documentation
- **Health Monitoring**: Built-in health check endpoints for monitoring
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **CORS Support**: Configurable CORS for cross-origin requests

## 🏗️ Architecture

```
doc-processor/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── bank_statements.py  # Bank statement processing endpoint
│   │   │   ├── health.py           # Health check endpoint
│   │   │   └── info.py             # API information endpoint
│   │   └── dependencies.py         # Dependency injection
│   ├── core/
│   │   ├── config.py               # Configuration management
│   │   └── logging.py              # Logging setup
│   ├── models/
│   │   └── responses.py            # Pydantic response models
│   ├── services/
│   │   └── veryfi_service.py       # Veryfi OCR service integration
│   ├── utils/
│   │   └── file_handler.py         # File handling utilities
│   ├── main.py                     # FastAPI application
│   └── requirements.txt            # Python dependencies
├── API_DOCUMENTATION.md            # Comprehensive API documentation
├── postman_collection.json         # Postman API collection
├── example_client.html             # Example web client
└── README.md                       # This file
```

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Veryfi API credentials

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd doc-processor
```

2. **Create a virtual environment**
```bash
python -m venv .venv
```

3. **Activate the virtual environment**

Windows:
```bash
.venv\Scripts\activate
```

Unix/MacOS:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r app/requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the `app/` directory with your Veryfi credentials:

```env
# Veryfi Configuration
VERYFI_CLIENT_ID=your_client_id
VERYFI_CLIENT_SECRET=your_client_secret
VERYFI_USERNAME=your_username
VERYFI_API_KEY=your_api_key

# Application Configuration (optional)
APP_NAME=Bank Statement Parser API
APP_VERSION=2.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# File Upload Configuration (optional)
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

### Getting Veryfi Credentials

1. Sign up at [Veryfi](https://www.veryfi.com/)
2. Navigate to your dashboard
3. Create a new application
4. Copy your credentials to the `.env` file

## 🚀 Running the Application

### Development Mode

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access comprehensive interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
  - Try out API endpoints directly
  - See request/response schemas
  - Test file uploads

- **ReDoc**: http://localhost:8000/redoc
  - Clean, responsive documentation
  - Detailed endpoint descriptions
  - Easy to navigate

### Additional Resources

- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Postman Collection**: Import `postman_collection.json` into Postman
- **Example Client**: Open `example_client.html` in your browser

## 🔌 Endpoints

### Root Endpoint
```
GET /
```
Returns API information and navigation links.

### Health Check
```
GET /api/v1/health
```
Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "doc-processor",
  "version": "2.0.0"
}
```

### API Information
```
GET /api/v1/info
```
Get comprehensive API capabilities and configuration.

**Response:**
```json
{
  "name": "Bank Statement Parser API",
  "version": "2.0.0",
  "description": "API for processing bank statements using OCR technology",
  "supported_formats": [...],
  "max_file_size": "10.00 MB",
  "endpoints": {...}
}
```

### Parse Bank Statement
```
POST /api/v1/parse-bank-statement
```
Upload and process a bank statement.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF, JPG, or PNG, max 10MB)

**Response:**
```json
{
  "status": "success",
  "data": {
    "bank_name": "Chase Bank",
    "account_holder_name": "John Doe",
    "account_number": "****1234",
    "confidence": 0.95
  },
  "message": "Document processed successfully"
}
```

## 💻 Usage Examples

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/parse-bank-statement" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/bank_statement.pdf"
```

### Python

```python
import requests

url = "http://localhost:8000/api/v1/parse-bank-statement"
files = {"file": open("bank_statement.pdf", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"Bank: {result['data']['bank_name']}")
print(f"Account Holder: {result['data']['account_holder_name']}")
print(f"Confidence: {result['data']['confidence']}")
```

### JavaScript

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/parse-bank-statement', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Extracted data:', data);
})
.catch(error => {
  console.error('Error:', error);
});
```

### Web Client

Open `example_client.html` in your browser for a fully functional web interface with:
- Drag-and-drop file upload
- Real-time validation
- Visual results display
- Error handling

## 🧪 Testing

### Manual Testing with Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on an endpoint (e.g., `/api/v1/parse-bank-statement`)
3. Click "Try it out"
4. Upload a test file
5. Click "Execute"
6. View the response

### Using Postman

1. Import `postman_collection.json` into Postman
2. Update the `baseUrl` variable if needed
3. Run the collection or individual requests

### Automated Testing (Coming Soon)

```bash
pytest tests/
```

## 📁 Project Structure

```
doc-processor/
├── app/
│   ├── api/
│   │   ├── endpoints/          # API endpoint modules
│   │   │   ├── bank_statements.py
│   │   │   ├── health.py
│   │   │   ├── info.py
│   │   │   └── __init__.py
│   │   ├── dependencies.py     # Dependency injection
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   ├── logging.py          # Logging configuration
│   │   └── __init__.py
│   ├── models/
│   │   ├── responses.py        # Pydantic models
│   │   └── __init__.py
│   ├── services/
│   │   ├── veryfi_service.py   # OCR service integration
│   │   └── __init__.py
│   ├── utils/
│   │   ├── file_handler.py     # File utilities
│   │   └── __init__.py
│   ├── .env                    # Environment variables (create this)
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── .venv/                      # Virtual environment
├── logs/                       # Application logs (auto-created)
├── API_DOCUMENTATION.md        # Detailed API docs
├── postman_collection.json     # Postman collection
├── example_client.html         # Example web client
└── README.md                   # This file
```

## 🔒 Security Considerations

### Current Implementation

- ✅ File type validation
- ✅ File size validation
- ✅ Temporary file cleanup
- ✅ Environment-based configuration
- ✅ Input validation with Pydantic

### Production Recommendations

1. **Enable HTTPS**: Use TLS/SSL for all API requests
2. **Add Authentication**: Implement API key or OAuth authentication
3. **Restrict CORS**: Configure specific allowed origins (currently set to "*")
4. **Add Rate Limiting**: Prevent abuse with rate limiting
5. **Implement Logging**: Use centralized logging for security auditing
6. **Data Encryption**: Encrypt sensitive data at rest
7. **Regular Updates**: Keep dependencies updated
8. **Environment Isolation**: Use separate environments for dev/staging/prod

### Example Production CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict to specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🐛 Known Limitations

- Maximum file size: 10 MB
- Supported formats: PDF, JPEG, PNG only
- English language documents only (currently)
- No authentication/authorization
- No rate limiting
- Single document processing (no batch processing)

## 🚀 Future Enhancements

- [ ] Batch document processing
- [ ] Authentication and authorization (API keys, JWT)
- [ ] Rate limiting per IP/API key
- [ ] Multi-language support
- [ ] Transaction history extraction
- [ ] Statement period detection
- [ ] Balance information extraction
- [ ] Webhook notifications
- [ ] Document history and retrieval
- [ ] Export to various formats (CSV, XML)
- [ ] Database integration for persistence
- [ ] Caching layer for performance
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For issues, questions, or contributions:
- **Email**: support@example.com
- **Issues**: Open an issue on GitHub
- **Documentation**: Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Veryfi](https://www.veryfi.com/) - OCR service provider
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

---

**Version**: 2.0.0  
**Last Updated**: 2025  
**Maintained by**: Your Team Name
