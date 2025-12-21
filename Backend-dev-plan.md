# Backend Development Plan - Pathways for Parents

## 1️⃣ Executive Summary

### What Will Be Built
A FastAPI backend that powers the Pathways for Parents web application - a guided roadmap platform for parents navigating autism with their children (0-8 years). The backend will handle user authentication, onboarding questionnaire logic, milestone progress tracking, and serve pre-populated journey stages and resources.

### Why This Approach
- **FastAPI (Python 3.13, async)** - Modern, fast, type-safe API framework with automatic OpenAPI docs
- **MongoDB Atlas** - Cloud-hosted NoSQL database for flexible schema and scalability
- **Motor + Pydantic v2** - Async MongoDB driver with robust data validation
- **No Docker** - Simplified local development and deployment
- **Manual testing via frontend** - Every task verified through UI before proceeding
- **Single branch `main`** - Streamlined Git workflow for MVP

### Constraints
- Python 3.13 runtime with async/await patterns
- MongoDB Atlas only (no local MongoDB instance)
- API base path: `/api/v1/*`
- JWT-based authentication (30-day expiry)
- Background tasks synchronous by default (use `BackgroundTasks` only if necessary)
- Manual testing required after every task (not just sprints)
- Git workflow: single branch `main` only

### Sprint Structure
Dynamic sprints (S0 → S5) covering:
- S0: Environment setup & frontend connection
- S1: Authentication (signup, login, logout)
- S2: Onboarding questionnaire & recommendation logic
- S3: Journey stages & milestone management
- S4: Resource library with filtering/search
- S5: User profile management & progress tracking

---

## 2️⃣ In-Scope & Success Criteria

### In-Scope Features
- User registration with email/password (Argon2 hashing)
- JWT-based login/logout with 30-day session
- Onboarding questionnaire with deterministic stage recommendation
- Journey timeline view with 5 pre-populated stages
- Milestone checklist tracking (check/uncheck persistence)
- Plain-English content embedded in milestones
- Resource library with category filtering and keyword search
- User profile viewing and editing
- Progress reset and onboarding retake
- Welcome email upon registration (via SendGrid/Postmark)

### Success Criteria
- All frontend features functional end-to-end
- User can complete onboarding → see personalized timeline → check milestones → progress persists
- Resources filterable by category and searchable by keyword
- All task-level manual tests pass via UI
- Each sprint's code pushed to `main` after verification
- MongoDB Atlas connection stable and performant
- API responses < 500ms for standard operations

---

## 3️⃣ API Design

### Base Path
`/api/v1`

### Error Envelope
```json
{ "error": "Human-readable error message" }
```

### Endpoints

#### Health Check
- **GET** `/healthz`
- **Purpose:** Verify backend is running and MongoDB Atlas is connected
- **Response:** `{ "status": "ok", "database": "connected", "timestamp": "ISO8601" }`
- **Validation:** None

#### Authentication
- **POST** `/api/v1/auth/signup`
  - **Purpose:** Register new user with email/password
  - **Request:** `{ "email": "string", "password": "string", "name": "string?" }`
  - **Response:** `{ "user": { "id": "string", "email": "string", "name": "string?" }, "token": "jwt_string" }`
  - **Validation:** Email format, password min 8 chars, email uniqueness

- **POST** `/api/v1/auth/login`
  - **Purpose:** Authenticate user and issue JWT
  - **Request:** `{ "email": "string", "password": "string" }`
  - **Response:** `{ "user": { "id": "string", "email": "string", "name": "string?", "recommendedStageId": "string?", "completedMilestones": ["string"] }, "token": "jwt_string" }`
  - **Validation:** Email format, credentials match

- **POST** `/api/v1/auth/logout`
  - **Purpose:** Invalidate session (client-side token removal)
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "message": "Logged out successfully" }`
  - **Validation:** Valid JWT

- **GET** `/api/v1/auth/me`
  - **Purpose:** Get current user profile
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "id": "string", "email": "string", "name": "string?", "recommendedStageId": "string?", "completedMilestones": ["string"], "createdAt": "ISO8601" }`
  - **Validation:** Valid JWT

#### Onboarding
- **POST** `/api/v1/onboarding`
  - **Purpose:** Submit onboarding questionnaire and calculate recommended stage
  - **Request:** `{ "childAgeRange": "0-18m|18-36m|3-5y|5-8y", "diagnosisStatus": "none|waiting|recent|established", "primaryConcern": "speech|behavior|school|services" }`
  - **Response:** `{ "recommendedStageId": "s1|s2|s3|s4|s5", "onboardingResponse": { "id": "string", "userId": "string", "childAgeRange": "string", "diagnosisStatus": "string", "primaryConcern": "string", "recommendedStageId": "string", "createdAt": "ISO8601" } }`
  - **Validation:** All fields required, predefined options only, valid JWT

