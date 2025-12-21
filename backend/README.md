# Pathways for Parents - Backend API

FastAPI backend for the Pathways for Parents platform.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory (a template `.env` file has been created for you):

```bash
APP_ENV=development
PORT=8000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pathways_db?retryWrites=true&w=majority
JWT_SECRET=e911f25fa5baada3aab43f52ddbb6ffd12db4eee5c7741eaf7036c74dccae9c1
JWT_EXPIRES_IN=2592000
CORS_ORIGINS=http://localhost:3000
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@pathwaysforparents.com
```

**IMPORTANT:** You must update the `MONGODB_URI` with your actual MongoDB Atlas connection string.

### 3. Start the Server

```bash
python3 -m uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/healthz` - Check server and database status

### Authentication (Base path: `/api/v1/auth`)

#### Signup
- **POST** `/api/v1/auth/signup`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }
  ```
- **Response:**
  ```json
  {
    "user": {
      "id": "...",
      "email": "user@example.com",
      "name": "John Doe",
      "recommended_stage_id": null,
      "completed_milestones": [],
      "created_at": "2024-01-01T00:00:00Z"
    },
    "token": "eyJ..."
  }
  ```

#### Login
- **POST** `/api/v1/auth/login`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response:** Same as signup

#### Get Current User
- **GET** `/api/v1/auth/me`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "id": "...",
    "email": "user@example.com",
    "name": "John Doe",
    "recommended_stage_id": null,
    "completed_milestones": [],
    "created_at": "2024-01-01T00:00:00Z"
  }
  ```

#### Logout
- **POST** `/api/v1/auth/logout`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

### Onboarding (Base path: `/api/v1/onboarding`)

