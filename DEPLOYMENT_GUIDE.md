# Deployment Guide - Pathways for Parents

This guide covers the complete deployment process for both the backend (FastAPI) and frontend (Next.js) applications.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- [ ] GitHub account (for code repository)
- [ ] Railway/Render/Heroku account (for backend hosting)
- [ ] Vercel/Netlify account (for frontend hosting)
- [ ] PostgreSQL database (Railway/Supabase/Neon)

### Required Tools
- [ ] Git installed locally
- [ ] Node.js 18+ and npm
- [ ] Python 3.9+
- [ ] PostgreSQL client (optional, for local testing)

---

## Backend Deployment

### Option 1: Deploy to Railway (Recommended)

#### Step 1: Prepare Backend for Deployment

1. **Create a `Procfile` in the backend directory:**
```bash
cd Pathways-for-Parents/backend
```

Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Create `runtime.txt` (optional, specifies Python version):**
```
python-3.11.0
```

3. **Verify `requirements.txt` is complete:**
```bash
pip freeze > requirements.txt
```

4. **Update `.gitignore` to exclude sensitive files:**
```
.env
__pycache__/
*.pyc
.pytest_cache/
*.db
```

#### Step 2: Set Up Railway

1. **Sign up/Login to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `Pathways-for-Parents` repository

3. **Configure Backend Service:**
   - Railway will auto-detect the Python app
   - Set the root directory to `backend`
   - Railway will automatically install dependencies from `requirements.txt`

#### Step 3: Add PostgreSQL Database

1. **Add PostgreSQL Plugin:**
   - In your Railway project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will provision a database and provide connection details

2. **Get Database URL:**
   - Click on the PostgreSQL service
   - Copy the `DATABASE_URL` from the "Connect" tab
   - Format: `postgresql://user:password@host:port/database`

#### Step 4: Configure Environment Variables

In Railway project settings, add these environment variables:

```bash
# Database
DATABASE_URL=<your-railway-postgres-url>

# JWT Configuration
SECRET_KEY=<generate-a-secure-random-string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your frontend URL)
FRONTEND_URL=https://your-app.vercel.app

# Environment
ENVIRONMENT=production
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Step 5: Deploy Backend

1. **Commit and Push Changes:**
```bash
git add .
git commit -m "Prepare backend for deployment"
git push origin main
```

2. **Railway Auto-Deploy:**
   - Railway will automatically detect changes and deploy
   - Monitor deployment logs in Railway dashboard
   - Wait for deployment to complete (usually 2-5 minutes)

3. **Get Backend URL:**
   - Once deployed, Railway provides a public URL
   - Format: `https://your-app.up.railway.app`
   - Test: `https://your-app.up.railway.app/docs`

#### Step 6: Initialize Database

1. **Run Database Migrations:**
   - Railway will automatically create tables on first run
   - The app uses SQLAlchemy to create tables automatically

2. **Seed Initial Data (Optional):**
   - Access Railway's terminal or use local connection
   - Run seed script if needed:
```bash
python -c "from utils.seed_data import seed_all_data; seed_all_data()"
```

---

### Option 2: Deploy to Render

#### Step 1: Prepare Backend

Same as Railway Step 1, but create `render.yaml`:

```yaml
services:
  - type: web
    name: pathways-backend
    env: python
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: pathways-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30

databases:
  - name: pathways-db
    region: oregon
    plan: free
```

#### Step 2: Deploy to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will read `render.yaml` and set up services
5. Monitor deployment in Render dashboard

---

## Frontend Deployment

### Option 1: Deploy to Vercel (Recommended)

#### Step 1: Prepare Frontend for Deployment

1. **Create `.env.production` file:**
```bash
cd Pathways-for-Parents/frontend
```

Create `.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app/api/v1
```

2. **Update `next.config.ts` for production:**
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/:path*`,
      },
    ];
  },
};

export default nextConfig;
```

3. **Verify `package.json` scripts:**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