- **GET** `/api/v1/onboarding`
  - **Purpose:** Retrieve user's onboarding response
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "id": "string", "userId": "string", "childAgeRange": "string", "diagnosisStatus": "string", "primaryConcern": "string", "recommendedStageId": "string", "createdAt": "ISO8601" }` or `null`
  - **Validation:** Valid JWT

#### Journey Stages
- **GET** `/api/v1/stages`
  - **Purpose:** List all journey stages
  - **Request:** None
  - **Response:** `[{ "id": "string", "title": "string", "description": "string", "ageRange": "string", "color": "string", "icon": "string", "order": number }]`
  - **Validation:** None (public endpoint)

- **GET** `/api/v1/stages/:stageId`
  - **Purpose:** Get single stage details
  - **Request:** None
  - **Response:** `{ "id": "string", "title": "string", "description": "string", "ageRange": "string", "color": "string", "icon": "string", "order": number }`
  - **Validation:** Valid stageId

#### Milestones
- **GET** `/api/v1/milestones`
  - **Purpose:** List all milestones (optionally filtered by stageId)
  - **Request:** Query param `?stageId=s1` (optional)
  - **Response:** `[{ "id": "string", "stageId": "string", "title": "string", "behavior": "string", "whyItMatters": "string", "ifNotYet": "string", "reassurance": "string" }]`
  - **Validation:** None (public endpoint)

- **GET** `/api/v1/milestones/:milestoneId`
  - **Purpose:** Get single milestone details
  - **Request:** None
  - **Response:** `{ "id": "string", "stageId": "string", "title": "string", "behavior": "string", "whyItMatters": "string", "ifNotYet": "string", "reassurance": "string" }`
  - **Validation:** Valid milestoneId

#### Milestone Progress
- **POST** `/api/v1/progress/milestones/:milestoneId/toggle`
  - **Purpose:** Toggle milestone completion status
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "milestoneId": "string", "isComplete": boolean, "completedAt": "ISO8601?" }`
  - **Validation:** Valid JWT, valid milestoneId

- **GET** `/api/v1/progress`
  - **Purpose:** Get user's milestone progress
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "completedMilestones": ["string"], "progressByStage": { "s1": 60, "s2": 0, ... } }`
  - **Validation:** Valid JWT

- **DELETE** `/api/v1/progress`
  - **Purpose:** Reset all milestone progress
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "message": "Progress reset successfully" }`
  - **Validation:** Valid JWT

#### Resources
- **GET** `/api/v1/resources`
  - **Purpose:** List resources with optional filtering
  - **Request:** Query params `?category=Diagnosis&search=iep` (both optional)
  - **Response:** `[{ "id": "string", "title": "string", "description": "string", "url": "string", "category": "string", "tags": ["string"] }]`
  - **Validation:** None (public endpoint)

- **GET** `/api/v1/resources/:resourceId`
  - **Purpose:** Get single resource details
  - **Request:** None
  - **Response:** `{ "id": "string", "title": "string", "description": "string", "url": "string", "category": "string", "tags": ["string"] }`
  - **Validation:** Valid resourceId

#### User Profile
- **GET** `/api/v1/users/me`
  - **Purpose:** Get current user profile (alias for `/auth/me`)
  - **Request:** None (JWT in Authorization header)
  - **Response:** `{ "id": "string", "email": "string", "name": "string?", "recommendedStageId": "string?", "completedMilestones": ["string"], "createdAt": "ISO8601" }`
  - **Validation:** Valid JWT

- **PATCH** `/api/v1/users/me`
  - **Purpose:** Update user profile (name, email)
  - **Request:** `{ "name": "string?", "email": "string?" }`
  - **Response:** `{ "id": "string", "email": "string", "name": "string?", "updatedAt": "ISO8601" }`
  - **Validation:** Valid JWT, email format if provided, email uniqueness

- **PATCH** `/api/v1/users/me/password`
  - **Purpose:** Change user password
  - **Request:** `{ "currentPassword": "string", "newPassword": "string" }`
  - **Response:** `{ "message": "Password updated successfully" }`
  - **Validation:** Valid JWT, current password matches, new password min 8 chars

---

