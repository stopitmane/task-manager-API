# 🚀 Railway Deployment Guide

## Quick Fix for PORT Issue

The error you encountered is because Railway's `$PORT` environment variable wasn't being recognized. Here's the **correct solution**:

### **Step 1: Use the Correct Procfile**
Your `Procfile` should contain:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **Step 2: Deploy to Railway**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Fix Railway deployment"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect it's a Python app

3. **Set Environment Variables:**
   - Go to your project settings
   - Add these variables:
     ```
     DATABASE_URL=sqlite:///./task_management.db
     SECRET_KEY=your-super-secret-key-here
     ```

### **Step 3: Railway Will Handle PORT Automatically**

Railway automatically:
- ✅ Sets the `$PORT` environment variable
- ✅ Provides the correct port number
- ✅ Handles the deployment process

### **Step 4: Your API Will Be Live**

Once deployed, your API will be available at:
```
https://your-app-name.railway.app
```

## 🔧 **Troubleshooting**

### **If you still get PORT errors:**

1. **Check Railway Logs:**
   - Go to your Railway project
   - Click on "Deployments"
   - Check the logs for errors

2. **Alternative Procfile (if needed):**
   ```
   web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Manual Port Setting:**
   - In Railway dashboard, add environment variable:
     ```
     PORT=8000
     ```

## 🎯 **Expected Behavior**

When Railway deploys successfully, you should see:
- ✅ Build completes without errors
- ✅ Application starts on the assigned port
- ✅ Health check endpoint works: `https://your-app.railway.app/health`
- ✅ API docs available: `https://your-app.railway.app/docs`

## 📊 **Testing Your Live API**

Once deployed, test these endpoints:

```bash
# Health check
curl https://your-app-name.railway.app/health

# API info
curl https://your-app-name.railway.app/info

# Register user
curl -X POST https://your-app-name.railway.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"password123"}'
```

## 🎉 **Success!**

Your Task Management System API will be:
- ✅ **Live and accessible** from anywhere
- ✅ **Professional documentation** available
- ✅ **Ready for portfolio** showcasing
- ✅ **Demonstrating deployment** skills

**The Railway deployment should work perfectly now!** 🚀 