4. **Test production build locally:**
```bash
npm run build
npm run start
```

#### Step 2: Deploy to Vercel

1. **Sign up/Login to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Project:**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select `Pathways-for-Parents/frontend` as root directory

3. **Configure Build Settings:**
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Add Environment Variables:**
   - In project settings, add:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app/api/v1
```

5. **Deploy:**
   - Click "Deploy"
   - Vercel will build and deploy automatically
   - Deployment takes 2-5 minutes

6. **Get Frontend URL:**
   - Vercel provides: `https://your-app.vercel.app`
   - You can add custom domain later

#### Step 3: Update Backend CORS

1. **Add Frontend URL to Backend Environment:**
   - Go to Railway dashboard
   - Add/Update environment variable:
```bash
FRONTEND_URL=https://your-app.vercel.app
```

2. **Update `main.py` CORS configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware
import os

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "https://your-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Redeploy backend** (Railway auto-deploys on git push)

---

### Option 2: Deploy to Netlify

#### Step 1: Prepare Frontend

Same as Vercel Step 1, plus create `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[redirects]]
  from = "/api/*"
  to = "https://your-backend.up.railway.app/api/v1/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Step 2: Deploy to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub and select repository
4. Configure build settings (Netlify reads `netlify.toml`)
5. Add environment variables
6. Deploy

---

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT secret key (generate securely) | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `FRONTEND_URL` | Frontend URL for CORS | `https://your-app.vercel.app` |
| `ENVIRONMENT` | Environment name | `production` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-backend.up.railway.app/api/v1` |

---

## Post-Deployment Verification

### Backend Verification

1. **Check API Health:**
```bash
curl https://your-backend.up.railway.app/docs
```

2. **Test Authentication:**
```bash
curl -X POST https://your-backend.up.railway.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","full_name":"Test User"}'
```

3. **Verify Database Connection:**
   - Check Railway logs for database connection success
   - Verify tables were created

### Frontend Verification

1. **Check Homepage:**
   - Visit `https://your-app.vercel.app`
   - Verify page loads correctly

2. **Test Authentication Flow:**
   - Try registering a new user
   - Try logging in
   - Verify JWT token is stored

3. **Test API Integration:**
   - Navigate to different pages
   - Check browser console for API errors
   - Verify data loads from backend

### End-to-End Testing

1. **Complete User Journey:**
   - Register new account
   - Complete onboarding
   - View journey stages
   - Mark milestones complete
   - View resources
   - Update profile

2. **Check Logs:**
   - Backend: Railway/Render logs
   - Frontend: Vercel/Netlify logs
   - Browser: Console and Network tab

---

## Troubleshooting

### Common Backend Issues

#### Database Connection Errors
```
Error: could not connect to server
```
**Solution:**
- Verify `DATABASE_URL` is correct
- Check database is running
- Verify network access (Railway/Render firewall)

#### CORS Errors
```
Access to fetch blocked by CORS policy
```
**Solution:**
- Add frontend URL to `FRONTEND_URL` env variable
- Update CORS middleware in `main.py`
- Redeploy backend

#### Module Import Errors
```
ModuleNotFoundError: No module named 'X'
```
**Solution:**
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility
- Rebuild and redeploy

### Common Frontend Issues

#### API Connection Errors
```
Failed to fetch
```
**Solution:**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running
- Verify CORS is configured

#### Build Errors
```
Error: Cannot find module
```
**Solution:**
- Run `npm install` locally
- Verify all dependencies in `package.json`
- Check Node.js version (18+)

#### Environment Variables Not Loading
```
undefined API URL
```
**Solution:**
- Verify env variables start with `NEXT_PUBLIC_`
- Redeploy after adding env variables
- Check Vercel/Netlify dashboard

### Performance Issues

#### Slow API Responses
**Solution:**
- Check database query performance
- Add database indexes
- Enable caching
- Upgrade hosting plan