## 4️⃣ Data Model (MongoDB Atlas)

### Collections

#### `users`
- **Fields:**
  - `_id`: ObjectId (MongoDB default)
  - `email`: string (required, unique, indexed)
  - `password_hash`: string (required, Argon2)
  - `name`: string (optional)
  - `recommended_stage_id`: string (optional, e.g., "s1")
  - `completed_milestones`: array of strings (default: [])
  - `created_at`: datetime (required)
  - `updated_at`: datetime (required)
- **Example:**
```json
{
  "_id": "ObjectId('...')",
  "email": "sarah@example.com",
  "password_hash": "$argon2id$v=19$m=65536...",
  "name": "Sarah",
  "recommended_stage_id": "s2",
  "completed_milestones": ["m1-1", "m1-2", "m2-1"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z"
}
```

#### `onboarding_responses`
- **Fields:**
  - `_id`: ObjectId
  - `user_id`: ObjectId (required, indexed, references users)
  - `child_age_range`: string (required, enum: "0-18m", "18-36m", "3-5y", "5-8y")
  - `diagnosis_status`: string (required, enum: "none", "waiting", "recent", "established")
  - `primary_concern`: string (required, enum: "speech", "behavior", "school", "services")
  - `recommended_stage_id`: string (required, e.g., "s1")
  - `created_at`: datetime (required)
  - `updated_at`: datetime (required)
