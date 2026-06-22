# ACNC Malaysia - Donor Missionary Support Platform

A comprehensive multi-currency donation platform with role-based access control, payment integration, and document management.

## Features

- **Multi-User Authentication**: Donor and Admin roles with JWT-based security
- **Donation Management**: Accept donations with fund allocation tracking
- **Multi-Currency Support**: USD, MYR, HKD, CNY, AUD, SGD, and more
- **Payment Integration**: QR code generation for:
  - Malaysia banks (Maybank, CIMB, Public Bank, etc.)
  - Hong Kong banks (HSBC, DBS, etc.)
  - Australian banks (Commonwealth, NAB, etc.)
- **Document Management**: PDF/Image upload for donor receipts
- **Admin Dashboard**: User management, donation tracking, reports
- **Multi-language Support**: English, Malay, Mandarin, Cantonese

## Tech Stack

- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS
- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with refresh tokens
- **File Storage**: AWS S3 or MinIO
- **Payment QR**: QR code generation with bank-specific formats

## Project Structure

```
.
├── frontend/              # Next.js application
├── backend/               # Python FastAPI application
├── docker-compose.yml
└── docs/                  # Documentation
```

## Quick Start

### Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI backend on port 8000
- Next.js frontend on port 3000

### Manual Setup

See `frontend/README.md` and `backend/README.md` for detailed instructions.

## Environment Variables

Copy `.env.example` files in each directory:

```bash
cd backend
cp .env.example .env

cd ../frontend
cp .env.example .env.local
```

## Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Payment Integration](docs/PAYMENT_INTEGRATION.md)
- [Multi-Currency Guide](docs/MULTI_CURRENCY.md)
- [File Upload Guide](docs/FILE_UPLOAD.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## License

MIT License - ACNC Malaysia