#### Frontend Loading Slowly
**Solution:**
- Enable Next.js image optimization
- Implement code splitting
- Use CDN for static assets
- Enable compression

---

## Continuous Deployment

### Automatic Deployments

Both Railway and Vercel support automatic deployments:

1. **Push to GitHub:**
```bash
git add .
git commit -m "Update feature"
git push origin main
```

2. **Automatic Build:**
   - Railway detects backend changes
   - Vercel detects frontend changes
   - Both rebuild and deploy automatically

3. **Monitor Deployments:**
   - Check Railway dashboard for backend
   - Check Vercel dashboard for frontend

### Rollback Strategy

If deployment fails:

1. **Railway/Render:**
   - Go to deployments tab
   - Click "Rollback" on previous successful deployment

2. **Vercel/Netlify:**
   - Go to deployments
   - Click "Promote to Production" on previous deployment

---

## Security Checklist

- [ ] Use strong `SECRET_KEY` (32+ characters)
- [ ] Enable HTTPS (automatic on Railway/Vercel)
- [ ] Configure CORS properly (only allow your frontend)
- [ ] Use environment variables (never commit secrets)
- [ ] Enable rate limiting (add middleware)
- [ ] Set secure cookie flags
- [ ] Implement input validation
- [ ] Use prepared statements (SQLAlchemy does this)
- [ ] Keep dependencies updated
- [ ] Monitor logs for suspicious activity

---

## Monitoring and Maintenance

### Set Up Monitoring

1. **Backend Monitoring:**
   - Railway provides built-in metrics
   - Set up error tracking (Sentry)
   - Monitor API response times

2. **Frontend Monitoring:**
   - Vercel Analytics (built-in)
   - Google Analytics
   - Error tracking (Sentry)

### Regular Maintenance

- [ ] Update dependencies monthly
- [ ] Review and rotate secrets quarterly
- [ ] Backup database weekly
- [ ] Monitor disk usage
- [ ] Review logs for errors
- [ ] Test critical user flows

---

## Cost Estimates

### Free Tier Limits

**Railway:**
- $5 free credit/month
- Suitable for development/small apps

**Vercel:**
- 100GB bandwidth/month
- Unlimited deployments
- Suitable for most projects

**Database (Railway PostgreSQL):**
- Included in Railway free tier
- 1GB storage

### Scaling Costs

As your app grows:
- Railway: ~$10-20/month (Hobby plan)
- Vercel: Free for most use cases
- Database: ~$7-15/month (dedicated)

---

## Next Steps

After successful deployment:

1. **Set up custom domain:**
   - Add domain in Vercel/Railway
   - Configure DNS records
   - Enable SSL (automatic)

2. **Set up monitoring:**
   - Add error tracking
   - Set up uptime monitoring
   - Configure alerts

3. **Optimize performance:**
   - Enable caching
   - Add CDN
   - Optimize database queries

4. **Plan for scaling:**
   - Monitor usage metrics
   - Plan database scaling
   - Consider load balancing

---

## Support Resources

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Next.js Docs:** https://nextjs.org/docs

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing locally
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] CORS configured
- [ ] Error handling implemented
- [ ] Logging configured

### Backend Deployment
- [ ] Create Railway/Render account
- [ ] Set up PostgreSQL database
- [ ] Configure environment variables
- [ ] Deploy backend
- [ ] Verify API endpoints
- [ ] Test authentication

### Frontend Deployment
- [ ] Create Vercel/Netlify account
- [ ] Configure build settings
- [ ] Set environment variables
- [ ] Deploy frontend
- [ ] Verify pages load
- [ ] Test API integration

### Post-Deployment
- [ ] Test complete user flow
- [ ] Verify all features work
- [ ] Check error logs
- [ ] Set up monitoring
- [ ] Document deployment URLs
- [ ] Update README with live URLs

---

**Congratulations!** Your Pathways for Parents application is now deployed and ready for users! 🎉