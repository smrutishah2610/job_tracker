# Cloudflare Setup After Resend API Key Creation

After creating your Resend API key, you need to configure it in Cloudflare. Here's what to do:

## Step-by-Step Setup

### 1. Set the Resend API Key as a Cloudflare Secret

Run this command in your terminal (from the project directory):

```bash
wrangler secret put RESEND_API_KEY
```

When prompted, paste your Resend API key:
```
re_fmF2hgy9_JNp85323QuxDa2SEw4koWsKG
```

**Important:** Secrets are stored securely by Cloudflare and are NOT visible in your code or `wrangler.toml` file.

### 2. Verify the Secret is Set

Check that your secret is configured:

```bash
wrangler secret list
```

You should see `RESEND_API_KEY` in the list.

### 3. Deploy Your Worker

Deploy the updated worker:

```bash
wrangler deploy
```

### 4. Test the Email Functionality

1. Visit your site: `https://smrutishah.com/jobtracking/login`
2. Try to sign up with a new account
3. Check your email for the verification code

## What Happens Behind the Scenes

- **Resend API Key**: Stored securely in Cloudflare's secret management
- **Worker Access**: Your `worker.py` code accesses it via `env.RESEND_API_KEY`
- **Email Sending**: When a user requests a verification code, the worker:
  1. Generates a 6-digit OTP
  2. Stores it in the database
  3. Calls Resend API to send the email
  4. Returns success/error to the user

## No Cloudflare Dashboard Configuration Needed

You **don't need to configure anything in the Cloudflare Dashboard** - everything is done via the `wrangler` CLI:

- ✅ Secrets are set via `wrangler secret put`
- ✅ Worker is deployed via `wrangler deploy`
- ✅ Routes are already configured (from your previous setup)

## Troubleshooting

**If emails still don't send:**

1. **Check secret is set:**
   ```bash
   wrangler secret list
   ```

2. **Check worker logs:**
   ```bash
   wrangler tail
   ```
   Then try signing up again and watch for errors.

3. **Verify API key is correct:**
   - Go to https://resend.com/api-keys
   - Make sure the key is active
   - Copy it again and reset the secret if needed

4. **Check Resend dashboard:**
   - Go to https://resend.com/emails
   - See if emails are being sent (even if they fail)
   - Check for any error messages

## Optional: Domain Verification (For Production)

If you want to use your own domain (`noreply@smrutishah.com`) instead of the test domain:

1. **In Resend Dashboard:**
   - Go to https://resend.com/domains
   - Add your domain: `smrutishah.com`
   - Copy the DNS records provided

2. **In Cloudflare Dashboard:**
   - Go to your domain's DNS settings
   - Add the SPF, DKIM, and DMARC records from Resend
   - Wait for verification (usually 5-10 minutes)

3. **Update worker.py:**
   - Change the "from" address in `send_email()` function:
   ```python
   "from": "Job Tracker <noreply@smrutishah.com>",
   ```

4. **Redeploy:**
   ```bash
   wrangler deploy
   ```

## Summary

**What you need to do:**
1. ✅ Run `wrangler secret put RESEND_API_KEY` (paste your API key)
2. ✅ Run `wrangler deploy`
3. ✅ Test the signup flow

**What you DON'T need to do:**
- ❌ Configure anything in Cloudflare Dashboard
- ❌ Add any environment variables manually
- ❌ Modify DNS settings (unless verifying domain)

That's it! The secret is automatically available to your worker when deployed.

