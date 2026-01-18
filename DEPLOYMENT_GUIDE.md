# 🚀 Deployment Guide - Performatives Platform

## Quick Deployment Options (Easiest to Hardest)

### 🌟 Best Options for Get Started Fast

1. **Railway** ⭐ RECOMMENDED - Easiest full-stack deployment
2. **Render** - Good free tier, easy setup
3. **Vercel + Render** - Best for Next.js + APIs
4. **DigitalOcean App Platform** - Balanced ease + control
5. **AWS/GCP** - Most powerful, more complex

---

## Option 1: Railway (All-in-One) ⭐ RECOMMENDED

**Best for:** Complete platform deployment with zero configuration

**Pros:**
- ✅ Deploy entire docker-compose with one click
- ✅ Automatic SSL certificates
- ✅ Built-in PostgreSQL
- ✅ GitHub integration
- ✅ Free tier: $5/month credit

### Step-by-Step

1. **Sign up at [railway.app](https://railway.app)**

2. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

3. **Deploy from your repo:**
   ```bash
   cd d:\cohort1\Performatives
   railway init
   railway up
   ```

4. **Configure services:**
   - Railway auto-detects docker-compose.yml
   - It will create services for each container
   - PostgreSQL is automatically provisioned

5. **Set environment variables:**
   ```bash
   railway variables set SECRET_KEY=your-production-secret-key
   railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```

6. **Generate domains:**
   ```bash
   railway domain
   ```

**Result:** Your platform will be live at `https://your-app.railway.app`

**Cost:** ~$10-20/month for all services

---

## Option 2: Render (Free Tier Available)

**Best for:** Individual service deployment with generous free tier

### Deploy Backend APIs (problem-1, prob-4)

1. **Go to [render.com](https://render.com)**

2. **New Web Service → Connect GitHub repo**

3. **Configure for each API:**

   **For problem-1:**
   - Name: `performatives-matching-api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3
   - Instance Type: Free (or Starter $7/month)

   **For prob-4:**
   - Name: `performatives-ats-api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add PostgreSQL database (free tier available)
   - Environment Variables:
     ```
     DATABASE_URL=${{Postgres.DATABASE_URL}}
     SECRET_KEY=your-secret-key-here
     ```

### Deploy Frontend (prob-3, problem-5)

**Use Vercel (recommended for frontends):**

1. **Go to [vercel.com](https://vercel.com)**

2. **Import GitHub repo**

3. **Configure projects:**
   
   **For prob-3 (React):**
   - Root Directory: `prob-3`
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

   **For problem-5 (Next.js):**
   - Root Directory: `problem-5`
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

**Result:**
- Frontend: `https://your-app.vercel.app`
- APIs: `https://your-api.onrender.com`

**Cost:** Free tier available (Render free + Vercel free)

---

## Option 3: DigitalOcean App Platform

**Best for:** Docker-based deployment with good pricing

### Steps

1. **Create account at [digitalocean.com](https://digitalocean.com)**

2. **Create App → Use GitHub repo**

3. **Configure from docker-compose:**
   - DigitalOcean auto-detects Dockerfile
   - Choose "Docker Compose" as source

4. **Set up database:**
   - Add managed PostgreSQL database
   - Link to prob-4 service

5. **Configure domains:**
   - Free SSL certificates
   - Custom domain support

**Cost:** ~$12-25/month for basic setup

---

## Option 4: AWS (Most Powerful)

**Best for:** Production, enterprise-grade deployment

### Architecture: ECS + RDS + ALB

```
┌─────────────────────────────────────────┐
│  Route 53 (DNS)                         │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│  CloudFront (CDN) + ACM (SSL)           │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│  Application Load Balancer              │
└─────────────────────────────────────────┘
         │              │              │
    ┌────────┐    ┌────────┐    ┌────────┐
    │ ECS    │    │ ECS    │    │ ECS    │
    │ prob-3 │    │ prob-4 │    │ prob-5 │
    └────────┘    └────────┘    └────────┘
                       │
                  ┌────────┐
                  │  RDS   │
                  │ Postgres│
                  └────────┘
```

### Quick Deploy with ECS

1. **Install AWS CLI:**
   ```bash
   aws configure
   ```

2. **Push images to ECR:**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and push each service
   docker build -t performatives-prob3 ./prob-3
   docker tag performatives-prob3:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/performatives-prob3:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/performatives-prob3:latest
   ```

3. **Create ECS cluster:**
   ```bash
   aws ecs create-cluster --cluster-name performatives
   ```

4. **Deploy with CloudFormation or Terraform**

**Cost:** ~$50-100/month minimum

---

## Option 5: Simple VPS (DigitalOcean Droplet)

**Best for:** Full control, simplest cloud deployment

### Steps

1. **Create Droplet:**
   - Ubuntu 22.04
   - 2GB RAM minimum ($12/month)
   - Add SSH key

2. **SSH into server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install docker-compose
   apt install docker-compose -y
   ```

4. **Clone your repo:**
   ```bash
   git clone https://github.com/AgroKING/Performatives.git
   cd Performatives
   ```

5. **Set environment variables:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your secrets
   ```

6. **Start services:**
   ```bash
   docker-compose up -d
   ```

7. **Configure domain (optional):**
   - Point your domain to server IP
   - Install Nginx for SSL:
     ```bash
     apt install certbot python3-certbot-nginx
     certbot --nginx -d yourdomain.com
     ```

**Result:** Platform running at `http://your-server-ip`

**Cost:** $12-24/month

---

## Option 6: Free Static Hosting (Frontend Only)

### Deploy Static Frontends

**problem-1 UI + prob-4 frontend → GitHub Pages**

1. **Build static files:**
   ```bash
   # For problem-1 (already static)
   # Just commit index.html
   
   # For prob-4 frontend (already static)
   # Just commit frontend/index.html
   ```

2. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/` (root)

3. **Access at:**
   - `https://agroking.github.io/Performatives/problem-1/index.html`
   - `https://agroking.github.io/Performatives/prob-4/frontend/index.html`

**For prob-3 (React) → Vercel:**
```bash
cd prob-3
npm run build
npx vercel --prod
```

**For problem-5 (Next.js) → Vercel:**
```bash
cd problem-5
npx vercel --prod
```

**Note:** Backend APIs still need hosting (use Render/Railway free tier)

---

## 🎯 Recommended Complete Setup

### Free Tier (Great for Demo)

**Frontends:**
- prob-3 → Vercel (free)
- problem-5 → Vercel (free)
- problem-1 UI → GitHub Pages (free)
- prob-4 frontend → GitHub Pages (free)

**Backends:**
- problem-1 API → Render (free tier)
- prob-4 API → Render (free tier + free PostgreSQL)

**Total Cost: $0/month** ✅

---

### Production Ready ($20-30/month)

**All Services:**
- Railway (all-in-one deployment)
- Includes PostgreSQL, SSL, auto-scaling
- Professional custom domain

**Total Cost: ~$20-30/month** 💰

---

### Enterprise Grade ($100+/month)

**AWS Setup:**
- ECS for containers
- RDS for PostgreSQL
- CloudFront CDN
- Route 53 DNS
- Auto-scaling enabled

**Total Cost: ~$100-200/month** 🏢

---

## Environment Variables for Production

Create `.env.production`:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/db_name

# Security
SECRET_KEY=generate-strong-random-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your domains)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (if using SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## SSL/HTTPS Setup

### Option A: Automatic (Railway/Render/Vercel)
- SSL certificates automatically provided
- No configuration needed

### Option B: Let's Encrypt (VPS)
```bash
certbot --nginx -d yourdomain.com
```

### Option C: Cloudflare (Free CDN + SSL)
1. Add domain to Cloudflare
2. Update nameservers
3. Enable "Full" SSL mode

---

## Database Migration

### For Production PostgreSQL:

1. **Export local data:**
   ```bash
   docker-compose exec postgres pg_dump -U ats_user ats_db > backup.sql
   ```

2. **Import to production:**
   ```bash
   psql $DATABASE_URL < backup.sql
   ```

### For Alembic migrations:
```bash
alembic upgrade head
```

---

## Monitoring & Logging

### Free Options:
- **UptimeRobot** - Health check monitoring
- **Better Stack** - Log aggregation
- **Sentry** - Error tracking (free tier)

### Paid Options:
- **Datadog** - Full observability
- **New Relic** - APM
- **CloudWatch** (AWS)

---

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 🎯 My Recommendation for You

**Start with Railway (Option 1)**

**Why:**
1. Deploy entire platform in 5 minutes
2. One command: `railway up`
3. Automatic SSL, PostgreSQL, scaling
4. $5 free credit to test
5. Easy to upgrade later

**Steps:**
```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd d:\cohort1\Performatives
railway init
railway up

# Done! You'll get a URL like:
# https://performatives.railway.app
```

**Alternative for $0/month:**
- Use Vercel (frontends) + Render free tier (backends)
- Takes longer to set up but completely free

---

**Need help with deployment? Let me know which option you want and I can provide detailed commands!** 🚀