- **Example:**
```json
{
  "_id": "ObjectId('...')",
  "user_id": "ObjectId('...')",
  "child_age_range": "18-36m",
  "diagnosis_status": "waiting",
  "primary_concern": "speech",
  "recommended_stage_id": "s2",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### `stages`
- **Fields:**
  - `_id`: string (custom, e.g., "s1")
  - `title`: string (required)
  - `description`: string (required)
  - `age_range`: string (required)
  - `color`: string (required, CSS class)
  - `icon`: string (required, icon name)
  - `order`: integer (required, 1-5)
  - `created_at`: datetime (required)
- **Example:**
```json
{
  "_id": "s1",
  "title": "Early Signs",
  "description": "Noticing differences and wondering what they mean.",
  "age_range": "0-3 years",
  "color": "bg-amber-100 text-amber-800",
  "icon": "Eye",
  "order": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `milestones`
- **Fields:**
  - `_id`: string (custom, e.g., "m1-1")
  - `stage_id`: string (required, references stages)
  - `title`: string (required)
  - `behavior`: string (required)
  - `why_it_matters`: string (required)
  - `if_not_yet`: string (required)
  - `reassurance`: string (required)
  - `created_at`: datetime (required)
- **Example:**
```json
{
  "_id": "m1-1",
  "stage_id": "s1",
  "title": "Observe Eye Contact",
  "behavior": "Notice if your child looks at you when you call their name or smile at them.",
  "why_it_matters": "Eye contact is a key way children connect and share attention. It helps them learn from others.",
  "if_not_yet": "Try getting down to their eye level. Hold a favorite toy near your face to encourage looking towards you.",
  "reassurance": "Many children have varying levels of eye contact. It can improve with gentle encouragement.",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `resources`
- **Fields:**
  - `_id`: string (custom, e.g., "r1")
  - `title`: string (required)
  - `description`: string (required)
  - `url`: string (required, valid URL)
  - `category`: string (required, enum: "Early Intervention", "Diagnosis", "Insurance", "IEP", "Therapy", "General")
  - `tags`: array of strings (required)
  - `created_at`: datetime (required)
- **Example:**
```json
{
  "_id": "r1",
  "title": "Autism Speaks: 100 Day Kit",
  "description": "A comprehensive guide for the first 100 days after an autism diagnosis.",
  "url": "https://www.autismspeaks.org/tool-kit/100-day-kit-young-children",
  "category": "Diagnosis",
  "tags": ["guide", "newly diagnosed"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 5️⃣ Frontend Audit & Feature Map

### Landing Page (`/`)
- **Route:** `/`
- **Purpose:** Marketing page with CTA to start journey
- **Data Needed:** None (static content)
- **Backend Endpoints:** None
- **Auth Required:** No

### Registration (`/register`)
- **Route:** `/register`
- **Purpose:** Create new user account
- **Data Needed:** Email, password, name (optional)
- **Backend Endpoints:** `POST /api/v1/auth/signup`
- **Auth Required:** No
- **Notes:** Triggers welcome email via SendGrid/Postmark

### Login (`/login`)
- **Route:** `/login`
- **Purpose:** Authenticate existing user
- **Data Needed:** Email, password
- **Backend Endpoints:** `POST /api/v1/auth/login`
- **Auth Required:** No

### Onboarding Questionnaire (`/onboarding`)
- **Route:** `/onboarding`
- **Purpose:** Collect child info and calculate recommended stage
- **Data Needed:** Child age range, diagnosis status, primary concern
- **Backend Endpoints:** `POST /api/v1/onboarding`, `GET /api/v1/onboarding`
- **Auth Required:** Yes (JWT)
- **Notes:** Implements deterministic recommendation algorithm

### Journey Timeline (`/journey`)
- **Route:** `/journey`
- **Purpose:** Display all 5 stages with progress indicators
- **Data Needed:** All stages, user's recommended stage, milestone progress per stage
- **Backend Endpoints:** `GET /api/v1/stages`, `GET /api/v1/progress`
- **Auth Required:** Yes (JWT)

### Stage Detail (`/journey/:stageId`)
- **Route:** `/journey/[id]`
- **Purpose:** Show milestones for specific stage with checkboxes
- **Data Needed:** Stage details, milestones for stage, user's completed milestones
- **Backend Endpoints:** `GET /api/v1/stages/:stageId`, `GET /api/v1/milestones?stageId=:id`, `POST /api/v1/progress/milestones/:id/toggle`
- **Auth Required:** Yes (JWT)
- **Notes:** Milestone toggle persists immediately

### Resource Library (`/resources`)
- **Route:** `/resources`
- **Purpose:** Browse/search curated resources
- **Data Needed:** All resources with category and tag filtering
- **Backend Endpoints:** `GET /api/v1/resources?category=X&search=Y`
- **Auth Required:** No (public)

### User Profile (`/profile`)
- **Route:** `/profile`
- **Purpose:** View account details and manage settings
- **Data Needed:** User profile, milestone count
- **Backend Endpoints:** `GET /api/v1/users/me`, `PATCH /api/v1/users/me`, `DELETE /api/v1/progress`
- **Auth Required:** Yes (JWT)
- **Notes:** Supports retake onboarding and reset progress

---

## 6️⃣ Configuration & ENV Vars

### Core Environment Variables
- `APP_ENV` - Environment (development, production) - default: "development"
- `PORT` - HTTP port - default: 8000
- `MONGODB_URI` - MongoDB Atlas connection string - required
- `JWT_SECRET` - Token signing key - required (generate with `openssl rand -hex 32`)
- `JWT_EXPIRES_IN` - Seconds before JWT expiry - default: 2592000 (30 days)
- `CORS_ORIGINS` - Allowed frontend URL(s) - default: "http://localhost:3000"
- `SENDGRID_API_KEY` - SendGrid API key for emails - required
- `SENDGRID_FROM_EMAIL` - Sender email address - required

### Example `.env` File
```
APP_ENV=development
PORT=8000
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/pathways?retryWrites=true&w=majority
JWT_SECRET=your-secret-key-here-generate-with-openssl
JWT_EXPIRES_IN=2592000
CORS_ORIGINS=http://localhost:3000
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@pathwaysforparents.com
```

---

## 7️⃣ Background Work

### Welcome Email (Required)
- **Trigger:** User completes registration via `POST /api/v1/auth/signup`
- **Purpose:** Send welcome email with personalized journey link
- **Implementation:** Use FastAPI `BackgroundTasks` to send email asynchronously after user creation
- **Idempotency:** Email sent only once per user (check `email_sent` flag or use unique constraint)
- **UI Check:** User sees success message immediately; email arrives within 5 minutes
- **Endpoint:** None (internal background task)

---

## 8️⃣ Integrations

### SendGrid/Postmark (Email Service)
- **Purpose:** Send transactional welcome email upon registration
- **Flow:**
  1. User submits registration form
  2. Backend creates user in MongoDB
  3. Background task triggers email send via SendGrid API
  4. Email contains: Welcome message, personalized journey link (`https://app.com/journey`), support contact
- **Extra ENV Vars:** `SENDGRID_API_KEY`, `SENDGRID_FROM_EMAIL`
- **Error Handling:** Log failure, retry once, return success to user regardless (email is async)

---

## 9️⃣ Testing Strategy (Manual via Frontend)

### Validation Approach
- Every task includes **Manual Test Step** (exact UI action + expected result)
- Every task includes **User Test Prompt** (copy-paste instruction for testing)
- After all tasks in sprint pass → commit and push to `main`
- If any task fails → fix and retest before proceeding

### Test Execution Flow
1. Complete backend task (e.g., implement signup endpoint)
2. Start backend server locally
3. Open frontend in browser
4. Execute Manual Test Step via UI
5. Verify expected result matches actual result
6. If pass → proceed to next task
7. If fail → debug, fix, retest
8. After all sprint tasks pass → commit and push to `main`

---

## 🔟 Dynamic Sprint Plan & Backlog

---

## 🧱 S0 – Environment Setup & Frontend Connection

### Objectives
- Create FastAPI skeleton with `/api/v1` base path and `/healthz` endpoint
- Connect to MongoDB Atlas using `MONGODB_URI`
- `/healthz` performs DB ping and returns JSON status
- Enable CORS for frontend
- Replace dummy API URLs in frontend with real backend URLs
- Initialize Git at root, set default branch to `main`, push to GitHub
- Create single `.gitignore` at root (ignore `__pycache__`, `.env`, `*.pyc`, `venv/`, `.vscode/`)

### User Stories
- As a developer, I can verify backend is running and connected to MongoDB Atlas
- As a frontend developer, I can call `/healthz` and see database status
- As a developer, I can push code to GitHub on `main` branch

### Tasks

#### Task 1: Initialize FastAPI Project Structure
- Create `backend/` directory at project root
- Create `backend/main.py` with FastAPI app instance
- Create `backend/requirements.txt` with dependencies:
  - `fastapi==0.115.0`
  - `uvicorn[standard]==0.32.0`
  - `motor==3.6.0`
  - `pydantic==2.9.0`
  - `pydantic-settings==2.5.0`
  - `python-jose[cryptography]==3.3.0`
  - `passlib[argon2]==1.7.4`
  - `python-multipart==0.0.12`
  - `sendgrid==6.11.0`
  - `python-dotenv==1.0.1`
- Create `backend/.env.example` with all required env vars
- Create `backend/config.py` for settings management using Pydantic Settings

**Manual Test Step:** Run `pip install -r requirements.txt` → all packages install without errors

**User Test Prompt:** "Install dependencies by running `pip install -r backend/requirements.txt` in your terminal. Confirm no errors appear."

#### Task 2: Implement `/healthz` Endpoint with MongoDB Ping
- Create `backend/database.py` with Motor async MongoDB client
- Implement connection to MongoDB Atlas using `MONGODB_URI`
- Add `/healthz` endpoint in `main.py` that:
  - Pings MongoDB using `client.admin.command('ping')`
  - Returns `{ "status": "ok", "database": "connected", "timestamp": "ISO8601" }`
  - Returns `{ "status": "error", "database": "disconnected" }` if ping fails
- Add startup event to test DB connection on app start

**Manual Test Step:** Start backend with `uvicorn backend.main:app --reload` → visit `http://localhost:8000/healthz` → see `{"status": "ok", "database": "connected", ...}`

**User Test Prompt:** "Start the backend server and navigate to `http://localhost:8000/healthz`. Confirm you see a JSON response with `status: ok` and `database: connected`."

#### Task 3: Enable CORS for Frontend
- Add `fastapi.middleware.cors.CORSMiddleware` to app
- Configure CORS to allow `CORS_ORIGINS` from env (default: `http://localhost:3000`)
- Allow credentials, all methods, all headers

**Manual Test Step:** Open frontend → open browser DevTools Network tab → refresh page → no CORS errors in console

**User Test Prompt:** "Open the frontend app in your browser, open DevTools (F12), go to the Console tab, and refresh the page. Confirm there are no CORS-related errors."

#### Task 4: Initialize Git Repository and Push to GitHub
- Run `git init` at project root (if not already initialized)
- Create `.gitignore` at root with:
  ```
  __pycache__/
  *.pyc
  *.pyo
  .env
  venv/
  .vscode/
  .DS_Store
  *.log
  ```
- Set default branch to `main`: `git branch -M main`
- Create initial commit: `git add . && git commit -m "Initial backend setup with FastAPI and MongoDB Atlas"`
- Create GitHub repo and push: `git remote add origin <repo-url> && git push -u origin main`

**Manual Test Step:** Visit GitHub repo URL → see initial commit with backend files

**User Test Prompt:** "Visit your GitHub repository in a browser. Confirm you see the initial commit with the backend directory and files."

### Definition of Done
- Backend runs locally on port 8000
- `/healthz` returns success with MongoDB Atlas connection status
- Frontend can call backend without CORS errors
- Code pushed to GitHub on `main` branch
- `.gitignore` prevents sensitive files from being committed

---

## 🧩 S1 – Basic Auth (Signup / Login / Logout)

### Objectives
- Implement JWT-based signup, login, and logout
- Store users in MongoDB with Argon2 password hashing
- Protect `/api/v1/auth/me` endpoint
- Frontend can register, login, logout, and view profile

### User Stories
- As a parent, I can create an account with email and password
- As a parent, I can log in and receive a JWT token
- As a parent, I can log out and invalidate my session
- As a parent, I can view my profile when logged in

### Tasks

#### Task 1: Create User Model and Password Hashing
- Create `backend/models/user.py` with Pydantic User model
- Fields: `id`, `email`, `password_hash`, `name`, `recommended_stage_id`, `completed_milestones`, `created_at`, `updated_at`
- Create `backend/utils/security.py` with:
  - `hash_password(password: str) -> str` using Argon2
  - `verify_password(plain: str, hashed: str) -> bool`
- Create `backend/schemas/auth.py` with request/response schemas:
  - `SignupRequest`, `LoginRequest`, `AuthResponse`, `UserResponse`

**Manual Test Step:** Run Python REPL → import `hash_password` → hash a password → verify it matches → confirm True

**User Test Prompt:** "Open a Python REPL in the backend directory and run: `from utils.security import hash_password, verify_password; h = hash_password('test123'); print(verify_password('test123', h))`. Confirm it prints `True`."

#### Task 2: Implement Signup Endpoint
- Create `backend/routers/auth.py` with APIRouter
- Implement `POST /api/v1/auth/signup`:
  - Validate email format and password length (min 8 chars)
  - Check email uniqueness in MongoDB
  - Hash password with Argon2
  - Insert user into `users` collection
  - Generate JWT token (30-day expiry)
  - Trigger welcome email in background (stub for now)
  - Return `{ "user": {...}, "token": "..." }`
- Add router to main app with `/api/v1` prefix

**Manual Test Step:** Open frontend → go to `/register` → fill form → submit → see success message → redirected to `/onboarding`

**User Test Prompt:** "Open the frontend, navigate to the registration page, create a new account with email and password, and submit. Confirm you see a success message and are redirected to the onboarding page."

#### Task 3: Implement Login Endpoint
- Implement `POST /api/v1/auth/login`:
  - Validate email format
  - Find user by email in MongoDB
  - Verify password with Argon2
  - Generate JWT token (30-day expiry)
  - Return `{ "user": {...}, "token": "..." }`
- Handle invalid credentials with 401 error

**Manual Test Step:** Open frontend → go to `/login` → enter registered email/password → submit → see "Welcome back!" → redirected to `/journey`

**User Test Prompt:** "Open the frontend, navigate to the login page, enter your registered email and password, and submit. Confirm you see a 'Welcome back!' message and are redirected to the journey page."

#### Task 4: Implement JWT Authentication Middleware
- Create `backend/utils/jwt.py` with:
  - `create_access_token(data: dict) -> str`
  - `decode_access_token(token: str) -> dict`
- Create `backend/dependencies/auth.py` with:
  - `get_current_user(token: str = Depends(oauth2_scheme)) -> User`
  - Extracts JWT from Authorization header
  - Decodes and validates token
  - Fetches user from MongoDB
  - Returns User object or raises 401

**Manual Test Step:** Use Postman/curl → call `/api/v1/auth/me` without token → get 401 → call with valid token → get user data

**User Test Prompt:** "Use Postman or curl to call `GET http://localhost:8000/api/v1/auth/me` without an Authorization header. Confirm you get a 401 error. Then call it with a valid JWT token in the header and confirm you get user data."

#### Task 5: Implement `/auth/me` and Logout Endpoints
- Implement `GET /api/v1/auth/me`:
  - Requires JWT authentication
  - Returns current user profile
- Implement `POST /api/v1/auth/logout`:
  - Requires JWT authentication
  - Returns success message (client handles token removal)

**Manual Test Step:** Open frontend → log in → go to `/profile` → see user email and name → click logout → redirected to home → try accessing `/profile` → redirected to login

**User Test Prompt:** "Log in to the frontend, navigate to the profile page, confirm you see your email and name. Click logout, confirm you're redirected to the home page. Try accessing the profile page again and confirm you're redirected to login."

### Definition of Done
- User can register via frontend and account is created in MongoDB
- User can log in and receive JWT token
- User can log out and session is invalidated
- Protected routes require valid JWT
