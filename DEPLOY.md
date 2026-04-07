# OpenReturn — Deployment Guide

## What You're Deploying
- Free tax education tool for Tax Years 2023, 2024, and 2025
- No user data is stored — everything lives in browser memory only
- No SSNs, bank details, or names are ever collected
- RAG-powered guidance from official IRS publications

---

## Step 1: Get Your Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Click "Sign Up" — completely free, no credit card
3. Go to "API Keys" in the left sidebar
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)
6. Save it somewhere safe

## Step 2: Set Up Locally First
1. Open Terminal on your Mac
2. Navigate to the openreturn folder:
   ```
   cd path/to/openreturn
   ```
3. Check your Python version (3.9+ required):
   ```
   python3 --version
   ```
4. Create a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   This installs ~50 packages including PyTorch and sentence-transformers.
   First install takes 5-10 minutes.
6. Copy the env example:
   ```
   cp .env.example .env
   ```
7. Open .env and paste your Groq key:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```
8. Run the app:
   ```
   streamlit run app.py
   ```
9. Open http://localhost:8501 in your browser
10. On first launch, the app will automatically download and index IRS documents
    (36 documents across 3 tax years — takes 5-10 minutes). You'll see a progress
    bar. After that, it's instant on subsequent launches.
11. Test the full flow end to end

**Alternative:** If you prefer to run ingestion separately:
```
python ingestion/ingest.py
```

## Step 3: Push to GitHub
1. Go to github.com and create a new repository called "openreturn"
2. Make it Public
3. Do NOT initialize with README (we have our own)
4. In Terminal (inside openreturn/ folder):
   ```
   git init
   git add .
   git commit -m "Initial commit — OpenReturn v1"
   git remote add origin https://github.com/dokababa/openreturn.git
   git push -u origin main
   ```
5. Go to github.com/dokababa/openreturn — you should see all your files
6. The README.md will render as the repo homepage with full docs

**What gets pushed:** All source code, requirements, README, DEPLOY guide.
**What does NOT get pushed (.gitignore):** `.env`, `.venv/`, `rag/chroma_store/`, `__pycache__/`

## Step 4: Deploy to Hugging Face Spaces
1. Go to huggingface.co and create a free account (or log in)
2. Click your profile picture → "New Space"
3. Fill in:
   - Owner: your username
   - Space name: openreturn
   - License: MIT
   - SDK: Streamlit
   - Hardware: CPU Basic (free)
4. Click "Create Space"
5. You now have an empty Space — deploy by pushing from GitHub:

   **Option A — Connect GitHub directly (recommended):**
   1. In your Space, go to Settings → Repository
   2. Click "Connect to GitHub repository"
   3. Select dokababa/openreturn
   4. It will auto-deploy on every git push

   **Option B — Push directly to Hugging Face:**
   1. In Terminal:
      ```
      git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/openreturn
      git push hf main
      ```

## Step 5: Add Your Groq API Key to Hugging Face
IMPORTANT — never put your API key in the code or commit it to GitHub.
Hugging Face has a secrets manager for this:

1. Go to your Space on huggingface.co
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Click "New secret"
5. Name: `GROQ_API_KEY`
6. Value: paste your `gsk_...` key
7. Click "Save"

The app will automatically read this secret as an environment variable.

## Step 6: ChromaDB on Hugging Face (Automatic)
The app handles this automatically now. On first launch on Hugging Face Spaces,
it will:
1. Detect that ChromaDB is empty
2. Show a progress bar and download all 36 IRS documents
3. Chunk, embed, and index them into ChromaDB
4. Reload the app when done

This takes about 5-10 minutes on first launch. After that, ChromaDB persists
for the lifetime of that Space instance.

**Note:** If the Space restarts (goes to sleep and wakes up), it will re-ingest
automatically. This is fine for a free tool — the first user after a restart
just waits a few minutes.

## Step 7: Verify Deployment
1. Go to huggingface.co/spaces/YOUR_USERNAME/openreturn
2. Wait for the build to complete (2-5 minutes first time)
3. Wait for auto-ingestion to finish (5-10 minutes on first launch)
4. You should see the OpenReturn landing page
5. Test the full flow:
   - Pick a tax year (2025, 2024, or 2023)
   - Answer the interview questions
   - See your required forms
   - Get line-by-line guidance
   - Accept the disclaimer
   - Download the PDF
6. Share the URL!

## Your Live URL Will Be:
https://huggingface.co/spaces/dokababa/openreturn

## Updating the App Later
Every time you make changes:
1. Test locally first: `streamlit run app.py`
2. Commit: `git add . && git commit -m "your update message"`
3. Push to GitHub: `git push origin main`
4. If connected to HF, it auto-deploys. Otherwise: `git push hf main`

## Troubleshooting

**"Groq API key not found"**
- Locally: make sure `.env` exists with your key
- On HF Spaces: add it as a Repository Secret (Step 5)

**Ingestion is slow or fails**
- Some IRS PDFs may be temporarily unavailable — the app skips those and continues
- Check your internet connection
- The app will use whatever documents it successfully downloads

**App shows "Something went wrong"**
- Check the terminal/logs for the actual Python error
- Most common cause: Groq rate limit (14,400 requests/day free)
- The app has built-in retry with backoff for rate limits

**Python version issues**
- The app works on Python 3.9+
- If you have issues with `python`, try `python3`
