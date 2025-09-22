# DOMAIN-SETUP.md

## Introduction
This document provides step-by-step instructions for setting up the custom domain **hustleandheal.com** for your project hosted on Vercel (frontend) and Railway (backend).

## Connecting hustleandheal.com to Vercel (Frontend)

### Step 1: Log in to your Vercel account
Go to [Vercel](https://vercel.com) and log in to your account.

### Step 2: Navigate to the project settings
Select your project from the dashboard and go to the settings.

### Step 3: Add the custom domain
In the "Domains" section, enter your custom domain **hustleandheal.com** and click "Add".

### Step 4: DNS Setup with Your Registrar
Follow these instructions based on your domain registrar:

#### For GoDaddy:
1. Log in to your GoDaddy account.
2. Navigate to "Domains" and select **hustleandheal.com**.
3. Click on "Manage DNS".
4. Add the following DNS records:
   - Type: A
     - Name: @
     - Value: [Vercel's IP address]
   - Type: CNAME
     - Name: www
     - Value: cname.vercel-dns.com

#### For Namecheap:
1. Log in to your Namecheap account.
2. Go to "Domain List" and select **hustleandheal.com**.
3. Click on "Manage".
4. Add the DNS records similar to GoDaddy.

## Using Railway for Backend

### Step 1: Log in to your Railway account
Visit [Railway](https://railway.app) and sign in.

### Step 2: Create or select a project
Create a new project or select an existing one.

### Step 3: Link your project to the custom domain
In the project settings, navigate to the domain section and add **hustleandheal.com**.

### Optional: Setting up a Subdomain (e.g., api.hustleandheal.com)
1. In Railway, create a new subdomain in the domains section.
2. Follow similar DNS instructions as above to point `api.hustleandheal.com` to your Railway project.

## Copy-Pasteable Instructions for Non-Technical Users
1. Log in to Vercel and add the domain hustleandheal.com in project settings.
2. Set up DNS records with your registrar as follows:
   - GoDaddy: Add A record with Vercel's IP and CNAME record as described.
   - Namecheap: Follow similar steps.
3. For Railway, log in, link your project to hustleandheal.com, and set up a subdomain if desired.

## Troubleshooting Tips
- **Domain not verified?** Ensure DNS records are correctly set and wait for propagation (may take up to 48 hours).
- **Check official documentation:**
  - [Vercel Documentation](https://vercel.com/docs)
  - [Railway Documentation](https://railway.app/docs)