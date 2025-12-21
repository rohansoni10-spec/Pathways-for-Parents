# MongoDB Atlas Setup Guide for Render Deployment

## Problem
Render's free database tier only supports PostgreSQL, but this application uses MongoDB. You need to use MongoDB Atlas (which has a free tier) for your MongoDB database.

## Solution: Set up MongoDB Atlas

### Step 1: Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Create a new organization (or use existing)

### Step 2: Create a Free Cluster
1. Click "Build a Database"
2. Choose **M0 FREE** tier
3. Select a cloud provider and region (choose one close to your Render region - Oregon)
4. Name your cluster (e.g., "pathways-cluster")
5. Click "Create Cluster"

### Step 3: Configure Database Access
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and strong password (save these!)
5. Set user privileges to "Read and write to any database"
6. Click "Add User"

### Step 4: Configure Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
   - This is necessary for Render to connect
4. Click "Confirm"

### Step 5: Get Connection String
1. Go back to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Select "Driver: Python" and "Version: 3.12 or later"
5. Copy the connection string - it will look like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<username>` with your database username
7. Replace `<password>` with your database password
8. Add your database name after the `/` and before the `?`:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/pathways_db?retryWrites=true&w=majority
   ```

### Step 6: Configure Render Environment Variable
1. Go to your Render dashboard
2. Select your "pathways-backend" service
3. Go to "Environment" tab
4. Find the `MONGODB_URI` variable
5. Paste your MongoDB Atlas connection string
6. Click "Save Changes"
7. Render will automatically redeploy with the new connection string

### Step 7: Verify Deployment
1. Wait for Render to finish deploying
2. Check the logs for "✓ Successfully connected to MongoDB Atlas"
3. Your backend should now be running successfully!

## Important Notes

- **Keep your connection string secure** - never commit it to Git
- The free tier (M0) includes:
  - 512 MB storage
  - Shared RAM
  - No backup
  - Perfect for development and small projects
- If you need more resources later, you can upgrade to a paid tier

## Troubleshooting

### Connection Timeout
- Verify Network Access allows 0.0.0.0/0
- Check that your connection string is correct
- Ensure username and password are properly URL-encoded

### Authentication Failed
- Double-check username and password
- Make sure the database user has proper permissions
- Verify the connection string format

### Database Not Found
- Ensure you added the database name to the connection string
- MongoDB will create the database automatically on first write