#### Submit Onboarding Questionnaire
- **POST** `/api/v1/onboarding`
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "childAgeRange": "3-5y",
    "diagnosisStatus": "waiting",
    "primaryConcern": "speech"
  }
  ```
- **Response:**
  ```json
  {
    "id": "...",
    "userId": "...",
    "childAgeRange": "3-5y",
    "diagnosisStatus": "waiting",
    "primaryConcern": "speech",
    "recommendedStageId": "s2",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
  ```

**Valid Values:**
- `childAgeRange`: `"0-18m"`, `"18-36m"`, `"3-5y"`, `"5-8y"`
- `diagnosisStatus`: `"none"`, `"waiting"`, `"recent"`, `"established"`
- `primaryConcern`: `"speech"`, `"behavior"`, `"social"`, `"school"`, `"general"`

#### Get Latest Onboarding Response
- **GET** `/api/v1/onboarding`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** Same as POST response

## Testing

### Option 1: Using the Test Script

A Python test script is provided to test all authentication endpoints:

```bash
# Make sure the server is running first
python3 test_auth.py

# Test onboarding functionality
python3 test_onboarding.py

# Test journey (stages, milestones, progress) functionality
python3 test_journey.py
```

The onboarding test script includes:
- Unit tests for the recommendation algorithm (15+ test cases)
- Integration tests for POST and GET endpoints
- Verification of data consistency and user updates

### Option 2: Using curl

#### Test Signup
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "name": "Test User"
  }'
```

#### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

#### Test Get Me (replace TOKEN with actual token)
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TOKEN"
```

#### Test Logout (replace TOKEN with actual token)
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer TOKEN"
```

### Option 3: Using Postman

1. Import the endpoints into Postman
2. Create a new environment with variable `baseUrl` = `http://localhost:8000`
3. Test each endpoint as described above

### Option 4: Using FastAPI Docs

Navigate to `http://localhost:8000/docs` to access the interactive API documentation (Swagger UI).

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and settings
├── database.py            # MongoDB connection management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Environment variables template
├── models/
│   ├── user.py           # User data model
│   ├── onboarding.py     # Onboarding data model with enums
│   ├── stage.py          # Journey stage model
│   └── milestone.py      # Milestone model
├── schemas/
│   ├── auth.py           # Auth request/response schemas
│   └── onboarding.py     # Onboarding request/response schemas
├── routers/
│   ├── auth.py           # Authentication endpoints
│   ├── onboarding.py     # Onboarding endpoints
│   ├── stages.py         # Journey stages endpoints
│   ├── milestones.py     # Milestones endpoints
│   └── progress.py       # User progress tracking endpoints
├── utils/
│   ├── security.py       # Password hashing utilities
│   ├── jwt.py            # JWT token utilities
│   ├── recommendation.py # Journey stage recommendation logic
│   └── seed_data.py      # Database seeding script
└── dependencies/
    └── auth.py           # Authentication dependencies
```

## Sprint 1 (S1) - Completed Features

✅ User Model with password hashing (Argon2)
✅ JWT-based authentication (30-day expiry)
✅ Signup endpoint with email validation
✅ Login endpoint with credential verification
✅ Protected `/auth/me` endpoint
✅ Logout endpoint
✅ MongoDB integration with Motor (async)
✅ CORS configuration for frontend

## Sprint 2 (S2) - Completed Features

✅ Onboarding data model with enums (ChildAgeRange, DiagnosisStatus, PrimaryConcern)
✅ Deterministic recommendation algorithm with:
  - Base stage calculation from diagnosis status
  - Age guardrails (caps based on child's age)
  - Concern-specific overrides
✅ POST `/api/v1/onboarding` endpoint (submit questionnaire)
✅ GET `/api/v1/onboarding` endpoint (retrieve latest response)
✅ Automatic user profile update with recommended stage
✅ Comprehensive test suite with 15+ algorithm test cases

### Recommendation Logic

The algorithm determines the recommended journey stage using three layers:

1. **Base Stage (Diagnosis Status):**
   - `none` → Stage 1
   - `waiting` → Stage 2
   - `recent` (≤12 months) → Stage 3
   - `established` (>12 months) → Stage 4

2. **Age Guardrails (Maximum Stage):**
   - `0-18m` → Max Stage 1
   - `18-36m` → Max Stage 2
   - `3-5y` → Max Stage 3
   - `5-8y` → Max Stage 4

3. **Concern Overrides:**
   - School concern + 5-8y age → Stage 4
   - Speech concern + <3y age → Stage 1
   - Behavior concern + recent diagnosis → Stage 3

## Sprint 3 (S3) - Completed Features

✅ Stage model with journey stage data (5 stages: Early Signs → Ongoing Support)
✅ Milestone model with production-quality content (~30 milestones total)
✅ Database seeding script with real, empathetic content
✅ GET `/api/v1/stages` endpoint (list all stages, sorted by order)
✅ GET `/api/v1/stages/{stage_id}` endpoint (get specific stage details)
✅ GET `/api/v1/milestones` endpoint (list all milestones, optional stage filter)
✅ GET `/api/v1/milestones/{milestone_id}` endpoint (get specific milestone)
✅ POST `/api/v1/progress/milestones/{milestone_id}/toggle` endpoint (toggle completion)
✅ GET `/api/v1/progress` endpoint (get user progress with stage percentages)
✅ DELETE `/api/v1/progress` endpoint (reset all progress)
✅ Comprehensive test suite for all journey endpoints

### Journey Content Structure

**5 Journey Stages:**
1. **Early Signs** (S1) - Noticing differences, first steps
2. **Diagnosis Journey** (S2) - Navigating evaluations
3. **Early Intervention** (S3) - Accessing services and support
4. **School Readiness** (S4) - Educational transitions and IEPs
5. **Ongoing Support** (S5) - Community, wellbeing, advocacy

**Milestone Content (per milestone):**
- Observable behavior description
- "Why it matters" explanation (60-80 words)
- "If not yet" guidance (reassuring, actionable)
- Reassurance copy (1-2 sentences)

### Seeding the Database

Before running tests, seed the database with stages and milestones:

```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Run the seed script
PYTHONPATH=. python3 utils/seed_data.py
```

The seed script is idempotent - it won't duplicate data if run multiple times.

## Next Steps

- Sprint 4 (S4): Resource library with filtering/search
- Sprint 5 (S5): Enhanced user profile management