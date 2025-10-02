# Quick Start: Setting Up Your API Key

This guide answers the common question: **"How do I set up my API key?"**

## TL;DR - Quick Answer

**NO, do NOT put your API key as a comment in .env!**

Use this format:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

NOT this:
```bash
# OPENAI_API_KEY=sk-your-key  ❌ Won't work - it's commented out!
```

---

## Step-by-Step Setup

### 1. Copy the Example File

```bash
cp .env.example .env
```

### 2. Edit the .env File

Open `.env` in your text editor and find this line:

```bash
# OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Change it to** (remove the # and add your real key):

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-from-openai
```

### 3. Get Your API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create an OpenAI account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. Paste it in your `.env` file

### 4. Verify Your Setup

Run this to test if it works:

```bash
python3 << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv('.env')
api_key = os.getenv("OPENAI_API_KEY")

if api_key and api_key.startswith('sk-'):
    print("✅ API key is set up correctly!")
else:
    print("❌ API key not found or incorrect format")
    print("   Make sure the line is NOT commented out with #")
EOF
```

---

## Common Mistakes & How to Fix Them

### ❌ Mistake 1: Leaving the # (Comment)

```bash
# OPENAI_API_KEY=sk-your-key
```

**Why it's wrong**: Lines starting with `#` are comments and ignored by the application.

**Fix**: Remove the `#`:
```bash
OPENAI_API_KEY=sk-your-key
```

---

### ❌ Mistake 2: Missing = Sign

```bash
OPENAI_API_KEYsk-your-key
```

**Why it's wrong**: Environment variables need an `=` sign to separate the name from the value.

**Fix**: Add the `=`:
```bash
OPENAI_API_KEY=sk-your-key
```

---

### ❌ Mistake 3: Spaces Around =

```bash
OPENAI_API_KEY = sk-your-key
```

**Why it's wrong**: Some parsers don't handle spaces around `=` correctly.

**Fix**: Remove spaces:
```bash
OPENAI_API_KEY=sk-your-key
```

---

### ❌ Mistake 4: API Key in a Comment

```bash
# My API key is: sk-your-key-here
```

**Why it's wrong**: 
1. The application can't read it
2. It's still visible in the file (security risk if committed)

**Fix**: Use proper format and NEVER commit `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

---

## Security Checklist

Before you start using the application:

- [ ] I copied `.env.example` to `.env`
- [ ] I added my real API key to `.env`
- [ ] I removed the `#` comment from the API key line
- [ ] I verified the format: `OPENAI_API_KEY=sk-...` (no spaces)
- [ ] I checked that `.env` is in `.gitignore`
- [ ] I will NEVER commit `.env` to git
- [ ] I understand to revoke exposed API keys immediately

---

## Your .env File Should Look Like This

```bash
# Flask Configuration
FLASK_DEBUG=false

# Application Security
SECRET_KEY=your-very-secure-random-key-change-in-production

# AI Integration (Optional)
# Remove the # below and add your actual key
OPENAI_API_KEY=sk-proj-abc123xyz456def789...

# Server Configuration (Optional)
# HOST=0.0.0.0
# PORT=5000
```

**Key Points**:
- ✅ `OPENAI_API_KEY` line has NO `#` at the start
- ✅ No spaces around the `=` sign
- ✅ The actual API key is on the same line
- ✅ Other optional settings can stay commented out with `#`

---

## Need More Help?

- **Security Best Practices**: See [SECURITY.md](SECURITY.md)
- **Full Setup Guide**: See [README.md](README.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Important Security Warning

⚠️ **NEVER commit your `.env` file to git!**

The `.env` file is already in `.gitignore`, but if you accidentally commit it:

1. **Immediately revoke the API key** at https://platform.openai.com/api-keys
2. Generate a new API key
3. Remove `.env` from git: `git rm --cached .env`
4. Update your `.env` with the new key

**Remember**: An exposed API key is compromised forever, even if you delete it from git history!
