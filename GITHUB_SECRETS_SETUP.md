# GitHub Secrets Setup Guide

Step-by-step instructions for configuring GitHub Secrets required for the CI/CD pipeline.

## 🔐 Why GitHub Secrets?

GitHub Secrets securely store sensitive information (like API keys, passwords, tokens) that are:
- Encrypted at rest
- Not visible in logs or workflow files
- Only accessible to authorized workflows
- Never committed to the repository

## 📍 Location

GitHub Repository → Settings → **Secrets and variables** → **Actions**

## 🔑 Required Secrets

### 1️⃣ DOCKER_USERNAME

**What it is**: Your Docker Hub username

**Where to get it**:
1. Go to [Docker Hub](https://hub.docker.com)
2. Log in (or create account)
3. Click your profile icon → Account Settings
4. Username is displayed (e.g., `your-docker-username`)

**How to add**:
```
Name: DOCKER_USERNAME
Value: your-docker-username
```

---

### 2️⃣ DOCKER_PASSWORD

**What it is**: Docker Hub personal access token (or password)

**⚠️ IMPORTANT: Use Personal Access Token, not password**

**How to create PAT**:
1. Go to [Docker Hub Account Settings](https://hub.docker.com/settings/security)
2. Click **New Access Token**
3. Give it a name: "GitHub Actions"
4. Select permissions:
   - ✅ Read, write, delete
5. Click **Generate**
6. **Copy the token** (you won't see it again!)

**How to add**:
```
Name: DOCKER_PASSWORD
Value: <paste-your-access-token>
```

---

### 3️⃣ RENDER_API_KEY

**What it is**: Render.com API key for programmatic deployments

**How to create**:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click your profile → **Account Settings**
3. Left sidebar → **API Keys**
4. Click **Create API Key**
5. Give it a name: "GitHub Actions"
6. Click **Generate**
7. **Copy the key** (shown only once!)

**How to add**:
```
Name: RENDER_API_KEY
Value: <paste-your-api-key>
```

---

### 4️⃣ RENDER_BACKEND_SERVICE_ID

**What it is**: The unique ID of your backend service on Render

**How to find it**:
1. Deploy your backend on Render first (see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md))
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click on your **backend service**
4. Go to **Settings** tab
5. Copy the **Service ID** (format: `srv-abc123xyz456`)

**How to add**:
```
Name: RENDER_BACKEND_SERVICE_ID
Value: srv-abc123xyz456
```

---

### 5️⃣ RENDER_FRONTEND_SERVICE_ID

**What it is**: The unique ID of your frontend service on Render

**How to find it**:
1. Deploy your frontend on Render first (see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md))
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click on your **frontend service**
4. Go to **Settings** tab
5. Copy the **Service ID** (format: `srv-def789uvw012`)

**How to add**:
```
Name: RENDER_FRONTEND_SERVICE_ID
Value: srv-def789uvw012
```

---

## ✅ Step-by-Step: Adding Secrets via GitHub Web UI

### Method 1: Using GitHub Web Interface (Easiest)

1. **Open your repository** on GitHub
2. Click **Settings** tab (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. **Name**: `DOCKER_USERNAME`
6. **Value**: `your-docker-username`
7. Click **Add secret**
8. **Repeat** for each secret

### Method 2: Using GitHub CLI (Faster)

Prerequisites: [Install GitHub CLI](https://cli.github.com)

```bash
# Login to GitHub (first time only)
gh auth login

# Add each secret
gh secret set DOCKER_USERNAME --body "your-docker-username"
gh secret set DOCKER_PASSWORD --body "your-access-token"
gh secret set RENDER_API_KEY --body "your-render-api-key"
gh secret set RENDER_BACKEND_SERVICE_ID --body "srv-xxxxx"
gh secret set RENDER_FRONTEND_SERVICE_ID --body "srv-yyyyy"

# Verify secrets are set
gh secret list
```

---

## 🔍 Verifying Secrets Are Set

### Via GitHub Web UI:
1. **Settings** → **Secrets and variables** → **Actions**
2. You should see all 5 secrets listed (values hidden for security)

### Via GitHub CLI:
```bash
gh secret list
```

Output example:
```
DOCKER_PASSWORD         Updated 2024-01-06
DOCKER_USERNAME         Updated 2024-01-06
RENDER_API_KEY          Updated 2024-01-06
RENDER_BACKEND_SERVICE_ID   Updated 2024-01-06
RENDER_FRONTEND_SERVICE_ID  Updated 2024-01-06
```

---

## 🧪 Testing the Secrets

After adding all secrets, test by:

1. **Push code** to `production` branch
2. **Go to Actions** tab in GitHub
3. **Click the workflow** (`CI/CD Pipeline`)
4. **Monitor the run**:
   - ✅ Tests should pass
   - ✅ Build should succeed
   - ✅ Docker images should push
   - ✅ Deployment should trigger

If any step fails, check the logs for error messages.

---

## ⚠️ Security Best Practices

✅ **DO:**
- Use **personal access tokens** instead of passwords for Docker Hub
- Use **API keys** instead of passwords for Render
- **Rotate keys** every 90 days (optional but recommended)
- Review secret access in repository settings
- Use **least privilege** permissions (only what's needed)

❌ **DON'T:**
- Share secrets in repositories
- Use passwords as secrets
- Commit `.env` files with secrets
- Share secrets in Slack, email, or chat
- Use same secret for multiple services

---

## 🔄 Updating Secrets

To update a secret value:

1. **Settings** → **Secrets and variables** → **Actions**
2. Click the secret to update
3. Click **Update**
4. Enter new value
5. Click **Update secret**

---

## 🗑️ Removing Secrets

To remove a secret (e.g., if compromised):

1. **Settings** → **Secrets and variables** → **Actions**
2. Click the secret to remove
3. Click **Delete**
4. Confirm deletion

---

## 🆘 Troubleshooting

### Secret Not Found in Workflow

**Error message**: `Secret not found or inaccessible`

**Solution**:
- Check secret **name** matches exactly (case-sensitive)
- Verify secret is in **Settings → Secrets** (not "Variables")
- Secret must be in same organization/repository

### Workflow Fails to Authenticate

**Error**: `Authentication failed` or `401 Unauthorized`

**Solution**:
- Verify secret values are correct (copy-paste carefully)
- Check if tokens are expired (regenerate if needed)
- Ensure permissions are correct (Docker read/write, Render admin)

### Docker Push Fails

**Error**: `denied: permission denied`

**Solution**:
- Verify `DOCKER_USERNAME` matches Docker Hub account
- Verify `DOCKER_PASSWORD` is valid access token
- Check token has "Read, Write, Delete" permissions
- Ensure repository name in workflow matches Docker Hub

### Render Deployment Fails

**Error**: `Service not found` or `Authentication failed`

**Solution**:
- Verify `RENDER_API_KEY` is current (not expired)
- Verify `RENDER_BACKEND_SERVICE_ID` and `RENDER_FRONTEND_SERVICE_ID` are correct
- Check Service IDs haven't changed (get fresh ones from Render)
- Ensure Render account has permission to deploy

---

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub CLI Documentation](https://cli.github.com)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [Render API Documentation](https://render.com/docs/api-reference)

---

## ✨ What's Next?

After secrets are set up:

1. ✅ Push code to `production` branch
2. ✅ Monitor **Actions** tab for pipeline execution
3. ✅ Check **Docker Hub** for pushed images
4. ✅ Verify **Render deployment** is working
5. ✅ Test deployed application in browser
