# Email Setup Guide

This application uses Resend API to send verification codes via email.

## Setup Instructions

### 1. Create a Resend Account
1. Go to https://resend.com
2. Sign up for a free account
3. Verify your email address

### 2. Get Your API Key
1. Go to https://resend.com/api-keys
2. Click "Create API Key"
3. Give it a name (e.g., "Job Tracker Production")
4. Copy the API key

### 3. Add API Key to Cloudflare Worker
Run this command in your terminal:

```bash
wrangler secret put RESEND_API_KEY
```

When prompted, paste your Resend API key.

### 4. Verify Your Domain (Optional but Recommended)
1. Go to https://resend.com/domains
2. Add your domain (e.g., smrutishah.com)
3. Add the DNS records provided by Resend to your domain
4. Wait for verification (usually takes a few minutes)

### 5. Update Email From Address
In `worker.py`, find the `send_email` function and update the "from" address:

```python
"from": "Job Tracker <noreply@smrutishah.com>",  # Change to your verified domain
```

If you haven't verified a domain, you can use Resend's test domain:
```python
"from": "Job Tracker <onboarding@resend.dev>",  # For testing only
```

## Testing

After setup, test the email functionality:
1. Try signing up with a new account
2. Check your email inbox for the verification code
3. If emails aren't arriving, check:
   - Resend dashboard for delivery status
   - Spam/junk folder
   - API key is correctly set as a secret

## Alternative Email Services

If you prefer a different email service, you can modify the `send_email` function in `worker.py` to use:
- SendGrid
- Mailgun
- AWS SES
- Cloudflare Email Workers

## Troubleshooting

**Emails not sending:**
- Verify RESEND_API_KEY secret is set: `wrangler secret list`
- Check Resend dashboard for API errors
- Ensure domain is verified (if using custom domain)

**Emails going to spam:**
- Verify your domain with Resend
- Use a verified domain in the "from" address
- Add SPF/DKIM records provided by Resend

