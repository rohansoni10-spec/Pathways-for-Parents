# Deployment Checklist - Quick Reference

Use this checklist to ensure a smooth deployment process.

---

## 🎯 Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing locally (`pytest` for backend, `npm test` for frontend)
- [ ] No console errors in browser
- [ ] Code reviewed and committed to main branch
- [ ] `.gitignore` properly configured (no secrets committed)

### Environment Setup
- [ ] Backend `.env.example` is up to date
- [ ] Frontend environment variables documented
- [ ] Database schema is finalized
- [ ] All dependencies listed in `requirements.txt` and `package.json`

---

## 🔧 Backend Deployment Steps

### 1. Prepare Backend Files
- [ ] `Procfile` created
- [ ] `runtime.txt` created (optional)
- [ ] `render.yaml` created (if using Render)
- [ ] `requirements.txt` is complete

### 2. Set Up Hosting Platform
**Railway (Recommended):**
- [ ] Sign up at [railway.app](https://railway.app)
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Set root directory to `backend`

**OR Render:**
- [ ] Sign up at [render.com](https://render.com)
- [ ] Create new Blueprint
- [ ] Connect GitHub repository

### 3. Add PostgreSQL Database
- [ ] Add PostgreSQL service/plugin
- [ ] Copy `DATABASE_URL` connection string
- [ ] Verify database is running

### 4. Configure Environment Variables
Add these in your hosting platform:
```bash
DATABASE_URL=<from-database-service>
SECRET_KEY=<generate-secure-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=<will-add-after-frontend-deploy>
ENVIRONMENT=production
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Deploy Backend
- [ ] Push code to GitHub
- [ ] Platform auto-deploys
- [ ] Monitor deployment logs
- [ ] Wait for successful deployment

### 6. Verify Backend
- [ ] Visit `https://your-backend-url.com/docs`
- [ ] Test API endpoints
- [ ] Check database connection in logs
- [ ] Verify tables were created

**Save Backend URL:** `_______________________________`

---

## 🎨 Frontend Deployment Steps

### 1. Prepare Frontend Files
- [ ] `.env.production` created with backend URL
- [ ] `vercel.json` created (if using Vercel)
- [ ] `netlify.toml` created (if using Netlify)
- [ ] Test production build locally: `npm run build && npm start`

### 2. Set Up Hosting Platform
**Vercel (Recommended):**
- [ ] Sign up at [vercel.com](https://vercel.com)
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Framework preset: Next.js

**OR Netlify:**
- [ ] Sign up at [netlify.com](https://netlify.com)
- [ ] Import GitHub repository
- [ ] Set build settings

### 3. Configure Environment Variables
Add in hosting platform:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com/api/v1
```

### 4. Deploy Frontend
- [ ] Click "Deploy"
- [ ] Monitor build logs
- [ ] Wait for successful deployment

### 5. Verify Frontend
- [ ] Visit frontend URL
- [ ] Test all pages load
- [ ] Check browser console for errors
- [ ] Test API integration

**Save Frontend URL:** `_______________________________`

---

## 🔄 Update Backend CORS

### Add Frontend URL to Backend
- [ ] Go to backend hosting platform
- [ ] Add/update environment variable:
```bash
FRONTEND_URL=https://your-frontend-url.com
```
- [ ] Backend will auto-redeploy
- [ ] Verify CORS works (test login/register)

---

## ✅ Post-Deployment Verification

### End-to-End Testing
- [ ] Register new user account
- [ ] Login successfully
- [ ] Complete onboarding flow
- [ ] View journey stages
- [ ] Mark milestones as complete
- [ ] View resources
- [ ] Update profile
- [ ] Logout and login again

### Check Logs
- [ ] Backend logs show no errors
- [ ] Frontend logs show no errors
- [ ] Browser console shows no errors
- [ ] Network tab shows successful API calls

### Performance Check
- [ ] Pages load in < 3 seconds
- [ ] API responses in < 1 second
- [ ] No memory leaks
- [ ] Mobile responsive

---

## 📊 Monitoring Setup

### Set Up Monitoring (Optional but Recommended)
- [ ] Enable Railway/Render metrics
- [ ] Enable Vercel Analytics
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up email alerts

---

## 🔒 Security Checklist

- [ ] Strong `SECRET_KEY` (32+ characters)
- [ ] HTTPS enabled (automatic)
- [ ] CORS properly configured
- [ ] No secrets in code/commits
- [ ] Environment variables secured
- [ ] Database credentials secured
- [ ] Rate limiting considered
- [ ] Input validation implemented

---

## 📝 Documentation Updates

- [ ] Update README with live URLs
- [ ] Document deployment process
- [ ] Add troubleshooting guide
- [ ] Update API documentation
- [ ] Create user guide (optional)

---

## 🚀 Going Live

### Final Steps
- [ ] Test with real users
- [ ] Monitor for 24 hours
- [ ] Fix any issues
- [ ] Announce launch! 🎉

### URLs to Share
- **Frontend:** `_______________________________`
- **Backend API:** `_______________________________`
- **API Docs:** `_______________________________/docs`

---

## 🆘 Quick Troubleshooting

### Backend Issues
**Database Connection Error:**
- Check `DATABASE_URL` is correct
- Verify database is running
- Check network/firewall settings

**CORS Error:**
- Add frontend URL to `FRONTEND_URL` env var
- Redeploy backend
- Clear browser cache

**Module Not Found:**
- Check `requirements.txt` is complete
- Verify Python version
- Rebuild and redeploy

### Frontend Issues
**API Connection Error:**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running
- Test API endpoint directly

**Build Error:**
- Run `npm install` locally
- Check Node.js version (18+)
- Review build logs

**Environment Variables Not Loading:**
- Ensure vars start with `NEXT_PUBLIC_`
- Redeploy after adding vars
- Check platform dashboard

---

## 📞 Support Resources

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Next.js Docs:** https://nextjs.org/docs

---

## 💰 Cost Tracking

### Free Tier Limits
- **Railway:** $5 credit/month
- **Vercel:** 100GB bandwidth/month
- **Render:** 750 hours/month

### Monitor Usage
- [ ] Check Railway usage weekly
- [ ] Monitor Vercel bandwidth
- [ ] Review database storage
- [ ] Plan for scaling if needed

---

## 🎯 Next Steps After Deployment

1. **Custom Domain (Optional):**
   - [ ] Purchase domain
   - [ ] Configure DNS
   - [ ] Add to Vercel/Railway
   - [ ] Enable SSL (automatic)

2. **Performance Optimization:**
   - [ ] Enable caching
   - [ ] Optimize images
   - [ ] Add CDN
   - [ ] Database indexing

3. **Feature Additions:**
   - [ ] Analytics
   - [ ] Email notifications
   - [ ] Social sharing
   - [ ] Mobile app (future)

---

**Deployment Date:** `_______________`

**Deployed By:** `_______________`

**Version:** `_______________`

---

✅ **Deployment Complete!** Your app is now live and ready for users! 🎉