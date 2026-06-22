# ACNC Malaysia - Donor Platform Backend

Python FastAPI backend for donation management platform.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- pip

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update database credentials in `.env`

5. Run migrations:
```bash
alembic upgrade head
```

6. Start development server:
```bash
uvicorn app.main:app --reload
```

API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Donations
- `POST /api/v1/donations/` - Create donation
- `GET /api/v1/donations/{donation_id}` - Get donation details
- `GET /api/v1/donations/my-donations` - Get user's donations

### Users
- `GET /api/v1/users/profile` - Get current user profile
- `PUT /api/v1/users/profile` - Update profile

### Admin
- `GET /api/v1/admin/dashboard` - Admin dashboard
- `GET /api/v1/admin/donations` - All donations
- `POST /api/v1/admin/verify-receipt/{donation_id}` - Verify receipt

## Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```
